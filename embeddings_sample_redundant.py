# import os
# from openai import AzureOpenAI

# api_key= "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6",  # Replace with your Azure OpenAI endpoint
# api_version = "2021-04-30",  # Ensure this is the correct API version
# azure_endpoint= os.getenv("https://openai-1401.openai.azure.com/")

# # # Set up Azure OpenAI credentials
# client = AzureOpenAI(azure_endpoint,api_key,api_version) # Replace with your API key from Azure Portal

import openai

# Set up your Azure OpenAI credentials
openai.api_type = "azure"
openai.api_base = "https://openai-1401.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-03-15-preview"  # Use the correct API version
openai.api_key = "CQsnmPhwDMX7BPDaI3U3kfY7tyDeqV91G7ZWC6yHM6WjzzVQ8B9FJQQJ99BCACYeBjFXJ3w3AAABACOG5te6"  # Replace with your Azure OpenAI API key

# Define the text for which you want to generate embeddings
input_text= "This is the text for which I want to generate embeddings."

# Call the Azure OpenAI API to generate embeddings
response = client.embeddings.create(
    input=input_text,
    engine="text-embedding-ada-002"  # Replace with your deployed model's name
)

# Extract embeddings from the response
embeddings = response['data'][0]['embedding']
print("Embeddings:", embeddings)
# input_text

