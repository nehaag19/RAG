from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Configuration
service_endpoint = "https://cognitivesearch1401.search.windows.net"  # Replace with your Azure Cognitive Search service endpoint
api_key = "59XaqX7ke3lF2UmKmEAmw7tRROVezagTtbcxo7MxuPAzSeDVJYHl"  # Replace with your Azure Cognitive Search admin API key
index_name = "index1401"

# Initialize SearchClient
search_client = SearchClient(endpoint=service_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))

def upload_chunks_and_embeddings(chunks, embeddings):
    if len(chunks) != len(embeddings):
        print("Error: The number of chunks and embeddings must match.")
        return
    
    # Upload chunks with their respective embeddings one at a time
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
        document = {
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
embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]  # Example embeddings (vectors)
upload_chunks_and_embeddings(chunks, embeddings)