import os
import magic
import collections

# Check if file exists
def check_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return False
    return True

# Analyze text files
def analyze_text_file(file_path):
    print(f"Analyzing text file: {file_path}")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    words = content.split()
    word_count = len(words)
    line_count = content.count('\n')
    char_count = len(content)

    print(f"Word count: {word_count}")
    print(f"Line count: {line_count}")
    print(f"Character count: {char_count}")
    
    # Most common words
    common_words = collections.Counter(words).most_common(10)
    print("Top 10 most common words:")
    for word, freq in common_words:
        print(f"{word}: {freq}")

# Analyze binary files (hexdump)
def analyze_binary_file(file_path):
    print(f"Analyzing binary file: {file_path}")
    with open(file_path, 'rb') as f:
        hex_content = f.read(64).hex()
    print(f"Hex dump (first 64 bytes): {hex_content}")

# Analyze image files (using Python Imaging Library)
def analyze_image_file(file_path):
    try:
        from PIL import Image
        img = Image.open(file_path)
        print(f"Image size: {img.size}")
        print(f"Image format: {img.format}")
        print(f"Image mode: {img.mode}")
    except ImportError:
        print("PIL (Python Imaging Library) is not installed.")
    except Exception as e:
        print(f"Error analyzing image: {e}")

# Main analysis function
def analyze_file(file_path):
    if not check_file(file_path):
        return

    file_type = magic.from_file(file_path, mime=True)

    if "text" in file_type:
        analyze_text_file(file_path)
    elif "image" in file_type:
        analyze_image_file(file_path)
    elif "binary" in file_type or "octet-stream" in file_type:
        analyze_binary_file(file_path)
    else:
        print(f"Unsupported file type: {file_type}")

# Example Usage
if __name__ == "__main__":
    file_path = input("Enter file path: ")
    analyze_file(file_path)
