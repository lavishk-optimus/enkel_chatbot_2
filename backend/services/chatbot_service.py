import re
from langgraph.graph.graph import Graph


from openai import AzureOpenAI
import requests
from backend.core.config import Config


search_headers = {
    "Content-Type": "application/json",
    "api-key": Config.AZURE_SEARCH_KEY
}
search_params = {"api-version": Config.AZURE_SEARCH_API_VERSION}

openai_client = AzureOpenAI(
    api_key=Config.AZURE_OPENAI_API_KEY,
    api_version="2024-02-01",
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
)

openai_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Config.AZURE_OPENAI_API_KEY}"
}


def generate_embedding(text):
    """Generate embeddings using Azure OpenAI"""
    client = AzureOpenAI(
        api_key=Config.AZURE_OPENAI_API_KEY,
        api_version="2024-02-01",
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
    )

    response = client.embeddings.create(
        input=text,
        model=Config.EMBEDDING_DEPLOYMENT_NAME
    )

    if response and response.data:
        return response.data[0].embedding
    else:
        print("Embedding generation failed.")
        return None


def query_cognitive_search(query_vector, threshold=0.7):
    """Retrieve relevant documents and filter by score"""
    url = f"{Config.AZURE_SEARCH_ENDPOINT}/indexes/{Config.INDEX_NAME}/docs/search?api-version=2024-11-01-Preview"
    
    search_payload = {
        "search": "*", 
        "vectorQueries": [
            {
                "kind": "vector", 
                "vector": query_vector,  
                "k": 5,  
                "fields": "chunkVector"  
            }
        ],
        "select": "title,chunk,score",  # Add score to the response
        "queryType": "semantic",
        "semanticConfiguration": "my-semantic-config"
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": Config.AZURE_SEARCH_KEY
    }

    response = requests.post(url, json=search_payload, headers=headers)

    if response.status_code == 200:
        documents = response.json().get("value", [])
        # Filter documents by score threshold
        filtered_documents = [doc for doc in documents if doc.get('score', 0) >= threshold]
        return filtered_documents
    else:
        print(f"Search request failed: {response.text}")
        return []


def vendor_normalization(documents):
    """
    Normalize vendor names across documents by identifying and standardizing variations.
    Example: "OptimusInc", "Optimusinfo" -> "Optimus"
    """
    vendor_name_mapping = {
        "OptimusInc": "Optimus",
        "Optimusinfo": "Optimus",
        # Add more mappings or logic here as needed
    }

    for doc in documents:
        for key, value in vendor_name_mapping.items():
            doc['chunk'] = doc['chunk'].replace(key, value)
    return documents


def generate_llm_response(query, documents):
    """Use Azure OpenAI to generate a response based on retrieved documents"""
    if not documents:
        return "I couldn't find relevant information."

    context = "\n".join([f"{doc['title']}: {doc['chunk']}" for doc in documents])
    
    if "expense" in query.lower() or "invoice" in query.lower():
        prompt = f"""
        You are a financial AI assistant. Analyze the given invoice details and determine the expense category and tax implications.

        Context:
        {context}

        Question: {query}

        - Identify the probable category of the expense.
        - Determine its tax treatment.
        - Provide confidence levels and supporting evidence.
        - If no relevant data is found, reply: "I couldn't find relevant information."

        Answer:
        """

    elif "vendor" in query.lower() or "supplier" in query.lower():
        prompt = f"""
        You are a financial AI assistant. Identify inconsistently named vendors and suggest standardizations.

        Context:
        {context}

        Question: {query}

        - Detect duplicate vendors (e.g., 'Optimus', 'Optimus Inc', 'Optimusinfo') and suggest standard names.
        - Provide confidence scores for matches.
        - If no relevant data is found, reply: "I couldn't find relevant information."

        Answer:
        """

    else:
        prompt = f"""
        You are an AI assistant. Answer the question strictly based on the provided context:

        Context:
        {context}

        Question: {query}

        If the question is unrelated to the provided context, reply: "I couldn't find relevant information."

        Answer:
        """

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a financial AI assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content


def handle_query(user_query, threshold=0.7):
    """Generate embedding & retrieve relevant documents with score filtering"""
    query_vector = generate_embedding(user_query)  
    if not query_vector:
        return {"error": "Embedding generation failed."}

    documents = query_cognitive_search(query_vector, threshold)  # Get documents with score filtering
    if not documents:
        return {"answer": "I couldn't find relevant information. Please try again."}

    documents = vendor_normalization(documents)  # Normalize vendor names
    return documents
