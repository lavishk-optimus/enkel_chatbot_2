import json
import requests
from dotenv import load_dotenv
from backend.core.config import Config 

load_dotenv()

# Setup the Payloads header
headers = {'Content-Type': 'application/json','api-key': Config.AZURE_SEARCH_KEY}
params = {'api-version': Config.AZURE_SEARCH_API_VERSION}

BLOB_CONTAINER_NAME = Config.BLOB_CONTAINER_NAME

indexer_payload = {
    "name": Config.INDEXER_NAME,
    "dataSourceName": Config.DATASOURCE_NAME,
    "targetIndexName": Config.INDEX_NAME,
    "skillsetName": Config.SKILLSET_NAME,
    "schedule" : { "interval" : "PT30M"}, 
    "fieldMappings": [
        {
          "sourceFieldName" : "metadata_title",
          "targetFieldName" : "title"
        },
        {
          "sourceFieldName" : "metadata_storage_name",
          "targetFieldName" : "name"
        },
        {
          "sourceFieldName" : "metadata_storage_path",
          "targetFieldName" : "location"
        }
    ],
    "outputFieldMappings":[],
    "parameters":
    {
        "maxFailedItems": -1,
        "maxFailedItemsPerBatch": -1,
        "configuration":
        {
            "dataToExtract": "contentAndMetadata",
            "imageAction": "generateNormalizedImages"
        }
    }
}

r = requests.put(Config.AZURE_SEARCH_ENDPOINT + "/indexers/" + Config.INDEXER_NAME,
                 data=json.dumps(indexer_payload), headers=headers, params=params)