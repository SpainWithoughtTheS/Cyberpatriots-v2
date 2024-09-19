import os

def search_files():
    print("Choose the type of file you want to search for:")
    print("1. mp3")
    print("2. png")
    print("3. mp4")
    print("4. jpeg")
    print("5. jpg")
    print("6. webp")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        filetype = "mp3"
    elif choice == '2':
        filetype = "png"
    elif choice == '3':
        filetype = "mp4"
    elif choice == '4':
        filetype = "jpeg"
    elif choice == '5':
        filetype = "jpg"
    elif choice == '6':
        filetype = "webp"
    else:
        print("Invalid choice")
        return
    
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(f".{filetype}"):
                print(os.path.join(root, file))

if __name__ == "__main__":
    search_files()
