from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import os
import uuid
import json
import io
import base64


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

USERS_FILES_JSON = "users_files.json"

if not os.path.exists(USERS_FILES_JSON):
    os.makedirs(USERS_FILES_JSON)

data = {}


def save_file_mapping(original_filename, new_filename):
    file_mappings = {}

    if os.path.getsize(USERS_FILES_JSON) > 0:
        try:
            with open(USERS_FILES_JSON, "r") as f:
                file_mappings = json.load(f)
        except json.JSONDecodeError:
            file_mappings = {}

    file_mappings[original_filename] = new_filename

    with open(USERS_FILES_JSON, "w") as f:
        json.dump(file_mappings, f, indent=4)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        app.logger.error("No file part in the request")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        app.logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

        file.save(file_path)
        app.logger.info(f"File saved at {file_path}")

        save_file_mapping(file.filename, unique_filename)

        try:
            global data
            data = pd.read_csv(file_path)
            quantitative = data.select_dtypes(include=[np.number])
            return jsonify(
                {
                    "columns": quantitative.columns.tolist(),
                    "preview": data.head().to_dict(orient="records"),
                    "fileName": file_path,
                }
            )
        except Exception as e:
            app.logger.error(f"Error processing file: {str(e)}")
            return jsonify({"error": "Error processing file"}), 500

    app.logger.error("File upload failed")
    return jsonify({"error": "File upload failed"}), 500


@app.route("/api/select_columns", methods=["POST"])
def select_columns():
    global data
    selected_columns_x = request.json['columnsX']
    selected_column_y = request.json['columnY']

    if selected_column_y not in data.columns or not all(
        col in data.columns for col in selected_columns_x
    ):
        return jsonify({"error": "Invalid column selection"}), 400

    data = data[selected_columns_x + [selected_column_y]]
    return jsonify({"message": "Columns selected successfully"})


@app.route("/api/trainModel", methods=["POST"])
def train_model2():
    
    file_name = request.json['filename']
    columns_x = request.json['colsX']
    column_y = request.json['colY']
    # cols_x = request.json['colsX']
    # columns_x = cols_x.split(",")  # Assurez-vous que colsX est une chaîne, et séparez-la en une liste
    # col_y = request.json['colY']
    # column_y = str(col_y)
    # file_name = request.json['filename']

    print("---------------------------")
    print("\n")
    print("Information :", file_name, " : ", columns_x, " - ", column_y)
    print("\n")
    print("---------------------------")

    print("--- debut recuperation fichier ---")
    # Vérifier que le fichier existe
    try:
        df = pd.read_csv(file_name)  # Charger le fichier CSV
    except FileNotFoundError:
        return jsonify({"error": "Fichier introuvable"}), 404
    print("--- fin recuperation fichier ---")

    print("--- debut select_target_column ---")
    # Création de X et Y
    # Création de X et Y
    x = df[columns_x]
    y = df[column_y].squeeze()  # Assure que y est bien une Series

    # Détecter si le problème est une classification
    is_classification = y.nunique() <= 10  

    # Encoder les classes si nécessaire
    if is_classification and y.dtype == "object":
        y = y.astype("category").cat.codes


    print("--- fin select_target_column ---")

    print("--- debut split_data ---")
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=18
    )
    print("--- fin split_data ---")

    print("--- debut train_xgboost ---")
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    params = {
        "objective": "multi:softprob" if is_classification else "reg:squarederror",
        "eval_metric": "mlogloss" if is_classification else "rmse",
        "num_class": len(set(y_train)) if is_classification else None,
        "max_depth": 6,
        "learning_rate": 0.1,
        "n_estimators": 100,
    }

    evals_result = {}
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=100,
        evals=[(dtrain, "train"), (dtest, "test")],
        early_stopping_rounds=10,
        evals_result=evals_result,
        verbose_eval=10,
    )
    print("--- fin train_xgboost ---")

    print("--- debut evaluate_model ---")
    y_pred = model.predict(dtest)
    if is_classification:
        y_pred_classes = y_pred.argmax(axis=1)
        accuracy = accuracy_score(y_test, y_pred_classes)
        print(f"Accuracy: {accuracy:.2f}")
    else:
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {mse:.2f}")

    # Capture des courbes d'apprentissage en image base64
    learning_curve_img = plot_learning_curves(evals_result)

    # Capture de l'importance des caractéristiques en image base64
    feature_importance_img = plot_feature_importance(model)

    # Retourner les résultats avec les images en base64
    return jsonify({
        "accuracy": accuracy if is_classification else mse,
        "learning_curve": learning_curve_img,
        "feature_importance": feature_importance_img,
        "columns_x": columns_x,
        "column_y": column_y,
    })

def plot_learning_curves(evals_result):
    """Trace les courbes d'apprentissage et les retourne en base64."""
    fig, ax = plt.subplots(figsize=(10, 6))
    for metric in evals_result["train"]:
        ax.plot(evals_result["train"][metric], label=f"Train {metric}")
        ax.plot(evals_result["test"][metric], label=f"Test {metric}")
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Metric Value")
    ax.set_title("XGBoost Training Progress")
    ax.legend()
    ax.grid(True)
    
    # Convertir le plot en image base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)  # Fermer la figure après la conversion

    return img_base64

def plot_feature_importance(model):
    """Trace l'importance des caractéristiques et les retourne en base64."""
    fig, ax = plt.subplots(figsize=(10, 6))
    xgb.plot_importance(model, importance_type="weight", max_num_features=10, ax=ax)
    ax.set_title("Feature Importance")
    
    # Convertir le plot en image base64
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close(fig)  # Fermer la figure après la conversion

    return img_base64

# @app.route("/api/train", methods=["POST"])
# def train_model():
#     global data
#     selected_columns = request.json["columns"]
#     df = data[selected_columns]
#     X = df.iloc[:, :-1]
#     y = df.iloc[:, -1]

#     le = LabelEncoder()
#     y_encoded = le.fit_transform(y)

#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y_encoded, test_size=0.2, random_state=42
#     )
#     model = XGBClassifier()
#     model.fit(X_train, y_train)
#     predictions = model.predict(X_test)
#     accuracy = accuracy_score(y_test, predictions)

#     return jsonify({"accuracy": accuracy})


@app.route("/api/saveModel", methods=["POST"])
def save_model():
    try:
        # Récupérer les données envoyées par le frontend
        model_data = request.json
        colX = model_data.get("colX")
        colY = model_data.get("colY")
        fileName = model_data.get("fileName")
        resultat = model_data.get("resultat")

        # Définir le chemin d'enregistrement du fichier
        file_path = "models_data.json"  # Vous pouvez choisir un autre emplacement et nom de fichier

        # Vérifier si le fichier existe déjà
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                all_models = json.load(f)
        else:
            all_models = []

        # Ajouter les nouvelles données du modèle
        model_entry = {
            "colX": colX,
            "colY": colY,
            "fileName": fileName,
            "resultat": resultat
        }
        all_models.append(model_entry)

        # Enregistrer les données dans le fichier
        with open(file_path, 'w') as f:
            json.dump(all_models, f, indent=4)

        return jsonify({"message": "Model saved successfully", "status": "success"})

    except Exception as e:
        return jsonify({"message": f"Error while saving model: {str(e)}", "status": "error"}), 500

@app.route("/api/getModels", methods=["GET"])
def get_models():
    try:
        # Vérifier si le fichier existe
        file_path = "models_data.json"  # Remplacez par le chemin de votre fichier
        if not os.path.exists(file_path):
            return jsonify({"message": "No models found", "status": "error"}), 404

        # Lire les données du fichier
        with open(file_path, 'r') as f:
            models_data = json.load(f)

        return jsonify({"models": models_data, "status": "success"})

    except Exception as e:
        return jsonify({"message": f"Error while retrieving models: {str(e)}", "status": "error"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=4000)
