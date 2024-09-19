import os

# List of media file extensions to search for
MEDIA_EXTENSIONS = ['.mp3', '.mp4', '.wav', '.flac', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.mkv', '.avi', '.mov']

def find_media_files(directory):
    media_files = []

    # Walk through all directories and files in the specified path
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has one of the media extensions
            if any(file.lower().endswith(ext) for ext in MEDIA_EXTENSIONS):
                media_files.append(os.path.join(root, file))
    
    return media_files

# Replace with the directory you want to search
search_directory = '/home/username'

media_files = find_media_files(search_directory)

if media_files:
    print("Media files found:")
    for media_file in media_files:
        print(media_file)
else:
    print("No media files found.")
