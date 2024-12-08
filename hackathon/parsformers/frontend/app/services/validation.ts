import { PrefabElement, PrefabElementSchema } from "@mod-construction/mod-dlm";
import testData from '../../assets/test_langchain.json';

const examplePrefabElement: PrefabElement = {
    id: '8be9e7b3-de6c-4621-8751-3a1b12d71f94',
    name: 'Insulated Concrete Wall Panel',
    description: 'A high-performance insulated concrete wall panel suitable for residential and commercial buildings.',
    boundingBox: {
        width: 3000, // in millimeters
        height: 6000, // in millimeters
        depth: 200 // in millimeters
    },
    images: [
        'https://example.com/images/panel-front.jpg',
        'https://example.com/images/panel-back.jpg'
    ],
    buildingSystem: 'Wall',
    productCategory: 'Insulated Concrete Panels',
    material: {
        finishMaterial: 'Concrete',
        structuralMaterial: 'Concrete'
    },
    dimensional: {
        width: {
            min: 1000,
            max: 4000
        },
        height: {
            min: 2000,
            max: 8000
        },
        length: {
            min: 100,
            max: 300
        }
    },
    structuralProperties: {
        loadBearingCapacity: {
            maximumLoad: 5000,
            unit: 'kN',
            loadDistribution: 'Uniform'
        },
        seismicResistance: 'Zone 3',
        windLoadResistance: 'Class C'
    },
    performance: {
        resistanceToFireClassification: 'A2',
        thermalTransmittance: 0.25,
        acousticProperties: {
            soundInsulationRating: 'Rw 55 dB',
            acousticPerformance: 'High'
        }
    },
    sustainability: {
        countryOfManufacturing: 'Germany',
        classification: 'A',
        VOCEmissions: 'Low',
        recyclability: '75%',
        energyEfficiency: 'LEED Gold'
    },
    documentationAndCompliance: {
        technicalSpecifications: 'https://example.com/specifications/panel-001.pdf',
        certifications: {
            certificationTypes: ['ISO 9001', 'CE Marking'],
            regulatoryApprovals: ['EN 14992', 'DIN 4102']
        }
    },
    installationAndConnectivity: {
        connectionType: 'Bolt-on',
        installationTime: '2 hours per panel',
        compatibility: 'Concrete Structure'
    },
    lifecycleAndMaintenance: {
        expectedLifespan: '50 years',
        maintenanceRequirements: 'Periodic inspection every 5 years',
        warranty: '10-year manufacturer warranty'
    },
    aestheticAndCustomizationOptions: {
        colorOptions: ['Gray', 'White', 'Beige'],
        texture: 'Smooth',
        modularAdaptability: 'Compatible with modular building systems'
    },
    economicFactors: {
        costPerUnit: 1500, // in euros
        manufacturingLeadTime: '4 weeks'
    }
};

// export function validatePrefabElement(input: unknown): { 
//     success: boolean; 
//     data?: PrefabElement; 
//     error?: any; 
// } {
//     // Type assertion of the input as PrefabElement
//     const prefabElement = input as PrefabElement;
    
//     // Validate using the schema
//     const validation = PrefabElementSchema.safeParse(prefabElement);
    
//     if (validation.success) {
//         return {
//             success: true,
//             data: validation.data
//         };
//     } else {
//         return {
//             success: false,
//             error: validation.error
//         };
//     }
// }

// ... existing imports ...

// Update the validation function to use test data
export function validatePrefabElement(json: any): { 
    success: boolean; 
    data?: PrefabElement; 
    error?: any; 
} {
    console.log(json)
    const data = json[0]
    try {
        // Use the example data that's already defined
        //const validation = PrefabElementSchema.safeParse(examplePrefabElement);
        const validation = PrefabElementSchema.safeParse(data);
        
        if (validation.success) {
            return {
                success: true,
                data: validation.data
            };
        } else {
            return {
                success: false,
                error: validation.error
            };
        }
    } catch (error) {
        return {
            success: false,
            error: error
        };
    }
}

// // Validate the element using the PrefabElementSchema
// const validation = PrefabElementSchema.safeParse(examplePrefabElement);

// if (validation.success) {
//    console.log('Element is valid:', validation.data);
// } else {
//    console.error('Element validation failed:', validation.error);
// }
