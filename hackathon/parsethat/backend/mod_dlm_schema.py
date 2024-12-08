from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

# Enums
class BuildingSystem(str, Enum):
    WALL = "Wall"
    BALCONY = "Balcony"
    POD = "Pod"
    FRAME = "Frame"
    FACADE = "Facade"
    FLOORS = "Floors"
    MODULES = "Modules"
    PLANTS = "Plants"
    ROOFS = "Roofs"
    STAIRS = "Stairs"


class ProductCategory(str, Enum):
    BOARDING = "Boarding"
    SOLID_WALL_PANELS = "Solid Wall Panels"
    CLOSED_WALL_PANELS = "Closed Wall Panels"
    TWINWALL = "Twinwall"
    OPEN_WALL_PANELS = "Open Wall Panels"
    SIPS = "Structural Insulated Panels (SIPs)"
    INSULATED_CONCRETE_PANELS = "Insulated Concrete Panels"
    PREFABRICATED_BALCONY = "Prefabricated Balcony"
    POD = "Pod"
    WHOLE_BUILDING_SYSTEM = "Whole Building System"
    STRUCTURAL_FRAME = "Structural Frame"
    FACADE_SYSTEM = "Facade System"
    HOLLOWCORE_FLOOR = "Hollowcore Floor"
    CONCRETE_LATTICE_FLOOR = "Concrete Lattice Floor"
    FLOOR_CASSETTES = "Floor Cassettes"
    SOLID_FLOOR_PANELS = "Solid Floor Panels"
    VOLUMETRIC_MODULE = "Volumetric module"
    PREFABRICATED_PLANT = "Prefabricated Plant"
    ROOF_PANEL = "Roof Panel"
    ROOF_TRUSS = "Roof Truss"
    PREFABRICATED_STAIRS = "Prefabricated Stairs"


class MaterialType(str, Enum):
    TIMBER = "Timber"
    STEEL = "Steel"
    CONCRETE = "Concrete"
    HYBRID = "Hybrid"
    OTHER = "Other"


class StructuralUnit(str, Enum):
    N = "N"
    KN = "kN"
    LBF = "lbf"
    KGF = "kgf"


class SeismicResistance(str, Enum):
    ZONE_1 = "Zone 1"
    ZONE_2 = "Zone 2"
    ZONE_3 = "Zone 3"
    ZONE_4 = "Zone 4"


class WindLoadResistance(str, Enum):
    CLASS_A = "Class A"
    CLASS_B = "Class B"
    CLASS_C = "Class C"
    CLASS_D = "Class D"


class FireClassification(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    HOUR_1 = "1-hour"
    HOUR_2 = "2-hour"
    HOUR_3 = "3-hour"
    HOUR_4 = "4-hour"


class SustainabilityClassification(str, Enum):
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class VOCEmissions(str, Enum):
    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Recyclability(str, Enum):
    PERCENT_0 = "0%"
    PERCENT_25 = "25%"
    PERCENT_50 = "50%"
    PERCENT_75 = "75%"
    PERCENT_100 = "100%"


class EnergyEfficiency(str, Enum):
    R1 = "R-1"
    R2 = "R-2"
    R5 = "R-5"
    ENERGY_STAR = "Energy Star"
    LEED_CERTIFIED = "LEED Certified"
    LEED_SILVER = "LEED Silver"
    LEED_GOLD = "LEED Gold"
    LEED_PLATINUM = "LEED Platinum"


class ConnectionType(str, Enum):
    BOLT_ON = "Bolt-on"
    WELDED = "Welded"
    CLIP_ON = "Clip-on"
    ADHESIVE = "Adhesive"
    MORTAR = "Mortar"


class CompatibilityType(str, Enum):
    STEEL_FRAME = "Steel Frame"
    WOOD_FRAME = "Wood Frame"
    CONCRETE_STRUCTURE = "Concrete Structure"
    BRICKWORK = "Brickwork"
    MODULAR_SYSTEMS = "Modular Systems"
    GLASS_FACADES = "Glass Facades"
    COMPOSITE_MATERIALS = "Composite Materials"


# Base Schemas
class BoundingBox(BaseModel):
    width: float
    height: float
    depth: float


class Material(BaseModel):
    finishMaterial: MaterialType
    structuralMaterial: MaterialType


class DimensionalRange(BaseModel):
    min: float
    max: float


class Dimensional(BaseModel):
    width: DimensionalRange
    height: DimensionalRange
    length: DimensionalRange


# class StructuralProperties(BaseModel):
#     loadBearingCapacity: Optional[dict] = None
#     seismicResistance: Optional[SeismicResistance] = None
#     windLoadResistance: Optional[WindLoadResistance] = None


class AcousticProperties(BaseModel):
    soundInsulationRating: str
    acousticPerformance: str


class Performance(BaseModel):
    resistanceToFireClassification: FireClassification
    thermalTransmittance: float
    acousticProperties: AcousticProperties


class Sustainability(BaseModel):
    countryOfManufacturing: str
    classification: SustainabilityClassification
    VOCEmissions: VOCEmissions
    recyclability: Recyclability
    energyEfficiency: EnergyEfficiency


class Certifications(BaseModel):
    certificationTypes: List[str]
    regulatoryApprovals: List[str]


class DocumentationAndCompliance(BaseModel):
    technicalSpecifications: str
    certifications: Certifications


class InstallationAndConnectivity(BaseModel):
    connectionType: ConnectionType
    installationTime: str
    compatibility: CompatibilityType


class PrefabElement(BaseModel):
    name: str
    description: str
    boundingBox: BoundingBox
    images: List[str]
    buildingSystem: BuildingSystem
    productCategory: ProductCategory
    material: Material
    dimensional: Dimensional
    # structuralProperties: Optional[StructuralProperties] = None
    performance: Performance
    sustainability: Sustainability
    documentationAndCompliance: DocumentationAndCompliance
    installationAndConnectivity: Optional[InstallationAndConnectivity] = None
