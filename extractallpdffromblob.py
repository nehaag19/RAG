from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
# from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime, timedelta

# Step 1: Connect to Azure Blob Storage
def connect_to_blob_storage(connection_string, container_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    return container_client

# Step 2: Generate a SAS URL for a Blob
def generate_sas_url(blob_name, account_name, account_key, container_name):
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # SAS valid for 1 hour
    )
    return f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

# Step 3: Analyze a PDF using Document Intelligence
def analyze_pdf(sas_url, endpoint, api_key):
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))
    poller = client.begin_analyze_document_from_url("prebuilt-document", document_url=sas_url)
    result = poller.result()

    
    # Extract text content from the document
    extracted_text = []
    for page in result.pages:
        for line in page.lines:
            extracted_text.append(line.content)
    return " ".join(extracted_text).replace("\n", " ")  # Return text as a single paragraph

# Step 4: Process All PDFs in the Blob Container
def process_pdfs_in_blob(container_client, account_name, account_key, endpoint, api_key):
    for blob in container_client.list_blobs():
        if blob.name.endswith(".pdf"):  # Filter only PDFs
            print(f"Processing PDF: {blob.name}")

            # Generate SAS URL for the PDF
            sas_url = generate_sas_url(blob.name, account_name, account_key, container_client.container_name)

            # Analyze and print the content
            try:
                text_content = analyze_pdf(sas_url, endpoint, api_key)
                print(f"\nContent of {blob.name}:\n{text_content}\n")
            except Exception as e:
                print(f"Failed to process {blob.name}: {e}")
        else:
            print(f"Ignoring non-PDF file: {blob.name}")

# Step 5: Main Function
def main():
    # Azure Blob Storage details
    connection_string = "DefaultEndpointsProtocol=https;AccountName=mystr1401;AccountKey=KvMNYTwjyNFhVJLkNeimYtrTcno5KyOQb+9SQpHid7HN32xlWp+p8YXJzZ/B5Em5f5NNMdvd2Z8U+AStQFn+EQ==;EndpointSuffix=core.windows.net" # Replace with your Blob Storage connection string
    container_name = "blobcontainer1401" # Replace with your Blob container name
    account_name = "mystr1401"  # Replace with your Azure storage account name
    account_key = "KvMNYTwjyNFhVJLkNeimYtrTcno5KyOQb+9SQpHid7HN32xlWp+p8YXJzZ/B5Em5f5NNMdvd2Z8U+AStQFn+EQ=="  # Replace with your Azure storage account key

    # Azure Document Intelligence (Form Recognizer) details
    endpoint = "https://diformrecog1401.cognitiveservices.azure.com/"
    api_key = "5N6sRxB6wUJ1GNZyZFB35lepABsFOGCP0GjIcLQO6xpiwTvkiMkXJQQJ99BCACYeBjFXJ3w3AAALACOGJ6eM"

    # Connect to the Blob Storage container
    container_client = connect_to_blob_storage(connection_string, container_name)

    # Process and print PDFs
    process_pdfs_in_blob(container_client, account_name, account_key, endpoint, api_key)

if __name__ == "__main__":
    main()

