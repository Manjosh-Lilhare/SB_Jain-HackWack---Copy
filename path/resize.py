import os
from PIL import Image

# Input and Output folders
input_folder = "path/to/input_folder"  # Change this to your folder path
output_folder = "path/to/output_folder"  # Change this to your folder path

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Resize dimensions
target_size = (224, 224)

# Process images
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        img_path = os.path.join(input_folder, filename)
        try:
            img = Image.open(img_path)
            img = img.resize(target_size, Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
            img.save(os.path.join(output_folder, filename))
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("Resizing complete!")
