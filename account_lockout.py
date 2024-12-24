import os

def modify_common_auth():
    file_path = "/etc/pam.d/common-auth"
    temp_file_path = file_path + ".tmp"

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, "r") as original_file, open(temp_file_path, "w") as temp_file:
            for line in original_file:
                # If the line contains 'pam_tally2.so', add the required options
                if "pam_tally2.so" in line and "deny=" not in line:
                    line = line.strip() + " deny=5 unlock_time=1800\n"
                temp_file.write(line)

        # Replace the original file with the modified one
        os.replace(temp_file_path, file_path)
        print(f"Modified {file_path} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Cleanup the temp file in case of an error
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    modify_common_auth()
