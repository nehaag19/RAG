from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchFieldDataType
import openai
import uuid  # To generate unique IDs for documents

# Document Intelligence API credentials
endpoint = "https://diformrecog1401.cognitiveservices.azure.com/"
key = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"

# Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_base = "https://openai-1401.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-03-15-preview"  # Use the correct API version
openai.api_key = "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6"  # Replace with your Azure OpenAI API key

# Azure Cognitive Search credentials
service_endpoint = "https://cognitivesearch1401.search.windows.net"  # Replace with your Azure Search service endpoint
api_key = "59XaqX7ke3lF2UmKmEAmw7tRROVezagTtbcxo7MxuPAzSeDVJYHl"  # Replace with your Azure Search API key
index_name = "index1401"  # Replace with your index name


# Initialize SearchClient
search_client = SearchClient(endpoint=service_endpoint,
                             index_name=index_name,
                             credential=AzureKeyCredential(api_key))

# Initialize Document Intelligence Client
document_intelligence_client = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Analyze the document
form_url = "https://mystr1401.blob.core.windows.net/blobcontainer1401/FORM-60.pdf?sp=r&st=2025-03-26T05:06:14Z&se=2025-05-26T13:06:14Z&spr=https&sv=2024-11-04&sr=b&sig=QLoukhg1ZQPyx7oRmGUyPRh0SLle4Sk8JkVw6tQN4Zs%3D"
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout", AnalyzeDocumentRequest(url_source=form_url)
)
result = poller.result()

# Extract content into a single paragraph
all_text = []
for page in result.pages:
    for line in page.lines:
        all_text.append(line.content)

single_paragraph_text = " ".join(all_text).replace("\n", " ")  # Remove line breaks

# Initialize Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # Max size of each chunk in characters
    chunk_overlap=15  # Overlap between consecutive chunks
)


# Split Text into Chunks
chunks = text_splitter.split_text(single_paragraph_text)
print("Chunks:", chunks)

# def upload_chunks_and_embeddings(chunks):
#     embeddings = []  # List to store embeddings for all chunks


# def upload_chunks_and_embeddings(chunks, embedding):
#     if len(ch  raise RuntimeError("Failed to generate embeddings for all chunks. Please check the OpenAI API response.")

#     return embeddingunks) != len(embedding):
#         print("Error: The number of chunks and embeddings must match.")
#         return


def generate_embeddings(chunks):
    embeddings = []  # List to store embeddings for all chunks


# Generate embeddings and store in Azure Cognitive Search
    for i, chunk in enumerate(chunks):
        try:
    # Generate embedding for the current chunk
            response = openai.Embedding.create(
                input=chunk,
                engine="text-embedding-ada-002"  # Replace with your deployed model's name
        )
            Embeddings = response['data'][0]['embeddings']  # Extract embedding from the response
            Embedding.append(embeddings)

        except Exception as e:
            print(f"Error generating embedding for chunk {i}: {e}")
            continue

    if len(embeddings) == 0:
        raise RuntimeError("No embeddings were successfully generated.")

    return embeddings

#  # Validate embedding format
#     if not isinstance(embedding, list) or len(embedding) != 1536:
#                 raise ValueError(f"Invalid embedding for chunk {i}. Expected an array of length 1536.")

#             embedding.append(embedding)
#     except Exception, e:
#             # Log the error and skip to the next chunk
#             print(f"Error generating embedding for chunk {i}: {e}")
#             continue

#     # Ensure embeddings list is not empty
#     if not embedding:
      

    # Attempt to append the embedding directly, allowing exceptions to handle issues
    

    # If no embeddings are successfully generated, raise an exception

# Generate embeddings for chunks
try:
    embedding = generate_embeddings(chunks)
except RuntimeError as e:
    print(f"Embedding generation failed: {e}")
    embeddings = []  # Fallback to an empty list to prevent further errors

def upload_chunks_and_embeddings(chunks, embedding):
    if not chunks or not embeddings:
        raise ValueError("Chunks or embeddings cannot be None or empty.")
    
    # Upload chunks with their respective embeddings
    for i, (chunk, embeddings) in enumerate(zip(chunks, embeddings), start=1):
        try:
            document = {
                "id": str(uuid.uuid4()),  # Generate a unique ID for each document
                "text_content": chunk,
                "text_content_embeddings": embeddings  # Ensure embeddings are arrays
            }
            result = search_client.upload_documents(documents=[document])
            print(f"Chunk {i} upload succeeded:", result)
        except Exception as e:
            print(f"Error uploading chunk {i}: {e}")



# Upload the chunks and embeddings
try:
    upload_chunks_and_embeddings(chunks, embeddings)
except ValueError as e:
    print(f"Upload failed: {e}")

