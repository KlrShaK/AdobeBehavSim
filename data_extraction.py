# import pandas as pd
# from sklearn.model_selection import train_test_split
# import requests
# import os
# import json
# import re
# from uuid import uuid4

# def load_data(file_path):
#     """Load the dataset from the given Excel file path."""
#     return pd.read_excel(file_path)

# def split_data(df, test_size=0.2):
#     """Split the data into training and validation sets."""
#     train_df, val_df = train_test_split(df, test_size=test_size, random_state=42)
#     return train_df, val_df

# def extract_media_urls(media_string):
#     """Extracts media URLs from the provided string that represents a photo or video object."""
#     urls = []
#     photo_match = re.search(r"Photo\(.*?fullUrl='(.*?)'", media_string)
#     if photo_match:
#         urls.append(photo_match.group(1))
#     video_matches = re.findall(r"VideoVariant\(.*?url='(.*?)',", media_string)
#     if video_matches:
#         urls.extend(video_matches)
#     return urls

# def download_media(media_urls, base_path):
#     """Download media files from URLs and return their unique IDs."""
#     media_ids = []
#     for media_url in media_urls:
#         try:
#             response = requests.get(media_url, timeout=10)
#             if response.status_code == 200:
#                 media_id = str(uuid4())
#                 # Correctly extract the file extension from the URL
#                 # Assuming format is before any query parameters and after the last '.' character
#                 file_extension = media_url.split('?')[0].split('.')[-1]
#                 filename = f"{media_id}.{file_extension}"
#                 # Ensure the filename does not contain any path separators that could create invalid paths
#                 filename = filename.replace('/', '_').replace('\\', '_')
#                 file_path = os.path.join(base_path, filename)
#                 with open(file_path, 'wb') as f:
#                     f.write(response.content)
#                 media_ids.append(media_id)
#         except Exception as e:
#             print(f"Failed to download {media_url}: {e}")
#     return media_ids

# def save_annotations(df, media_dir, annotation_file):
#     """Save annotations in a JSON file, referencing media by unique IDs."""
#     annotations = []
#     for _, row in df.iterrows():
#         if pd.notnull(row['media']):
#             media_urls = extract_media_urls(row['media'])
#             media_ids = download_media(media_urls, media_dir)
#             annotation = row.to_dict()
#             annotation['media'] = media_ids
#             annotations.append(annotation)
    
#     with open(annotation_file, 'w') as f:
#         json.dump(annotations, f, indent=4)

# def create_directories(base_path):
#     """Create required directories for training and validation datasets."""
#     for phase in ['train', 'val']:
#         for sub_dir in ['media', 'annotation']:
#             os.makedirs(os.path.join(base_path, phase, sub_dir), exist_ok=True)

# def preprocess_data(file_path, base_dir):
#     """Main preprocessing function to load data, split, download media, and save annotations."""
#     df = load_data(file_path)
#     train_df, val_df = split_data(df)
    
#     # Setup directories
#     create_directories(base_dir)
    
#     # Process and save training data
#     train_media_dir = os.path.join(base_dir, "train/media")
#     save_annotations(train_df, train_media_dir, os.path.join(base_dir, "train/annotation/annotations.json"))
    
#     # Process and save validation data
#     val_media_dir = os.path.join(base_dir, "val/media")
#     save_annotations(val_df, val_media_dir, os.path.join(base_dir, "val/annotation/annotations.json"))

# # Set the file_path to your Excel file and base_dir to your dataset directory
# file_path = 'behavSimChallSmall.xlsx'
# base_dir = './dataset'

# preprocess_data(file_path, base_dir)
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
import requests
import os
import json
import re
from uuid import uuid4

def load_data(file_path):
    """Load the dataset from the given Excel file path."""
    return pd.read_excel(file_path)

def split_data(df, test_size=0.2):
    """Split the data into training and validation sets."""
    train_df, val_df = train_test_split(df, test_size=test_size, random_state=42)
    return train_df, val_df

def extract_media_urls(media_string):
    """Extracts media URLs from the provided string that represents a photo or video object."""
    urls = []
    photo_match = re.search(r"Photo\(.*?fullUrl='(.*?)'", media_string)
    if photo_match:
        urls.append(photo_match.group(1))
    video_matches = re.findall(r"VideoVariant\(.*?url='(.*?)',", media_string)
    if video_matches:
        urls.extend(video_matches)
    return urls

def download_media(media_urls, base_path, file_id):
    """Download media files from URLs and use the provided file_id as the filename."""
    media_ids = []
    for media_url in media_urls:
        try:
            response = requests.get(media_url, timeout=20)
            if response.status_code == 200:
                # Use the provided file_id directly for the filename, along with the correct file extension
                file_extension = media_url.split('?')[0].split('.')[-1]
                filename = f"{file_id}.{file_extension}"
                # Sanitize the filename to ensure it does not contain any path separators
                filename = filename.replace('/', '_').replace('\\', '_')
                file_path = os.path.join(base_path, filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                media_ids.append(file_id)  # Use file_id instead of generating a new UUID
        except Exception as e:
            print(f"Failed to download {media_url}: {e}")
    return media_ids


def save_annotations(df, media_dir, annotation_file):
    """Save annotations in a JSON file, referencing media by the original ID."""
    annotations = []
    for _, row in df.iterrows():
        if pd.notnull(row['media']):
            media_urls = extract_media_urls(row['media'])
            # Pass row['id'] as the file_id to the download_media function
            media_ids = download_media(media_urls, media_dir, row['id'])
            annotation = row.to_dict()
            annotation['media'] = media_ids  # The media is now referenced by the original ID
            annotations.append(annotation)
    
    with open(annotation_file, 'w') as f:
        json.dump(annotations, f, indent=4)


def create_directories(base_path):
    """Create required directories for training and validation datasets."""
    for phase in ['train', 'val']:
        for sub_dir in ['media', 'annotation']:
            os.makedirs(os.path.join(base_path, phase, sub_dir), exist_ok=True)

def preprocess_data(file_path, base_dir):
    """Main preprocessing function to load data, split, download media, and save annotations."""
    df = load_data(file_path)
    train_df, val_df = split_data(df)
    
    # Setup directories
    create_directories(base_dir)
    
    # Process and save training data
    train_media_dir = os.path.join(base_dir, "train/media")
    save_annotations(train_df, train_media_dir, os.path.join(base_dir, "train/annotation/annotations.json"))
    
    # Process and save validation data
    val_media_dir = os.path.join(base_dir, "val/media")
    save_annotations(val_df, val_media_dir, os.path.join(base_dir, "val/annotation/annotations.json"))

# Set the file_path to your Excel file and base_dir to your dataset directory
# file_path = 'behavSimChallSmall.xlsx'  # Test file
file_path = 'behaviour_content_simulation_train.xlsx'

base_dir = './dataset'

preprocess_data(file_path, base_dir)
# ------------------------------------------------------------------------------------------------------------
