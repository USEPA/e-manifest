# The Manifest

The Uniform Hazardous Waste Manifest (AKA "manifest" or EPA form 8700-22) is form required by EPA for all hazardous waste generators who transport hazardous waste for off-site treatment, recycling, storage or disposal.
It is also commonly used to satify and U.S. Department of Transportation (DOT) requirements.
When completed, the form contains information on the type and quantity of the waste being transported, instructions for handling the waste, and signature lines

## Paper Manifests

Since the inception of the uniform manifest, the manifesting process was completed on
[NCR paper](https://www.google.com/search?client=firefox-b-1-d&q=NCR+paper#ip=1) often refered to
as carbon-copy paper. e-Manifest collects these manifest in addition to managing electronic manifests.
With paper manifests, once the waste reaches its destination, the designated receiving facility returns one of the signed copies to the generator, and submits one to the e-Manifest system using one of
[the available submission methods](https://www.epa.gov/e-manifest/how-submit-hazardous-waste-manifest)

![sample paper manifest](../assets/sample_uniform_hazardous_waste_manifest.png)

Only [registered manifest printers](https://www.epa.gov/hwgenerators/hazardous-waste-manifest-system#printer) can print paper manifest. You can print paper copies of electronic manifest from the e-Manifest system for Hybrid manifests and to carry onboard with the transporter for DOT purposes. EPA established this procedure, in part, to ensure that each manifest has a unique identifying string called the Manifest Tracking Number (MTN) in box 4.

All paper manifests that accompany waste that requires manifesting (whether the waste is federally regualted or state regualted in the generatoring or receiving state) must be submitted to the e-Manifest system by the designated receving facility. The Receiving facility is required to pay a fee, the amount depends on the submission type and the current e-Manifest fees.

## Electronic Manifests

An Electronic manifest is the electronic format of the uniform hazardous waste manifest obtained and completed through the e-Manifest system. It is the legal equivalent. At the time of writing, all electronic manifest use the letters "ELC" as the suffix to their manifest tracking number.

Arguably the easiest way to visualize an electronic manifest is [JSON](https://www.json.org/json-en.html) encoded.

```json
{
  "createdDate": "2021-10-20T15:12:35.046+00:00",
  "updatedDate": "2023-06-01T18:26:52.793+00:00",
  "manifestTrackingNumber": "100032713ELC",
  "status": "Signed",
  "discrepancy": false,
  "submissionType": "FullElectronic",
  "originType": "Service",
  "shippedDate": "2023-02-10T05:42:05.246+00:00",
  "receivedDate": "2023-06-01T18:21:18.642+00:00",
  "generator": {
    "epaSiteId": "VATESTGEN001",
    "name": "VA TEST GEN 2021",
    "modified": true,
    "registered": true,
    "mailingAddress": {
      "address1": "123 VA TEST GEN 2021 WAY",
      "city": "ARLINGTON",
      "state": {
        "code": "VA",
        "name": "VIRGINIA"
      },
      "country": {
        "code": "US",
        "name": "UNITED STATES"
      },
      "zip": "22202"
    },
    "siteAddress": {
      "address1": "123 VA TEST GEN 2021 WAY",
      "city": "ARLINGTON",
      "state": {
        "code": "VA",
        "name": "VIRGINIA"
      },
      "country": {
        "code": "US",
        "name": "UNITED STATES"
      },
      "zip": "22202"
    },
    "contact": {
      "phone": {
        "number": "555-555-5555"
      },
      "email": "Testing@EPA.GOV"
    },
    "emergencyPhone": {
      "number": "888-888-8888"
    },
    "electronicSignaturesInfo": [
      {
        "humanReadableDocument": {
          "name": "human-readable.html",
          "size": 174777,
          "mimeType": "TEXT_HTML"
        }
      }
    ],
    "gisPrimary": false,
    "canEsign": true,
    "limitedEsign": true,
    "hasRegisteredEmanifestUser": true
  },
  "transporters": [
    {
      "epaSiteId": "VATESTRAN02",
      "name": "VA TEST TRAN 2021",
      "modified": true,
      "registered": true,
      "mailingAddress": {
        "address1": "321 VA TEST TRAN 2021 ROAD",
        "city": "ARLINGTON",
        "state": {
          "code": "VA",
          "name": "VIRGINIA"
        },
        "country": {
          "code": "US",
          "name": "UNITED STATES"
        },
        "zip": "22202"
      },
      "siteAddress": {
        "address1": "321 VA TEST TRAN 2021 ROAD",
        "city": "ARLINGTON",
        "state": {
          "code": "VA",
          "name": "VIRGINIA"
        },
        "country": {
          "code": "US",
          "name": "UNITED STATES"
        },
        "zip": "22202"
      },
      "contact": {
        "phone": {
          "number": "888-999-8888"
        }
      },
      "electronicSignaturesInfo": [
        {
          "signer": {
            "firstName": "John",
            "lastName": "Doe",
            "userId": "jdoe12345"
          },
          "signatureDate": "2023-02-10T05:42:05.246+00:00",
          "humanReadableDocument": {
            "name": "human-readable.html",
            "size": 181426,
            "mimeType": "TEXT_HTML"
          },
          "signerRole": "Industry",
          "signatureMethod": "QuickerSign"
        }
      ],
      "gisPrimary": false,
      "canEsign": true,
      "limitedEsign": true,
      "hasRegisteredEmanifestUser": true,
      "order": 1
    }
  ],
  "designatedFacility": {
    "epaSiteId": "VATESTTSDF03",
    "name": "VA TEST TSDF 2021",
    "modified": true,
    "registered": true,
    "mailingAddress": {
      "address1": "234 VA TEST TSDF 2021 DRIVE",
      "city": "ARLINGTON",
      "state": {
        "code": "VA",
        "name": "VIRGINIA"
      },
      "country": {
        "code": "US",
        "name": "UNITED STATES"
      },
      "zip": "22202"
    },
    "siteAddress": {
      "address1": "234 VA TEST TSDF 2021 DRIVE",
      "city": "ARLINGTON",
      "state": {
        "code": "VA",
        "name": "VIRGINIA"
      },
      "country": {
        "code": "US",
        "name": "UNITED STATES"
      },
      "zip": "22202"
    },
    "contact": {
      "phone": {
        "number": "555-555-5555"
      },
      "email": "Testing@EPA.GOV"
    },
    "electronicSignaturesInfo": [
      {
        "signer": {
          "firstName": "Jane",
          "lastName": "foo",
          "userId": "janefoo12345"
        },
        "signatureDate": "2023-06-01T18:21:18.642+00:00",
        "humanReadableDocument": {
          "name": "human-readable.html",
          "size": 179135,
          "mimeType": "TEXT_HTML"
        },
        "signerRole": "Industry",
        "signatureMethod": "QuickSign"
      },
      {
        "humanReadableDocument": {
          "name": "human-readable.html",
          "size": 179162,
          "mimeType": "TEXT_HTML"
        }
      }
    ],
    "gisPrimary": false,
    "canEsign": true,
    "limitedEsign": true,
    "hasRegisteredEmanifestUser": true
  },
  "wastes": [
    {
      "dotHazardous": true,
      "dotInformation": {
        "idNumber": {
          "code": "NA1993"
        },
        "printedDotInformation": "NA1993, Waste Diesel fuel, 3, III"
      },
      "quantity": {
        "containerNumber": 13,
        "containerType": {
          "code": "DM",
          "description": "Metal drums, barrels, kegs"
        },
        "quantity": 481,
        "unitOfMeasurement": {
          "code": "G",
          "description": "Gallons"
        }
      },
      "hazardousWaste": {
        "federalWasteCodes": [
          {
            "code": "D001",
            "description": "IGNITABLE WASTE"
          }
        ],
        "tsdfStateWasteCodes": [],
        "generatorStateWasteCodes": []
      },
      "additionalInfo": {
        "comments": [
          {
            "label": "Profile #",
            "description": "E654321",
            "handlerId": "VATESTRAN02"
          }
        ],
        "handlingInstructions": "This Manifest is for testing purposes and does not match reality it's more to show what you can do."
      },
      "lineNumber": 1,
      "br": false,
      "managementMethod": {
        "code": "H040",
        "description": "INCINERATION"
      },
      "pcb": false,
      "discrepancyResidueInfo": {
        "wasteQuantity": false,
        "wasteType": false,
        "residue": false
      },
      "epaWaste": true
    },
    {
      "dotHazardous": false,
      "wasteDescription": "PCB contaminated bags",
      "quantity": {
        "containerNumber": 12,
        "containerType": {
          "code": "BA",
          "description": "Burlap, cloth, paper, or plastic bags"
        },
        "quantity": 132,
        "unitOfMeasurement": {
          "code": "K",
          "description": "Kilograms"
        }
      },
      "hazardousWaste": {
        "federalWasteCodes": [],
        "tsdfStateWasteCodes": [],
        "generatorStateWasteCodes": []
      },
      "additionalInfo": {
        "handlingInstructions": "This Manifest is for testing purposes and does not match reality it's more to show what you can do."
      },
      "lineNumber": 2,
      "br": false,
      "managementMethod": {
        "code": "H040",
        "description": "INCINERATION"
      },
      "pcb": true,
      "pcbInfos": [
        {
          "loadType": {
            "code": "BulkWaste"
          },
          "dateOfRemoval": "2018-04-18T16:00:00.000+00:00",
          "weight": 432,
          "bulkIdentity": "Bulk Waste ID2"
        },
        {
          "loadType": {
            "code": "BulkWaste"
          },
          "dateOfRemoval": "2018-03-18T16:00:00.000+00:00",
          "weight": 432,
          "bulkIdentity": "Bulk Waste ID"
        }
      ],
      "discrepancyResidueInfo": {
        "wasteQuantity": false,
        "wasteType": false,
        "residue": false
      },
      "epaWaste": false
    }
  ],
  "additionalInfo": {
    "handlingInstructions": "On the Manifest level. This Manifest is for testing purposes and does not match reality it's more to show what you can do."
  },
  "rejection": false,
  "residue": false,
  "import": false,
  "containsPreviousRejectOrResidue": false,
  "correctionInfo": {
    "active": true
  }
}
```

### Electronic vs Paper Manifest Content

The electronic manifest generally contains the same informaion as its paper counterpart, however there are a few key differences.

#### Physical Space

The electronic manifest is not constrained by the available physical space on a piece of paper.

1. **Waste Codes**: Generators are required to enter up to six (6) waste codes to describe each waste stream. State waste codes that are not redundant with federal codes must be entered here, in addition to the federal waste codes which are most representative of the properties of the waste. For more inforation, see the [Instructions for completing the hazardous waste manifest](https://www.epa.gov/hwgenerators/uniform-hazardous-waste-manifest-instructions-sample-form-and-continuation-sheet). Electronic manifest are not constrained by space, all applicable waste codes can be entered for the applicable waste stream.

2. \*\*

#### Additional Fields

The electronic manifest also contains additional fields that the paper manifest does not. As the e-Manifest continues to be developed, additional fields that benefit the e-Manifest stakeholders and EPA may be added.

#### Status

The status field of electronic manifests is managed by the e-Manifest system, starting with the `NotAssigned` status through `Signed` and beyond if the manifest undergoes post-receipt corrections. Since paper manifests are completed outside the e-Manifest system and uploaded 30 days after the shipment reaches the designated receiving facility, paper manifests can only be assigned a subsect of the availble statuses.

## More Information

For more information on the uniform hazardous waste manifest and updates on the e-Manifest syste, visit
<https://www.epa.gov/e-manifest>

- [The paper manifest](https://www.epa.gov/hwgenerators/hazardous-waste-manifest-system)
  - [Instructions for completing the hazardous waste manifest](https://www.epa.gov/hwgenerators/uniform-hazardous-waste-manifest-instructions-sample-form-and-continuation-sheet)
  - [Paper manifest submission options](https://www.epa.gov/e-manifest/how-submit-hazardous-waste-manifest)
  - [e-Manifest submission Fees](https://www.epa.gov/e-manifest/e-manifest-user-fees-and-payment-information)
- [Terminology](terminology.md)
