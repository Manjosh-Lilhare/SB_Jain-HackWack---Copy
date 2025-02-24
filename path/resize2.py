import os
from PIL import Image

# Input and Output folder paths
input_folder = "path/to/input_folder"  # Change this to your input folder path
output_folder = "path/to/output_folder"  # Change this to your output folder path

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Resize dimensions
target_size = (224, 224)

# Traverse through all subdirectories
for root, _, files in os.walk(input_folder):
    for filename in files:
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            img_path = os.path.join(root, filename)
            try:
                # Open and resize the image
                img = Image.open(img_path)
                img = img.resize(target_size, Image.LANCZOS)  # Use LANCZOS for high-quality resizing
                
                # Create the corresponding subfolder inside the output folder
                relative_path = os.path.relpath(root, input_folder)  # Get relative path of subfolder
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)  # Ensure subfolder exists
                
                # Save the processed image in the corresponding subfolder
                img.save(os.path.join(output_subfolder, filename))
                print(f"Processed: {filename} → Saved to {output_subfolder}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

print("Resizing complete!")
