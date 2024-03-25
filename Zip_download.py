import requests
import os
import zipfile
import json

# GitHub API URL for the latest release of cvelistV5
api_url = 'https://api.github.com/repos/CVEProject/cvelistV5/releases/latest'

# Local file to store the tag name of the last downloaded release
last_downloaded_tag_file = 'last_downloaded_tag.txt'

def fetch_latest_release_tag():
    print("Fetching the latest release tag from GitHub...")
    response = requests.get(api_url)
    if response.status_code == 200:
        latest_release_info = response.json()
        print(f"Latest release tag found: {latest_release_info['tag_name']}")
        return latest_release_info['tag_name']
    else:
        print(f"Failed to fetch latest release info, status code: {response.status_code}")
        return None

def is_new_release_available(latest_tag):
    print("Checking if a new release is available...")
    if not os.path.exists(last_downloaded_tag_file):
        print("No record of last download found. Proceeding with download.")
        return True  # No record of last download, so proceed
    with open(last_downloaded_tag_file, 'r') as file:
        last_downloaded_tag = file.read().strip()
        if last_downloaded_tag != latest_tag:
            print("New release available.")
            return True
        else:
            print("No new release since the last download. No action needed.")
            return False

def update_last_downloaded_tag(latest_tag):
    print(f"Updating the last downloaded tag to: {latest_tag}")
    with open(last_downloaded_tag_file, 'w') as file:
        file.write(latest_tag)

def main():
    latest_tag = fetch_latest_release_tag()
    if latest_tag and is_new_release_available(latest_tag):
        # Define the URL for the GitHub zip file (update if needed based on release data)
        zip_url = f'https://github.com/CVEProject/cvelistV5/archive/refs/tags/{latest_tag}.zip'
        zip_file_path = 'cve_data.zip'
        extract_dir = 'cve_data'

        print(f"Downloading the latest CVE data from {zip_url}...")
        response = requests.get(zip_url)
        with open(zip_file_path, 'wb') as file:
            file.write(response.content)
        print("Download complete.")

        print("Extracting the ZIP file...")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print("Extraction complete.")

        # Placeholder for your data processing logic
        # print("Processing the data...")

        # After successful download and processing, update the last downloaded tag
        update_last_downloaded_tag(latest_tag)
        print("Process completed successfully.")
    else:
        print("Exiting. No new data to process.")

if __name__ == "__main__":
    main()
