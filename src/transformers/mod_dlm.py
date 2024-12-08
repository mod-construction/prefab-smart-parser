from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from uuid import uuid4
from enum import Enum

class UndefinedType(str, Enum):
    UNDEFINED = "undefined"

class BoundingBox(BaseModel):
    width: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    height: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    depth: Union[float, UndefinedType] = UndefinedType.UNDEFINED

class Material(BaseModel):
    finishMaterial: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    structuralMaterial: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class Range(BaseModel):
    min: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    max: Union[float, UndefinedType] = UndefinedType.UNDEFINED

class Dimensional(BaseModel):
    width: Range = Field(default_factory=Range)
    height: Range = Field(default_factory=Range)
    length: Range = Field(default_factory=Range)

class LoadBearingCapacity(BaseModel):
    maximumLoad: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    unit: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    loadDistribution: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class StructuralProperties(BaseModel):
    loadBearingCapacity: LoadBearingCapacity = Field(default_factory=LoadBearingCapacity)
    seismicResistance: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    windLoadResistance: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class AcousticProperties(BaseModel):
    soundInsulationRating: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    acousticPerformance: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class Performance(BaseModel):
    resistanceToFireClassification: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    thermalTransmittance: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    acousticProperties: AcousticProperties = Field(default_factory=AcousticProperties)

class Sustainability(BaseModel):
    countryOfManufacturing: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    classification: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    VOCEmissions: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    recyclability: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    energyEfficiency: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class Certifications(BaseModel):
    certificationTypes: List[str] = Field(default_factory=list)
    regulatoryApprovals: List[str] = Field(default_factory=list)

class DocumentationAndCompliance(BaseModel):
    technicalSpecifications: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    certifications: Certifications = Field(default_factory=Certifications)

class InstallationAndConnectivity(BaseModel):
    connectionType: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    installationTime: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    compatibility: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class LifecycleAndMaintenance(BaseModel):
    expectedLifespan: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    maintenanceRequirements: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    warranty: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class AestheticAndCustomizationOptions(BaseModel):
    colorOptions: List[str] = Field(default_factory=list)
    texture: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    modularAdaptability: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class EconomicFactors(BaseModel):
    costPerUnit: Union[float, UndefinedType] = UndefinedType.UNDEFINED
    manufacturingLeadTime: Union[str, UndefinedType] = UndefinedType.UNDEFINED

class PrefabElement(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    description: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    boundingBox: BoundingBox = Field(default_factory=BoundingBox)
    images: List[str] = Field(default_factory=list)
    buildingSystem: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    productCategory: Union[str, UndefinedType] = UndefinedType.UNDEFINED
    material: Material = Field(default_factory=Material)
    dimensional: Dimensional = Field(default_factory=Dimensional)
    structuralProperties: StructuralProperties = Field(default_factory=StructuralProperties)
    performance: Performance = Field(default_factory=Performance)
    sustainability: Sustainability = Field(default_factory=Sustainability)
    documentationAndCompliance: DocumentationAndCompliance = Field(default_factory=DocumentationAndCompliance)
    installationAndConnectivity: InstallationAndConnectivity = Field(default_factory=InstallationAndConnectivity)
    lifecycleAndMaintenance: LifecycleAndMaintenance = Field(default_factory=LifecycleAndMaintenance)
    aestheticAndCustomizationOptions: AestheticAndCustomizationOptions = Field(default_factory=AestheticAndCustomizationOptions)
    economicFactors: EconomicFactors = Field(default_factory=EconomicFactors)

class ModDLMTransformer:
    """Transform extracted data into mod-dlm format"""

    def __init__(self):
        self.confidence_threshold = 0.8

    def _get_value_or_undefined(self, data: Dict, key: str, value_type: type = str) -> Union[any, UndefinedType]:
        """
        Get value from dictionary or return undefined if not present or empty
        
        Args:
            data: Dictionary containing data
            key: Key to look up
            value_type: Expected type of the value
        Returns:
            Value or UndefinedType.UNDEFINED
        """
        value = data.get(key)
        if value is None or value == "":
            return UndefinedType.UNDEFINED
        try:
            typed_value = value_type(value)
            return typed_value
        except (ValueError, TypeError):
            return UndefinedType.UNDEFINED

    async def transform(self, extracted_data: Dict) -> PrefabElement:
        """
        Transform extracted data into mod-dlm PrefabElement format
        
        Args:
            extracted_data: Dictionary containing extracted product information
        Returns:
            PrefabElement object
        """
        try:
            # Transform dimensional data
            dimensional = Dimensional(
                width=Range(
                    min=self._get_value_or_undefined(extracted_data, 'width_min', float),
                    max=self._get_value_or_undefined(extracted_data, 'width_max', float)
                ),
                height=Range(
                    min=self._get_value_or_undefined(extracted_data, 'height_min', float),
                    max=self._get_value_or_undefined(extracted_data, 'height_max', float)
                ),
                length=Range(
                    min=self._get_value_or_undefined(extracted_data, 'length_min', float),
                    max=self._get_value_or_undefined(extracted_data, 'length_max', float)
                )
            )

            # Create PrefabElement
            prefab_element = PrefabElement(
                name=self._get_value_or_undefined(extracted_data, 'product_name'),
                description=self._get_value_or_undefined(extracted_data, 'description'),
                boundingBox=BoundingBox(
                    width=self._get_value_or_undefined(extracted_data, 'width', float),
                    height=self._get_value_or_undefined(extracted_data, 'height', float),
                    depth=self._get_value_or_undefined(extracted_data, 'depth', float)
                ),
                images=extracted_data.get('images', []),
                buildingSystem=self._classify_building_system(extracted_data),
                productCategory=self._classify_product_category(extracted_data),
                material=Material(
                    finishMaterial=self._get_value_or_undefined(extracted_data, 'finish_material'),
                    structuralMaterial=self._get_value_or_undefined(extracted_data, 'structural_material')
                ),
                dimensional=dimensional,
                structuralProperties=self._transform_structural_properties(extracted_data),
                performance=self._transform_performance(extracted_data),
                sustainability=self._transform_sustainability(extracted_data),
                documentationAndCompliance=self._transform_documentation(extracted_data),
                installationAndConnectivity=self._transform_installation(extracted_data),
                lifecycleAndMaintenance=self._transform_lifecycle(extracted_data),
                aestheticAndCustomizationOptions=self._transform_aesthetics(extracted_data),
                economicFactors=self._transform_economic_factors(extracted_data)
            )

            return prefab_element

        except Exception as e:
            raise Exception(f"Transformation error: {str(e)}")

    def _classify_building_system(self, data: Dict) -> str:
        """Classify the building system based on extracted data"""
        keywords = {
            "Wall": ["wall", "partition", "facade"],
            "Floor": ["floor", "slab", "deck"],
            "Roof": ["roof", "ceiling"],
            "Structure": ["beam", "column", "frame"]
        }
        
        description = data.get('description', '').lower()
        for system, terms in keywords.items():
            if any(term in description for term in terms):
                return system
        return "Other"

    def _transform_structural_properties(self, data: Dict) -> StructuralProperties:
        """Transform structural properties data"""
        return StructuralProperties(
            loadBearingCapacity=LoadBearingCapacity(
                maximumLoad=float(data.get('max_load', 0)),
                unit=data.get('load_unit', 'kN'),
                loadDistribution=data.get('load_distribution', 'Unknown')
            ),
            seismicResistance=data.get('seismic_resistance', 'Unknown'),
            windLoadResistance=data.get('wind_load_resistance', 'Unknown')
        )

    def _transform_performance(self, data: Dict) -> Performance:
        """Transform performance data"""
        return Performance(
            resistanceToFireClassification=data.get('fire_resistance', 'Unknown'),
            thermalTransmittance=float(data.get('thermal_transmittance', 0.0)),
            acousticProperties=AcousticProperties(
                soundInsulationRating=data.get('sound_insulation', 'Unknown'),
                acousticPerformance=data.get('acoustic_performance', 'Unknown')
            )
        )

    def _transform_sustainability(self, data: Dict) -> Sustainability:
        """Transform sustainability data"""
        return Sustainability(
            countryOfManufacturing=data.get('manufacturing_country', 'Unknown'),
            classification=data.get('sustainability_class', 'Unknown'),
            VOCEmissions=data.get('voc_emissions', 'Unknown'),
            recyclability=data.get('recyclability', 'Unknown'),
            energyEfficiency=data.get('energy_efficiency', 'Unknown')
        )

    def _transform_documentation(self, data: Dict) -> DocumentationAndCompliance:
        """Transform documentation and compliance data"""
        return DocumentationAndCompliance(
            technicalSpecifications=data.get('technical_specs_url', ''),
            certifications=Certifications(
                certificationTypes=data.get('certifications', []),
                regulatoryApprovals=data.get('approvals', [])
            )
        )

    def _transform_installation(self, data: Dict) -> InstallationAndConnectivity:
        """Transform installation and connectivity data"""
        return InstallationAndConnectivity(
            connectionType=data.get('connection_type', 'Unknown'),
            installationTime=data.get('installation_time', 'Unknown'),
            compatibility=data.get('compatibility', 'Unknown')
        )

    def _transform_lifecycle(self, data: Dict) -> LifecycleAndMaintenance:
        """Transform lifecycle and maintenance data"""
        return LifecycleAndMaintenance(
            expectedLifespan=data.get('lifespan', 'Unknown'),
            maintenanceRequirements=data.get('maintenance', 'Unknown'),
            warranty=data.get('warranty', 'Unknown')
        )

    def _transform_aesthetics(self, data: Dict) -> AestheticAndCustomizationOptions:
        """Transform aesthetic and customization data"""
        return AestheticAndCustomizationOptions(
            colorOptions=data.get('colors', []),
            texture=data.get('texture', 'Unknown'),
            modularAdaptability=data.get('modularity', 'Unknown')
        )

    def _transform_economic_factors(self, data: Dict) -> EconomicFactors:
        """Transform economic factors data"""
        return EconomicFactors(
            costPerUnit=float(data.get('cost', 0.0)),
            manufacturingLeadTime=data.get('lead_time', 'Unknown')
        )

    def _classify_product_category(self, data: Dict) -> str:
        """Classify the product category based on extracted data"""
        description = data.get('description', '').lower()
        categories = {
            "Insulated Concrete Panels": ["insulated", "concrete", "panel"],
            "Structural Frames": ["frame", "structural", "beam"],
            "Modular Units": ["modular", "unit", "pod"],
            "Facade Elements": ["facade", "cladding", "curtain"]
        }
        
        for category, keywords in categories.items():
            if all(keyword in description for keyword in keywords):
                return category
        return "Other"

    def validate(self, mod_dlm_data: Dict) -> bool:
        """Validate mod-dlm formatted data"""
        # Implementation here
        pass 