from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import uuid  # To generate unique IDs for documents
import numpy as np  # Optional: Used for creating mock embeddings for demonstr

# Azure Cognitive Search configuration
index_name = "index1401"  # Replace with your index name
# search_endpoint = "https://cognitivesearch1401.search.windows.net"  # Replace with your Azure Search service endpoint
# search_api_key = "59XaqX7ke3lF2UmKmEAmw7tRROVezagTtbcxo7MxuPAzSeDVJYHl"  # Replace with your Azure Search API key

service_endpoint = "https://cognitivesearch1401.search.windows.net"  # Replace with your Azure Search service endpoint
api_key = "59XaqX7ke3lF2UmKmEAmw7tRROVezagTtbcxo7MxuPAzSeDVJYHl"  # Replace with your Azure Search API key

# Initialize SearchClient
search_client = SearchClient(endpoint=service_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))

def generate_mock_embedding(length):
    """Generate a mock embedding of the specified length for demonstration."""
    return list(np.random.rand(length))


def upload_chunks_and_embeddings(chunks, embeddings):
    if len(chunks) != len(embeddings):
        print("Error: The number of chunks and embeddings must match.")
        return
    
    # Upload chunks with their respective embeddings one at a time
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
        document = {
            "id": str(uuid.uuid4()),  # Generate a unique ID for each document
            "text_content": chunk,
            "text_content_embeddings": embedding
        }

        try:
            result = search_client.upload_documents(documents=[document])
            print(f"Chunk {i} upload succeeded:", result)
        except Exception as e:
            print(f"Error uploading chunk {i}:", e)


# Example usage
chunks = ["This is chunk 1.", "This is chunk 2.", "This is chunk 3."]
embeddings = [generate_mock_embedding(1536) for _ in range(len(chunks))] # Example embeddings (vectors)
upload_chunks_and_embeddings(chunks, embeddings)