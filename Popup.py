import json
import os

def block_chrome_popups():
    prefs_path = os.path.expanduser("~/.config/google-chrome/Default/Preferences")

    if os.path.exists(prefs_path):
        try:
            with open(prefs_path, 'r') as file:
                prefs_data = json.load(file)

            prefs_data.setdefault("profile", {}).setdefault("default_content_setting_values", {})["popups"] = 2

            with open(prefs_path, 'w') as file:
                json.dump(prefs_data, file, indent=4)

            print("Pop-up blocking has been enabled in Chrome.")
        except (json.JSONDecodeError, IOError) as e:
            print(f"An error occurred: {e}")
    else:
        print("Preferences file not found. Make sure Chrome is installed and has been run at least once.")


if __name__ == "__main__":
    block_chrome_popups()
