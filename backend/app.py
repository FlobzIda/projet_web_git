from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Store uploaded CSV data
data = {}

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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        app.logger.info(f'File saved at {file_path}')
        global data
        data['df'] = pd.read_csv(file_path)
        return jsonify({'columns': data['df'].columns.tolist()})
    app.logger.error('File upload failed')
    return jsonify({'error': 'File upload failed'}), 500

@app.route('/train', methods=['POST'])
def train_model():
    global data
    selected_columns = request.json['columns']
    df = data['df'][selected_columns]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Encode the target variable
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    model = XGBClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return jsonify({'accuracy': accuracy})

if __name__ == '__main__':
    app.run(debug=True)