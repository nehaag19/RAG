from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

endpoint = "https://diformrecog1401.cognitiveservices.azure.com/"
key = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"

# sample document
# formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/FORM-60.pdf?sp=r&st=2025-03-21T09:14:38Z&se=2025-03-21T17:14:38Z&spr=https&sv=2024-11-04&sr=b&sig=lTkgVA6WXxV2eQ7UISgBeEzl5H%2FoI6UmiKQ19xAuXbo%3D"
# formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/ticket.pdf?sp=r&st=2025-03-25T12:52:04Z&se=2025-03-25T20:52:04Z&spr=https&sv=2024-11-04&sr=b&sig=uCU07g3I0836r61VOBKGWggsVCZypWA1qLXiyFTCzyw%3D"
# formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/FORM-60.pdf?sp=r&st=2025-03-25T12:54:16Z&se=2025-03-25T20:54:16Z&spr=https&sv=2024-11-04&sr=b&sig=%2BUHqQRl5WLe6ALyCfaaOnG4Gdm8m2DMWrq3Og3uk34I%3D"
formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/ticket.pdf?sp=r&st=2025-03-26T12:24:24Z&se=2025-04-26T20:24:24Z&spr=https&sv=2024-11-04&sr=b&sig=iitQNHqZfxPRb9cHQS2rbTjShTrL%2FIxYUk6MB1zE9TY%3D"

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
    chunk_overlap=20      # Set the overlap between consecutive chunks
)

# Split Text into Chunks
chunks = text_splitter.split_text(single_paragraph_text)

# Output Chunks
print(f"Number of Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")

