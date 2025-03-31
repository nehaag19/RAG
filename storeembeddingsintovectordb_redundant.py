from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import openai

endpoint = "https://diformrecog1401.cognitiveservices.azure.com/"
key = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"



# Set up your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = "https://openai-1401.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-03-15-preview"  # Use the correct API version
openai.api_key = "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6"  # Replace with your Azure OpenAI API key


formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/FORM-60.pdf?sp=r&st=2025-03-25T12:54:16Z&se=2025-03-25T20:54:16Z&spr=https&sv=2024-11-04&sr=b&sig=%2BUHqQRl5WLe6ALyCfaaOnG4Gdm8m2DMWrq3Og3uk34I%3D"
document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl)
)
result = poller.result()

# Extract content from the entire file into a single paragraph
all_text = []
for page in result.pages:
    for line in page.lines:
        all_text.append(line.content)  # Extract the text content of each line

# Join the extracted content into a single paragraph
single_paragraph_text = " ".join(all_text).replace("\n", " ")  # Remove line breaks
print("Extracted Content as Single Paragraph:")
print(single_paragraph_text)

# Initialize Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       # Set the max size of each chunk in characters
    chunk_overlap=15      # Set the overlap between consecutive chunks
)

# Split Text into Chunks
chunks = text_splitter.split_text(single_paragraph_text)

# Output Chunks
print(f"Number of Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")

# Generate embeddings for each chunk
embedding_results = []  # Store embeddings for all chunks

for i, chunk in enumerate(chunks):
    # Generate embeddings for the current chunk
    response = openai.Embedding.create(
        input=chunk,  # Pass a single chunk
        engine="text-embedding-ada-002"  # Replace with your deployed model's name
    )
    embedding = response['data'][0]['embedding']  # Extract embedding from the response
    embedding_results.append(embedding)
    print(f"Generated Embedding for Chunk {i+1}: {embedding}")

# Final embeddings for all chunks
print("All Embeddings Generated:", embedding_results)
