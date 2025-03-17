import json
import requests
from dotenv import load_dotenv
from backend.core.config import Config 

load_dotenv()

# Setup the Payloads header
headers = {'Content-Type': 'application/json','api-key': Config.AZURE_SEARCH_KEY}
params = {'api-version': Config.AZURE_SEARCH_API_VERSION}

BLOB_CONTAINER_NAME = Config.BLOB_CONTAINER_NAME

skillset_payload = {
    "name": Config.SKILLSET_NAME,
    "description": "e2e Skillset for RAG - Files",
    "skills":
    [
        {
            "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
            "description": "Extract text (plain and structured) from image.",
            "context": "/document/normalized_images/*",
            "defaultLanguageCode": "en",
            "detectOrientation": True,
            "inputs": [
                {
                  "name": "image",
                  "source": "/document/normalized_images/*"
                }
            ],
                "outputs": [
                {
                  "name": "text",
                  "targetName" : "images_text"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.MergeSkill",
            "description": "Create merged_text, which includes all the textual representation of each image inserted at the right location in the content field. This is useful for PDF and other file formats that supported embedded images.",
            "context": "/document",
            "insertPreTag": " ",
            "insertPostTag": " ",
            "inputs": [
                {
                  "name":"text", "source": "/document/content"
                },
                {
                  "name": "itemsToInsert", "source": "/document/normalized_images/*/images_text"
                },
                {
                  "name":"offsets", "source": "/document/normalized_images/*/contentOffset"
                }
            ],
            "outputs": [
                {
                  "name": "mergedText", 
                  "targetName" : "merged_text"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
            "context": "/document",
            "textSplitMode": "pages",  # although it says "pages" it actally means chunks, not actual pages
            "maximumPageLength": 5000, # 5000 characters is default and a good choice
            "pageOverlapLength": 750,  # 15% overlap among chunks
            "defaultLanguageCode": "en",
            "inputs": [
                {
                    "name": "text",
                    "source": "/document/merged_text"
                }
            ],
            "outputs": [
                {
                    "name": "textItems",
                    "targetName": "chunks"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
            "description": "Azure OpenAI Embedding Skill",
            "context": "/document/chunks/*",
            "resourceUri": Config.AZURE_OPENAI_ENDPOINT,
            "apiKey": Config.AZURE_OPENAI_API_KEY,
            "deploymentId": Config.EMBEDDING_DEPLOYMENT_NAME,
            "modelName": Config.EMBEDDING_DEPLOYMENT_NAME,
            "inputs": [
                {
                    "name": "text",
                    "source": "/document/chunks/*"
                }
            ],
            "outputs": [
                {
                    "name": "embedding",
                    "targetName": "vector"
                }
            ]
        }
    ],
    "indexProjections": {
        "selectors": [
            {
                "targetIndexName": Config.INDEX_NAME,
                "parentKeyFieldName": "ParentKey",
                "sourceContext": "/document/chunks/*",
                "mappings": [
                    {
                        "name": "title",
                        "source": "/document/title"
                    },
                    {
                        "name": "name",
                        "source": "/document/name"
                    },
                    {
                        "name": "location",
                        "source": "/document/location"
                    },
                    {
                        "name": "chunk",
                        "source": "/document/chunks/*"
                    },
                    {
                        "name": "chunkVector",
                        "source": "/document/chunks/*/vector"
                    }
                ]
            }
        ],
        "parameters": {
            "projectionMode": "skipIndexingParentDocuments"
        },
        "cognitiveServices": {
        "@odata.type": "#Microsoft.Azure.Search.CognitiveServicesByKey",
        "description": Config.COG_SERVICE_NAME,
        "key": Config.COG_SERVICES_KEY
    }
    }
}

r = requests.put(Config.AZURE_SEARCH_ENDPOINT + "/skillsets/" + Config.SKILLSET_NAME,
                 data=json.dumps(skillset_payload), headers=headers, params=params)