import json
import requests
from dotenv import load_dotenv
from backend.core.config import Config 

load_dotenv()

# Setup the Payloads header
headers = {'Content-Type': 'application/json','api-key': Config.AZURE_SEARCH_KEY}
params = {'api-version': Config.AZURE_SEARCH_API_VERSION}

BLOB_CONTAINER_NAME = Config.BLOB_CONTAINER_NAME

datasource_payload = {
    "name": Config.DATASOURCE_NAME,
    "description": "Demo files to demonstrate ai search capabilities.",
    "type": "azureblob",
    "credentials": {
        "connectionString": Config.BLOB_CONNECTION_STRING
    },
    "dataDeletionDetectionPolicy" : {
        "@odata.type" :"#Microsoft.Azure.Search.NativeBlobSoftDeleteDeletionDetectionPolicy" 
    },
    "container": {
        "name": BLOB_CONTAINER_NAME
    }
}
r = requests.put(Config.AZURE_SEARCH_ENDPOINT+ "/datasources/" + Config.DATASOURCE_NAME,
                 data=json.dumps(datasource_payload), headers=headers, params=params)
