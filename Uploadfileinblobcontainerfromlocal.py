from azure.storage.blob import BlobServiceClient

def upload_file_to_blob(storage_account_name, container_name, storage_account_key, file_path, blob_name):
    try:
        # Step 1: Construct the Blob Service Client
        connect_str = "DefaultEndpointsProtocol=https;AccountName=mystr1401;AccountKey=KvMNYTwjyNFhVJLkNeimYtrTcno5KyOQb+9SQpHid7HN32xlWp+p8YXJzZ/B5Em5f5NNMdvd2Z8U+AStQFn+EQ==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Step 2: Get a Client for the Container
        container_client = blob_service_client.get_container_client(container_name)

        # Step 3: Upload the File
        with open(file_path, "rb") as file_data:
            container_client.upload_blob(name=blob_name, data=file_data, overwrite=True)
        
        print(f"File '{file_path}' uploaded to Blob Storage as '{blob_name}'.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage
if __name__ == "__main__":
    # Replace these values with your Azure Blob Storage details
    storage_account_name = "mystr1401"
    container_name = "blobcontainer1401"
    storage_account_key = "KvMNYTwjyNFhVJLkNeimYtrTcno5KyOQb+9SQpHid7HN32xlWp+p8YXJzZ/B5Em5f5NNMdvd2Z8U+AStQFn+EQ=="  # Get this from Azure Portal
    file_path = "C:/Users/sumit/Desktop/mydata/boston_housing.csv"  # Local file path
    blob_name = "Boston Housing"

    upload_file_to_blob(storage_account_name, container_name, storage_account_key, file_path, blob_name)
