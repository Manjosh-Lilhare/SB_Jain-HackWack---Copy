import os
import sqlite3
import numpy as np
from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the model
model_path = 'models/herbai_custom_model.h5'
if os.path.exists(model_path):
    model = load_model(model_path)
    print("✅ Model loaded successfully!")
else:
    print("❌ Error: Model file not found!")
    model = None

# Automatically get class labels from dataset folder names
dataset_path = "dataset"
if os.path.exists(dataset_path):
    class_labels = sorted(os.listdir(dataset_path))  # Get class names from folder names
    print("✅ Class Labels Loaded:", class_labels)
else:
    class_labels = []
    print("❌ Error: Dataset folder not found!")

print("Total Classes:", len(class_labels))
print(class_labels)

# Define upload folder
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_herb(image_path):
    try:
        # Load and preprocess the image
        img = load_img(image_path, target_size=(224, 224))  
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  

        if model is None:
            return "Error: Model not loaded"

        # Get predictions
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)

        if predicted_class[0] >= len(class_labels):
            return "Error: Predicted class index out of range"

        return class_labels[predicted_class[0]]

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return "Error during prediction"

def get_herb_details(herb_name):
    """Fetch details from the SQLite database based on the predicted herb (case-insensitive)."""
    try:
        db_path = r"C:\Users\lilha\OneDrive\Pictures\Desktop\SB_Jain HackWack - Copy\herbai\DataBase_HerbAi\Project.db"  
        if not os.path.exists(db_path):
            print("❌ Error: Database file not found!")
            return None

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"🔍 Searching for {herb_name} in the database (case-insensitive)...")

        # Use LOWER() function to make the search case-insensitive
        cursor.execute("SELECT * FROM plants WHERE LOWER(predicted_plant) = LOWER(?)", (herb_name,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                "prediction": result[1],
                "bitonic_name": result[2],
                "medicinal_properties": result[3],
                "traditional_uses": result[4],
                "cultural_significance": result[5]
            }
        else:
            print(f"⚠ No data found for {herb_name}")
            return None
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None



@app.route('/')
def index():
    return render_template('new.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"✅ File saved successfully: {filepath}")

        predicted_herb = predict_herb(filepath)
        herb_details = get_herb_details(predicted_herb)

        if herb_details:
            return jsonify(herb_details)
        else:
            return jsonify({"prediction": predicted_herb, "error": "No details found in database"})

    return jsonify({'error': 'Invalid file type'})

@app.route('/search', methods=['GET'])
def search_herb():
    herb_name = request.args.get('herb', '').strip()
    if not herb_name:
        return jsonify({"error": "Please enter a herb name to search."})

    herb_details = get_herb_details(herb_name)

    if herb_details:
        return jsonify(herb_details)
    else:
        return jsonify({"error": "No matching herb found in database."})


if __name__ == '__main__':
    app.run(debug=True)
