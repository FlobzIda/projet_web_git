from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import os
import uuid
import json
import xgboost as xgb
from sklearn.metrics import accuracy_score, mean_squared_error
import matplotlib.pyplot as plt


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

data = {}

USERS_FILES_JSON = 'users_files.json'

def save_file_mapping(original_filename, new_filename):
    file_mappings = {}
    
    if os.path.exists(USERS_FILES_JSON) and os.path.getsize(USERS_FILES_JSON) > 0:
        try:
            with open(USERS_FILES_JSON, 'r') as f:
                file_mappings = json.load(f)
        except json.JSONDecodeError:
            file_mappings = {}
    
    file_mappings[original_filename] = new_filename
    
    with open(USERS_FILES_JSON, 'w') as f:
        json.dump(file_mappings, f, indent=4)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Générer un UUID v4 pour nommer le fichier
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        app.logger.info(f'File saved at {file_path}')
        
        # Enregistrer la correspondance dans users_files.json
        save_file_mapping(file.filename, unique_filename)
        
        try:
            global data
            data = pd.read_csv(file_path)
            quantitative = data.select_dtypes(include=[np.number])
            return jsonify({'columns': quantitative.columns.tolist(), 'fileName':file_path})
        except Exception as e:
            app.logger.error(f'Error processing file: {str(e)}')
            return jsonify({'error': 'Error processing file'}), 500
    
    app.logger.error('File upload failed')
    return jsonify({'error': 'File upload failed'}), 500

@app.route('/train', methods=['GET'])
def train_model():
    file_name = request.args.get('filename')
    cols_x = request.args.get('colsX')
    columns_x = cols_x.split(",")
    col_y = request.args.get('colY')
    column_y = str(col_y)

    print("---------------------------")
    print('\n')
    print(file_name," : ",columns_x," - ",column_y)
    print('\n')
    print("---------------------------")

    return jsonify({"message": "Données préparées avec succès"}), 200

if __name__ == '__main__':
    app.run(debug=True)