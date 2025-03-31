from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

# Azure Storage configurations
connection_string = "DefaultEndpointsProtocol=https;AccountName=mystr1401;AccountKey=KvMNYTwjyNFhVJLkNeimYtrTcno5KyOQb+9SQpHid7HN32xlWp+p8YXJzZ/B5Em5f5NNMdvd2Z8U+AStQFn+EQ==;EndpointSuffix=core.windows.net"

source_container_name = "blobcontainer1401"  # Replace with the source container name
source_blob_name = "FORM-60.pdf"  # Replace with the name of the existing file in the source blob
destination_container_name = "blobcontainer1401"  # Replace with the destination container name
destination_blob_name = "new-file.txt"  # Name for the new file in the destination blob

try:
    # Step 1: Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Step 2: Read the file from the source blob
    source_blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
    downloaded_blob = source_blob_client.download_blob()
    content = downloaded_blob.readall()  # Reads the entire content as binary
    print(content)  # Output will be in binary format

    print(downloaded_blob)
    extracted_content = downloaded_blob.content_as_text(encoding="UTF-8")
    print(extracted_content)
     #.decode("utf-8")  # Extracted content as a string
    print(f"Data successfully read from source blob '{source_blob_name}'.")

    # Step 3: Save the extracted content into a local file
    local_file_name = "temp_extracted_data.txt"
    with open(local_file_name, "w", encoding="utf-8") as file:
        file.write(extracted_content)
    print(f"Extracted content saved to local file: {local_file_name}")

    # Step 4: Upload the new file to the destination blob
    destination_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)

    # Ensure the destination container exists
    destination_container_client = blob_service_client.get_container_client(destination_container_name)
    if not destination_container_client.exists():
        destination_container_client.create_container()
        print(f"Created new container: {destination_container_name}")

    # Upload the file
    with open(local_file_name, "rb") as data:
        destination_blob_client.upload_blob(data, overwrite=True)
    print(f"New file '{destination_blob_name}' successfully uploaded to container '{destination_container_name}'.")

except Exception as e:
    print(f"An error occurred: {e}")