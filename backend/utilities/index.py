import json
import requests
from dotenv import load_dotenv
from backend.core.config import Config 

load_dotenv()

# Setup the Payloads header
headers = {'Content-Type': 'application/json','api-key': Config.AZURE_SEARCH_KEY}
params = {'api-version': Config.AZURE_SEARCH_API_VERSION}

BLOB_CONTAINER_NAME = Config.BLOB_CONTAINER_NAME

index_payload = {
    
    "name": Config.INDEX_NAME,
    "vectorSearch": {
        "algorithms": [
            {
                "name": "use-hnsw",
                "kind": "hnsw",
            }
        ],
        "compressions": [ # Compression (optional)
            {
                "name": "use-scalar",
                "kind": "scalarQuantization",
                "rescoringOptions": {
                    "enableRescoring": "true",
                    "defaultOversampling": 10,
                    "rescoreStorageMethod": "preserveOriginals"
                },
                "scalarQuantizationParameters": {
                    "quantizedDataType": "int8"
                },
                "truncationDimension": 1024
            },
            {
                "name": "use-binary",
                "kind": "binaryQuantization",
                "rescoringOptions": {
                    "enableRescoring": "true",
                    "defaultOversampling": 10,
                    "rescoreStorageMethod": "preserveOriginals"
                },
                "truncationDimension": 1024
            }
        ],
        
        "vectorizers": [ 
            {
                "name": "use-openai",
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": Config.AZURE_OPENAI_ENDPOINT,
                    "apiKey": Config.AZURE_OPENAI_API_KEY,
                    "deploymentId": Config.EMBEDDING_DEPLOYMENT_NAME,
                    "modelName": Config.EMBEDDING_DEPLOYMENT_NAME
                }
            }
        ],
        "profiles": [
           {
                "name": "vector-profile-hnsw-scalar",
                "compression": "use-scalar", 
                "algorithm": "use-hnsw",
                "vectorizer": "use-openai"
           },
           {
                "name": "vector-profile-hnsw-binary",
                "compression": "use-binary",
                "algorithm": "use-hnsw",
                "vectorizer": "use-openai"
           }
         ]
    },
    "semantic": {
        "configurations": [
            {
                "name": "my-semantic-config",
                "prioritizedFields": {
                    "titleField": {
                        "fieldName": "title"
                    },
                    "prioritizedContentFields": [
                        {
                            "fieldName": "chunk"
                        }
                    ],
                    "prioritizedKeywordsFields": []
                }
            }
        ]
    },
    "fields": [
        {"name": "id", "type": "Edm.String", "key": "true", "analyzer": "keyword", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false","facetable": "false"},
        {"name": "ParentKey", "type": "Edm.String", "searchable": "true", "retrievable": "true", "facetable": "false", "filterable": "true", "sortable": "false"},
        {"name": "title", "type": "Edm.String", "searchable": "true", "retrievable": "true", "facetable": "false", "filterable": "true", "sortable": "false"},
        {"name": "name", "type": "Edm.String", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},
        {"name": "location", "type": "Edm.String", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},   
        {"name": "chunk","type": "Edm.String", "searchable": "true", "retrievable": "true", "sortable": "false", "filterable": "false", "facetable": "false"},
        {
            "name": "chunkVector",
            "type": "Collection(Edm.Half)", 
            "dimensions": 1536, # IMPORTANT: Make sure these dimmensions match your embedding model name
            "vectorSearchProfile": "vector-profile-hnsw-scalar",
            "searchable": "true",
            "retrievable": "false",
            "filterable": "false",
            "sortable": "false",
            "facetable": "false",
            "stored": "false" # Compression (optional)
        }
    ]
}

r = requests.put(Config.AZURE_SEARCH_ENDPOINT + "/indexes/" + Config.INDEX_NAME,
                 data=json.dumps(index_payload), headers=headers, params=params)