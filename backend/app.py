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


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

data = {}

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
    selected_columns_x = request.json["columnsX"]
    selected_column_y = request.json["columnY"]

    if selected_column_y not in data.columns or not all(
        col in data.columns for col in selected_columns_x
    ):
        return jsonify({"error": "Invalid column selection"}), 400

    data = data[selected_columns_x + [selected_column_y]]
    return jsonify({"message": "Columns selected successfully"})


@app.route("/api/trainModel", methods=["POST"])
def trainModel():
    data = request.get_json()  # Récupérer les données JSON du corps de la requête

    file_name = data.get("filename")
    cols_x = data.get("colsX")
    column_x = cols_x.split(
        ","
    )  # Assurez-vous que colsX est une chaîne, et séparez-la en une liste
    col_y = data.get("colY")
    column_y = str(col_y)

    print("---------------------------")
    print("\n")
    print(file_name, " : ", column_x, " - ", column_y)
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
    x = df[columns_x]
    print(column_y)
    y = list(df[column_y])

    # Détecter si le problème est une classification
    is_classification = y.nunique() <= 10

    # Encoder les classes si nécessaire
    if is_classification and y.dtype == "object":
        y = y.astype("category").cat.codes
    print("--- fin select_target_column ---")

    print("--- debut split_data ---")
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
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
    print("--- fin evaluate_model")

    print("--- debut plot_learning_curves ---")
    """Trace les courbes d'apprentissage."""
    plt.figure(figsize=(10, 6))
    for metric in evals_result["train"]:
        plt.plot(evals_result["train"][metric], label=f"Train {metric}")
        plt.plot(evals_result["test"][metric], label=f"Test {metric}")
    plt.xlabel("Rounds")
    plt.ylabel("Metric Value")
    plt.title("XGBoost Training Progress")
    plt.legend()
    plt.grid(True)
    plt.show()
    print("--- fin plot_learning_curves ---")

    print("--- debut plot_feature_importance---")
    xgb.plot_importance(model, importance_type="weight", max_num_features=10)
    plt.title("Feature Importance")
    plt.show()
    print("--- fin plot_feature_importance")
    gg = "ok fin ml"
    return gg


@app.route("/api/train", methods=["POST"])
def train_model():
    global data
    selected_columns = request.json["columns"]
    df = data[selected_columns]
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )
    model = XGBClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return jsonify({"accuracy": accuracy})


if __name__ == "__main__":
    app.run(debug=True, port=4000)
