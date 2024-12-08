from typing import Dict, List, Optional, Tuple
import spacy
from spacy.language import Language
from spacy.tokens import Doc
import re
from core.config import settings
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class MeasurementUnit:
    value: float
    unit: str
    dimension: Optional[str] = None

class NLPProcessor:
    def __init__(self):
        # Load spaCy model based on settings
        self.nlp = spacy.load(settings.SPACY_MODEL)
        
        # Add custom components to pipeline
        self.add_custom_components()
        
        # Compile regex patterns
        self.measurement_pattern = re.compile(
            r'(\d+(?:\.\d+)?)\s*(mm|cm|m|kg|m²|m2|m³|m3)'
        )
        
        # Common construction-specific terms
        self.material_indicators = {
            'made of', 'constructed from', 'built with',
            'material:', 'materials:', 'composition:'
        }

    def add_custom_components(self):
        """Add custom pipeline components to spaCy"""
        
        @Language.component("measurement_detector")
        def measurement_detector(doc: Doc) -> Doc:
            """Detect and classify measurements in text"""
            matches = self.measurement_pattern.finditer(doc.text)
            for match in matches:
                value, unit = match.groups()
                span = doc.char_span(match.start(), match.end())
                if span:
                    span._.measurement = MeasurementUnit(
                        value=float(value),
                        unit=unit
                    )
            return doc

        # Register custom extensions
        if not Doc.has_extension("measurements"):
            Doc.set_extension("measurements", default=[])
        
        # Add components to pipeline
        self.nlp.add_pipe("measurement_detector", after="ner")

    async def process(self, text: str) -> Dict:
        """
        Process text through NLP pipeline
        
        Args:
            text: Input text to process
        Returns:
            Dictionary containing extracted information
        """
        doc = self.nlp(text)
        
        return {
            'measurements': self.extract_measurements(doc),
            'materials': self.extract_materials(doc),
            'technical_terms': self.extract_technical_terms(doc),
            'key_phrases': self.extract_key_phrases(doc),
            'entities': self.extract_entities(doc)
        }

    def extract_measurements(self, doc: Doc) -> List[Dict]:
        """Extract and standardize measurements"""
        measurements = []
        
        for match in self.measurement_pattern.finditer(doc.text):
            value, unit = match.groups()
            
            # Standardize units
            standardized = self.standardize_unit(float(value), unit)
            
            # Detect measurement context
            context = self.detect_measurement_context(doc, match.start())
            
            measurements.append({
                'original': f"{value} {unit}",
                'standardized': standardized,
                'context': context
            })
            
        return measurements

    def extract_materials(self, doc: Doc) -> List[Dict]:
        """Extract material information"""
        materials = []
        
        for sent in doc.sents:
            # Check for material indicators
            if any(indicator in sent.text.lower() for indicator in self.material_indicators):
                # Extract material entities and their properties
                for token in sent:
                    if token.pos_ == "NOUN" and not token.is_stop:
                        materials.append({
                            'material': token.text,
                            'context': sent.text,
                            'confidence': self.calculate_confidence(token)
                        })
        
        return materials

    def extract_technical_terms(self, doc: Doc) -> List[Dict]:
        """Extract technical specifications and terminology"""
        terms = defaultdict(list)
        
        for sent in doc.sents:
            # Look for technical specifications patterns
            if any(term in sent.text.lower() for term in ['spec', 'technical', 'specification']):
                for token in sent:
                    if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop:
                        terms[token.text].append(sent.text)
        
        return [{'term': k, 'contexts': v} for k, v in terms.items()]

    def extract_key_phrases(self, doc: Doc) -> List[str]:
        """Extract important phrases using dependency parsing"""
        key_phrases = []
        
        for chunk in doc.noun_chunks:
            if chunk.root.dep_ in ['nsubj', 'dobj', 'pobj']:
                key_phrases.append(chunk.text)
        
        return key_phrases

    def extract_entities(self, doc: Doc) -> Dict[str, List[str]]:
        """Extract named entities"""
        entities = defaultdict(list)
        
        for ent in doc.ents:
            entities[ent.label_].append(ent.text)
            
        return dict(entities)

    def standardize_unit(self, value: float, unit: str) -> Dict:
        """Standardize measurements to SI units"""
        conversions = {
            'cm': ('m', 0.01),
            'mm': ('m', 0.001),
            'm2': ('m²', 1),
            'm3': ('m³', 1),
        }
        
        if unit in conversions:
            si_unit, factor = conversions[unit]
            return {
                'value': value * factor,
                'unit': si_unit
            }
        
        return {
            'value': value,
            'unit': unit
        }

    def detect_measurement_context(self, doc: Doc, measurement_start: int) -> str:
        """Detect the context of a measurement"""
        context_window = 5  # tokens before and after
        
        for sent in doc.sents:
            if sent.start_char <= measurement_start <= sent.end_char:
                context_start = max(0, sent.start)
                context_end = min(len(doc), sent.end)
                
                context_tokens = doc[context_start:context_end]
                return context_tokens.text
                
        return ""

    def calculate_confidence(self, token) -> float:
        """Calculate confidence score for extracted information"""
        confidence = 0.0
        
        # Base confidence on various factors
        if token.pos_ in ["NOUN", "PROPN"]:
            confidence += 0.3
        if not token.is_stop:
            confidence += 0.2
        if token.dep_ in ["nsubj", "dobj"]:
            confidence += 0.3
        if token.ent_type_:
            confidence += 0.2
            
        return min(confidence, 1.0) 