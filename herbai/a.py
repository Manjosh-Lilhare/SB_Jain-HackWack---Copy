import os

def get_folder_names(path=r"C:\Users\lilha\OneDrive\Pictures\Desktop\SB_Jain HackWack - Copy\herbai\dataset"):
    """
    Returns a list of folder names within the specified path.

    Args:
        path (str): The path to the directory to scan. Defaults to the current directory.

    Returns:
        list: A list of folder names.
    """
    folder_names = []
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                folder_names.append(item)
        return folder_names
    except FileNotFoundError:
        print(f"Error: Path '{path}' not found.")
        return []
    except PermissionError:
        print(f"Error: Permission denied accessing '{path}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Example usage:
current_folders = get_folder_names()  # Get folders in the current directory
print("Folders in the current directory:", current_folders)

specific_folders = get_folder_names("/path/to/your/directory") #Or a specific path
print("Folders in the specific directory:", specific_folders)

#Example with an error:
non_existent_path_folders = get_folder_names("/this/path/does/not/exist")
print("Folders in a non-existent directory:", non_existent_path_folders)

#Example with a subfolder.
if len(current_folders) > 0:
    first_folder = current_folders[0]
    subfolders = get_folder_names(first_folder)
    print(f"Subfolders of {first_folder}:", subfolders)