from azure.cosmos import CosmosClient

from dotenv import load_dotenv
import os

# Load environment variables from the .env file (if present)
load_dotenv()

# Cosmos DB Configuration
COSMOS_ENDPOINT=os.getenv('COSMOS_ENDPOINT')
COSMOS_KEY=os.getenv('COSMOS_KEY')
DATABASE_NAME=os.getenv('DATABASE_NAME')
CONTAINER_NAME=os.getenv('CONTAINER_NAME')

# Initialize the Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def fetch_documents_by_user_id(user_id):
    """Fetch all documents for a specific user_id."""
    query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"
    documents = list(container.query_items(query=query, enable_cross_partition_query=True))
    return documents

# Example Usage
user_id = "1"
documents = fetch_documents_by_user_id(user_id)

if documents:
    print(f"Found {len(documents)} documents for user_id {user_id}:")
    for doc in documents:
        print("question: ",doc['question'])
        print("answer: ",doc['question'])
else:
    print(f"No documents found for user_id {user_id}")
