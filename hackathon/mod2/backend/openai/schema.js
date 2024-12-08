const examplePrefabElement = {
    id: '', 
    name: '',
    description: '',
    boundingBox: {
        width: 0,
        height: 0,
        depth: 0,
    },
    images: [],
    buildingSystem: '',
    productCategory: '',
    material: {
        finishMaterial: '',
        structuralMaterial: '',
    },
    dimensional: {
        width: { min: 0, max: 0 },
        height: { min: 0, max: 0 },
        length: { min: 0, max: 0 },
    },
    structuralProperties: {
        loadBearingCapacity: {
            maximumLoad: 0,
            unit: '',
            loadDistribution: '',
        },
        seismicResistance: '',
        windLoadResistance: '',
    },
    performance: {
        resistanceToFireClassification: '',
        thermalTransmittance: 0,
        acousticProperties: {
            soundInsulationRating: '',
            acousticPerformance: '',
        },
    },
    sustainability: {
        countryOfManufacturing: '',
        classification: '',
        VOCEmissions: '',
        recyclability: '',
        energyEfficiency: '',
    },
    documentationAndCompliance: {
        technicalSpecifications: '',
        certifications: {
            certificationTypes: [],
            regulatoryApprovals: [],
        },
    },
    installationAndConnectivity: {
        connectionType: '',
        installationTime: '',
        compatibility: '',
    },
    lifecycleAndMaintenance: {
        expectedLifespan: '',
        maintenanceRequirements: '',
        warranty: '',
    },
    aestheticAndCustomizationOptions: {
        colorOptions: [],
        texture: '',
        modularAdaptability: '',
    },
    economicFactors: {
        costPerUnit: 0,
        manufacturingLeadTime: '',
    },
};

module.exports = examplePrefabElement;
