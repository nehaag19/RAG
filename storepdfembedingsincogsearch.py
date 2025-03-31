# Import necessary libraries
from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.search.documents import SearchClient
import openai
import uuid  # To generate unique IDs for documents

# ---------------------- CONFIGURATION ---------------------- #

# Document Intelligence API credentials (Azure)
DOCUMENT_INTELLIGENCE_ENDPOINT = "https://diformrecog1401.cognitiveservices.azure.com/"
DOCUMENT_INTELLIGENCE_KEY = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"  # Replace with your key

# Azure OpenAI API credentials
openai.api_type = "azure"
openai.api_base = "https://openai-1401.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-03-15-preview"  # Use the correct API version
openai.api_key = "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6"  # Replace with your Azure OpenAI API key

# Azure Cognitive Search credentials
SEARCH_SERVICE_ENDPOINT = "https://cognitivesearch1401.search.windows.net"
SEARCH_API_KEY = "59XaqX7ke3lF2UmKmEAmw7tRROVezagTtbcxo7MxuPAzSeDVJYHl"   # Replace with your Search API key
INDEX_NAME = "index1401"  # Replace with your index name

# Initialize Search clients
search_client = SearchClient(endpoint=SEARCH_SERVICE_ENDPOINT,
                             index_name=INDEX_NAME,
                             credential=AzureKeyCredential(SEARCH_API_KEY))

document_intelligence_client = DocumentIntelligenceClient(
    endpoint=DOCUMENT_INTELLIGENCE_ENDPOINT,
    credential=AzureKeyCredential(DOCUMENT_INTELLIGENCE_KEY)
)

# ---------------------- DOCUMENT EXTRACTION ---------------------- #

def extract_text_from_document(url):
    """Extract text from a document using Azure Document Intelligence."""
    try:
        # Analyze the document
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", AnalyzeDocumentRequest(url_source=url)
        )
        result = poller.result()

        # Extract content into a single paragraph
        all_text = []
        for page in result.pages:
            for line in page.lines:
                all_text.append(line.content)

        # Join all extracted text into a single paragraph
        single_paragraph_text = " ".join(all_text).replace("\n", " ")  # Remove line breaks
        return single_paragraph_text

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

# ---------------------- TEXT PROCESSING ---------------------- #

def split_text_into_chunks(text, chunk_size=200, chunk_overlap=15):
    """Split extracted text into chunks for embedding."""
#     # Initialize Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Max size of each chunk in characters
        chunk_overlap=chunk_overlap  # Overlap between consecutive chunks
    )

    # Split the text into chunks
    chunks = text_splitter.split_text(text)
    return chunks

# ---------------------- EMBEDDING GENERATION ---------------------- #

def generate_embeddings(chunks):
    """Generate embeddings for each chunk using OpenAI API."""
    embeddings = []  # List to store embeddings for all chunks

    for i, chunk in enumerate(chunks):
        try:
            # Generate embedding for the current chunk
            response = openai.Embedding.create(
                input=chunk,
                engine="text-embedding-ada-002"  # Replace with your deployed model's name
            )
            # Extract the embedding from the response
            embedding = response['data'][0]['embedding']
            embeddings.append(embedding)

            # Print chunk followed by its embedding
            print(f"\nChunk {i + 1}:")
            print(chunk)
            print("\nEmbedding:")
            print(embedding)

        except Exception as e:
            print(f"Error generating embedding for chunk {i}: {e}")
            continue  # Skip this chunk and continue to the next

    # Check if embeddings were successfully generated
    if len(embeddings) == 0:
        raise RuntimeError("No embeddings were successfully generated.")

    return embeddings

# ---------------------- UPLOAD TO COGNITIVE SEARCH ---------------------- #

def upload_chunks_and_embeddings(chunks, embeddings):
    """Upload chunks and their respective embeddings to Azure Cognitive Search."""
    if not chunks or not embeddings:
        raise ValueError("Chunks or embeddings cannot be None or empty.")

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
        try:
            # Create a unique document ID and prepare document
            document = {
                "id": str(uuid.uuid4()),  # Generate a unique ID for each document
                "text_content": chunk,
                "text_content_embeddings": embedding  # Ensure embeddings are arrays
            }
            # Upload the document to Cognitive Search
            result = search_client.upload_documents(documents=[document])
            print(f"Chunk {i} upload succeeded:", result)
            
        except Exception as e:
            print(f"Error uploading chunk {i}: {e}")

# ---------------------- MAIN SCRIPT EXECUTION ---------------------- #

# Set the form URL (replace with your actual form URL)
form_url = "https://mystr1401.blob.core.windows.net/blobcontainer1401/ticket.pdf?sp=r&st=2025-03-26T12:24:24Z&se=2025-04-26T20:24:24Z&spr=https&sv=2024-11-04&sr=b&sig=iitQNHqZfxPRb9cHQS2rbTjShTrL%2FIxYUk6MB1zE9TY%3D"

# Extract text from the document
extracted_text = extract_text_from_document(form_url)
if extracted_text:
    # Split the text into chunks
    chunks = split_text_into_chunks(extracted_text)
    print("Chunks:", chunks)

    # Generate embeddings for the chunks
    try:
        embeddings = generate_embeddings(chunks)
    except RuntimeError as e:
        print(f"Embedding generation failed: {e}")
        embeddings = []  # Fallback to an empty list to prevent further errors

    # Upload the chunks and embeddings to Azure Cognitive Search
    try:
        upload_chunks_and_embeddings(chunks, embeddings)
    except ValueError as e:
        print(f"Upload failed: {e}")
