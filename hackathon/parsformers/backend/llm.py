from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import uuid
import json
from preprocess import extract_text_from_pdf, split_into_sentences, create_overlapping_chunks
import PyPDF2

building_system = [
          "Wall",
          "Balcony",
          "Pod",
          "Frame",
          "Facade",
          "Floors",
          "Modules",
          "Plants",
          "Roofs",
          "Stairs"
        ]
product_category = [
          "Boarding",
          "Solid Wall Panels",
          "Closed Wall Panels",
          "Twinwall",
          "Open Wall Panels",
          "Structural Insulated Panels (SIPs)",
          "Insulated Concrete Panels",
          "Prefabricated Balcony",
          "Pod",
          "Whole Building System",
          "Structural Frame",
          "Facade System",
          "Hollowcore Floor",
          "Concrete Lattice Floor",
          "Floor Cassettes",
          "Solid Floor Panels",
          "Volumetric module",
          "Prefabricated Plant",
          "Roof Panel",
          "Roof Truss",
          "Prefabricated Stairs"
        ]
material = [
              "Timber",
              "Steel",
              "Concrete",
              "Hybrid",
              "Other"
            ]

load_dotenv()

def define_model():
    llm = ChatOpenAI(temperature=0)
    return llm

class SchemaOutput(BaseModel):
    id: str
    name: str
    description: str
    boundingBox: dict
    buildingSystem: str
    productCategory: str
    material: dict
    dimensional: dict

def map_llm_response_to_updated_schema(llm_response: dict) -> dict:
    """Map the LLM response to the updated schema format."""
    try:
        # Generate required fields
        element_id = generate_uuid()
        name = llm_response.get("element", "Unknown Element")
        description = llm_response.get("explanation", "No description provided.")

        # Populate boundingBox with values (keeping units)
        bounding_box = {
            "width": llm_response.get("width", 0), 
            "height": llm_response.get("height", 0), 
            "length": llm_response.get("length", 0)
        }
        dimensional = {
            "width": {"min":llm_response.get("min_width", 0),
                      "max":llm_response.get("max_width", 0)}, 
            "height": {"min":llm_response.get("min_height", 0),
                      "max":llm_response.get("max_height", 0)}, 
            "length": {"min":llm_response.get("min_heigt", 0),
                      "max":llm_response.get("max_height", 0)}, 
        }

        material = {
            "finishMaterial": llm_response.get("material", "Other"),
            "structuralMaterial": llm_response.get("material", "Other"),
        }

        structural_properties = {
            "loadBearingCapacity": {
                "maximumLoad": llm_response.get("maximum_load", 0),
                "unit": llm_response.get("load_unit", "None"),
                "loadDistribution": llm_response.get("load_distribution", "None"),
            }
        }

        performance = {
            "resistanceToFireClassification": llm_response.get("resistance_to_fire_classification", None),
            "thermalTransmittance": llm_response.get("thermal_transmittance", 0),
            "acousticProperties": {
                "soundInsulationRating": llm_response.get("sound_insulation_rating", None),
                "acousticPerformance": llm_response.get("acoustic_performance", None),
            }
        }

        sustainability = {
            "countryOfManufacturing": llm_response.get("country_of_manufacturing", None),
            "classification": llm_response.get("sustainability_classification", None),
        }

        documentation_and_compliance = {
            "technicalSpecifications": llm_response.get("technical_specifications", None),
            "certifications": {
                "certificationTypes": llm_response.get("certification_types", []),
                "regulatoryApprovals": llm_response.get("regulatory_approvals", []),
            }
        }

        lifecycle_and_maintenance = {
            "expectedLifespan": llm_response.get("expected_lifespan", None),
            "maintenanceRequirements": llm_response.get("maintenance_requirements", None),
            "warranty": llm_response.get("warranty", None),
        }

        schema_element = {
            "id": element_id,
            "name": name,
            "description": description,
            "boundingBox": {
                "width": bounding_box["width"],
                "height": bounding_box["height"],
                "depth": bounding_box["length"],  # Assuming depth = length
            },
            "images": [],  # Placeholder for image links
            "buildingSystem": llm_response.get("building_system", "Unknown"),
            "productCategory": llm_response.get("product_category", "Unknown"),
            "material": material,
            "dimensional": dimensional,
            "structuralProperties": structural_properties,
            "performance": performance,
            "sustainability": sustainability,
            "documentationAndCompliance": documentation_and_compliance,
            "lifecycleAndMaintenance": lifecycle_and_maintenance,
        }
        return schema_element
    except Exception as e:
        print(f"Error mapping LLM response to schema: {e}")
        return None

def generate_uuid():
    """Generate a unique UUID."""
    return str(uuid.uuid4())

class ChooseType(BaseModel):
    element: str = Field(description="What is the name of idetified entity.")
    building_system: str = Field(description="What kind of building system category the element belongs to.")
    product_category: str = Field(description="What kind of product category the element belongs to.")
    explanation: str = Field(description="The reason why you chose this specific product category.")
    material: str = Field(description="What kind of material the element is built from?")
    height: int = Field(description="What is the height of the element, as an integer value")
    width: int = Field(description="What is the  width of the element?")
    length: int = Field(description="What is the length of the element?")
    maximum_height: int = Field(description="What is the maximum height of the element, as an integer value")
    minimum_height: int = Field(description="What is the minimum height of the element, as an integer value")
    max_width: int = Field(description="What is the maximum width of the element, as an integer value")
    min_width: int = Field(description="What is the minimum width of the element, as an integer value")
    max_length: int = Field(description="What is the maximum length of the element, as an integer value")
    min_length: int = Field(description="What is the minimum length of the element, as an integer value")
    # New fields
    maximum_load: int = Field(description="What is the maximum load-bearing capacity of the element, as an integer value")
    load_unit: str = Field(description="What is the unit of the load-bearing capacity, as unit in string")
    load_distribution: str = Field(description="Describe the load distribution of the element.")
    resistance_to_fire_classification: str = Field(description="What is the resistance to fire classification of the element?")
    thermal_transmittance: int = Field(description="What is the thermal transmittance of the element as an integer value?")
    sound_insulation_rating: str = Field(description="What is the sound insulation rating of the element?")
    acoustic_performance: str = Field(description="Describe the acoustic performance of the element.")
    country_of_manufacturing: str = Field(description="Which country is the element manufactured in?")
    sustainability_classification: str = Field(description="What is the sustainability classification of the element?")
    technical_specifications: str = Field(description="Provide the technical specifications of the element.")
    certification_types: str = Field(description="List the certification types of the element.")
    regulatory_approvals: str = Field(description="List the regulatory approvals of the element.")
    expected_lifespan: str = Field(description="What is the expected lifespan of the element?")
    maintenance_requirements: str = Field(description="What are the maintenance requirements of the element?")
    warranty: str = Field(description="What is the warranty period of the element?")

def llm_stack(model, chunk):
    """Process a single chunk with the LLM and map the response."""
    building_system = [
        "Wall", "Balcony", "Pod", "Frame", "Facade", "Floors", "Modules", "Plants", "Roofs", "Stairs"
    ]
    product_category = [
        "Boarding", "Solid Wall Panels", "Closed Wall Panels", "Twinwall",
        "Open Wall Panels", "Structural Insulated Panels (SIPs)", "Insulated Concrete Panels",
        "Prefabricated Balcony", "Pod", "Whole Building System", "Structural Frame", "Facade System",
        "Hollowcore Floor", "Concrete Lattice Floor", "Floor Cassettes", "Solid Floor Panels",
        "Volumetric module", "Prefabricated Plant", "Roof Panel", "Roof Truss", "Prefabricated Stairs"
    ]
    material = ["Timber", "Steel", "Concrete", "Hybrid", "Other"]

    parser = JsonOutputParser(pydantic_object=ChooseType)
    # template = """
    #     You are an assistant that identifies elements related to the building domain. For each element:
    #     - Extract metadata and match it to predefined categories.
    #     - Fill missing data with 'None'.
    #     - Please consider synonyms of the words, such as thickness for the width.
    #     Features to extract:
    #     - Building system: {building_system}
    #     - Product category: {product_category}
    #     - Materials: {material}
    #     - Maximum and minimum dimensions (height, width, length)
    #     - Load bearing capacity (maximum load, unit, load distribution)
    #     - Resistance to fire classification
    #     - Thermal transmittance
    #     - Acoustic properties (sound insulation rating, acoustic performance)
    #     - Country of manufacturing
    #     - Sustainability classification
    #     - Technical specifications
    #     - Certifications (certification types, regulatory approvals)
    #     - Expected lifespan
    #     - Maintenance requirements
    #     - Warranty

    #     Given text: {chunk}

    #     Output format: {format_instructions}
    # """
    template = """
    You are an assistant that reads the given text and identifies elements related to the building domain. Here is a sample workflow that you can follow:
    1. Identify the elements described in the text.  
    2. Extract metadata about the element, including dimensions, material, and other properties. Use synonyms for interpretation (e.g., "width" could be "thickness" or "breadth").
    3. If some features are indirectly mentioned or implied, infer the values if possible. For example, if "thick concrete walls" is stated, infer a material of "Concrete" and a general width range.
    4. For features that are not mentioned, type "None" for missing data.
    Every numerical units must be in milimeters, and just output numerical values as an integer without the unit. 

    Features to extract:
    - Element Name
    - Building system: One of the following categories: {building_system}
    - Product category: One of the following categories: {product_category}
    - Material: One of the following: {material}
    - Dimensions:
      - Maximum height, minimum height
      - Maximum width, minimum width
      - Maximum length, minimum length
    - Structural properties (if mentioned):
      - Maximum load-bearing capacity (maximum load, unit, load distribution)
    - Performance features:
      - Resistance to fire classification
      - Thermal transmittance
      - Acoustic properties (sound insulation rating, acoustic performance)
    - Sustainability features:
      - Country of manufacturing
      - Sustainability classification
    - Documentation:
      - Technical specifications
      - Certification types
      - Regulatory approvals
    - Lifecycle and maintenance:
      - Expected lifespan
      - Maintenance requirements
      - Warranty

    Please use the exact format below for your response. Do not skip any field, and use "None" for missing data.

    Example input:
    "The wall system consists of solid wall panels made of concrete, with a thickness between 18 cm and 40 cm, and a height up to 9 meters."

    Example output:
    {{
        "element": "Wall System",
        "building_system": "Wall",
        "product_category": "Solid Wall Panels",
        "explanation": "The text mentions solid wall panels made of concrete with specific dimensions.",
        "material": "Concrete",
        "height": 9000,
        "width": 1234,
        "length": 500,
        "maximum height": 1000,
        "minimum height": 10,
        "maximum width": 200,
        "minimum width": 10,
        "maximum length": 30,
        "minimum length": 10,
        "maximum load": 500,
        "load unit": "kn",
        "load distribution": "None",
        "resistance to fire classification": "None",
        "thermal transmittance": "None",
        "sound insulation rating": "None",
        "acoustic performance": "None",
        "country of manufacturing": "None",
        "sustainability classification": "None",
        "technical specifications": "None",
        "certification types": [],
        "regulatory approvals": [],
        "expected lifespan": "None",
        "maintenance requirements": "None",
        "warranty": "None"
    }}

    - Given text: {chunk}

    - Output format: {format_instructions}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["building_system", "product_category", "material", "chunk"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    result = chain.invoke({
        "building_system": building_system,
        "product_category": product_category,
        "material": material,
        "chunk": chunk,
    })
    return map_llm_response_to_updated_schema(result)


if __name__ == "__main__":
    file_name= "bele_doppelwand_2015"
    pdf_file_path = f"Data/PDFs/{file_name}.pdf"
    pdf_text = extract_text_from_pdf(pdf_file_path)
    sentences_list = split_into_sentences(pdf_text)
    chunks = create_overlapping_chunks(sentences_list)

    model = define_model()
    schema_outputs = []

    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index + 1}/{len(chunks)}...")
        llm_response = llm_stack(model, chunk)
        print("LLM Response: ", llm_response)
        if llm_response:
            print("The output after mapping ... ")
            schema_outputs.append(llm_response)

    print("Final Schema Outputs:")
    print(schema_outputs)

    try:
        import os
        os.makedirs("result", exist_ok=True)

        # Write JSON to file
        with open(f"result/{file_name}.json", "w") as file:
            json.dump(schema_outputs, file, indent=4)  
    except Exception as e:
        print("The error:", e)  

        ## 