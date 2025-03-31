
import openai
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest


endpoint = "https://diformrecog1401.cognitiveservices.azure.com/"
key = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"

# sample document
# formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/FORM-60.pdf?sp=r&st=2025-03-21T09:14:38Z&se=2025-03-21T17:14:38Z&spr=https&sv=2024-11-04&sr=b&sig=lTkgVA6WXxV2eQ7UISgBeEzl5H%2FoI6UmiKQ19xAuXbo%3D"
formUrl = "https://mystr1401.blob.core.windows.net/blobcontainer1401/ticket.pdf?sp=r&st=2025-03-25T06:59:23Z&se=2025-04-30T14:59:23Z&spr=https&sv=2024-11-04&sr=b&sig=D3fWhcxxmpEQ%2BEcn8emMq4p3UBlIQ%2B5bPfbEAP6eKX0%3D"
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
print("Extracted Content is as follows in Paragraph:")
print(single_paragraph_text)




# Set up your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = "https://openai-1401.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-03-15-preview"  # Use the correct API version
openai.api_key = "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6"  # Replace with your Azure OpenAI API key

# Call the Azure OpenAI API to generate embeddings
response = openai.Embedding.create(
    input=single_paragraph_text,
    engine="text-embedding-ada-002"  # Replace with your deployed model's name
)

# Extract embeddings from the response
embeddings = response['data'][0]['embedding']
print("Embeddings:", embeddings)
