import httpx
import glob
import os

def upload_file(api_url, local_file_path, destination_folder):
    # Extract the filename from the local file path
    filename = os.path.basename(local_file_path)

    # Construct the URL for the upload endpoint
    upload_url = f"{api_url}/uploads/{destination_folder}/{filename}"

    # Read the file content
    with open(local_file_path, 'rb') as file:
        file_content = file.read()

    # Make a POST request to get the presigned URL
    response = httpx.put(upload_url)
    print(response.status_code)
    
    # Check if the request was successful
    if response.status_code != 307:
        raise Exception(f"Failed to get presigned URL: {response.text}")

    # Extract the presigned URL from the response
    presigned_url = response.headers.get('Location')
    if not presigned_url:
        raise Exception("Presigned URL not found in the response")

    # Upload the file to the presigned URL
    upload_response = httpx.put(presigned_url, content=file_content)

    # Check if the upload was successful
    if upload_response.status_code != 200:
        raise Exception(f"Failed to upload file: {upload_response.text}")

    print(f"File {filename} uploaded successfully to {destination_folder}")


def process_file(api_url, local_file_path, destination_folder):
    # Extract the filename from the local file path
    filename = os.path.basename(local_file_path)

    # Construct the URL for the upload endpoint
    process_url = f"{api_url}/process/{destination_folder}/{filename}"

    # Make a POST request to get the presigned URL
    response = httpx.post(process_url)
    print(response.status_code)
    
if __name__=="__main__":
    api_url = os.environ["BACKEND_URL"]
    
    # Loop through all files in 'files/' directory and its subdirectories
    for file_path in glob.glob('files/**/*', recursive=True):
        # Check if the path is a file and not a directory
        if os.path.isfile(file_path):
            # Extracting folder name and file name
            folder_name = os.path.basename(os.path.dirname(file_path))
            file_name = os.path.basename(file_path)
            if not (file_name.endswith(".txt") or file_name.endswith(".md")):
                continue
            print(f"Folder: {folder_name}, File: {file_name}")
            upload_file(api_url, f"./files/{folder_name}/{file_name}", folder_name)
            process_file(api_url, f"./files/{folder_name}/{file_name}", folder_name)