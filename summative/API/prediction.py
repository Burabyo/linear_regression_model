from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
import os
import io

# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Student Math Score Predictor",
    description="Predicts a student's Math Score based on lifestyle and academic features.",
    version="1.0.0"
)

# ── CORS Middleware ────────────────────────────────────────────────────────────
# Configured specifically — NOT using wildcard * for security
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8080",
        "https://student-math-predictor.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

# ── Load model and scaler ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "best_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ── Input schema with Pydantic ─────────────────────────────────────────────────
# Each field has: type enforcement + range constraints + description
class StudentInput(BaseModel):
    Gender: int = Field(
        ..., ge=0, le=1,
        description="Student gender: 0 = female, 1 = male"
    )
    ParentEduc: int = Field(
        ..., ge=0, le=5,
        description="Parent education level (0=some high school, 5=master's degree)"
    )
    LunchType: int = Field(
        ..., ge=0, le=1,
        description="Lunch type: 0 = free/reduced, 1 = standard"
    )
    TestPrep: int = Field(
        ..., ge=0, le=1,
        description="Test preparation: 0 = completed, 1 = none"
    )
    ParentMaritalStatus: int = Field(
        ..., ge=0, le=3,
        description="Parent marital status (0=divorced, 1=married, 2=single, 3=widowed)"
    )
    PracticeSport: int = Field(
        ..., ge=0, le=2,
        description="Sport practice frequency: 0 = never, 1 = sometimes, 2 = regularly"
    )
    IsFirstChild: int = Field(
        ..., ge=0, le=1,
        description="Is first child: 0 = no, 1 = yes"
    )
    NrSiblings: int = Field(
        ..., ge=0, le=7,
        description="Number of siblings (0 to 7)"
    )
    TransportMeans: int = Field(
        ..., ge=0, le=1,
        description="Transport to school: 0 = private, 1 = school bus"
    )
    WklyStudyHours: int = Field(
        ..., ge=0, le=2,
        description="Weekly study hours: 0 = less than 5, 1 = 5 to 10, 2 = more than 10"
    )
    ReadingScore: int = Field(
        ..., ge=0, le=100,
        description="Reading exam score (0 to 100)"
    )
    WritingScore: int = Field(
        ..., ge=0, le=100,
        description="Writing exam score (0 to 100)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "Gender": 1,
                "ParentEduc": 3,
                "LunchType": 1,
                "TestPrep": 0,
                "ParentMaritalStatus": 1,
                "PracticeSport": 2,
                "IsFirstChild": 1,
                "NrSiblings": 2,
                "TransportMeans": 1,
                "WklyStudyHours": 2,
                "ReadingScore": 72,
                "WritingScore": 68
            }
        }

# ── Feature column order (must match training) ────────────────────────────────
FEATURE_COLUMNS = [
    "Gender", "ParentEduc", "LunchType", "TestPrep",
    "ParentMaritalStatus", "PracticeSport", "IsFirstChild",
    "NrSiblings", "TransportMeans", "WklyStudyHours",
    "ReadingScore", "WritingScore"
]

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "Student Math Score Prediction API is running. Visit /docs for Swagger UI."}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", tags=["Prediction"])
def predict(data: StudentInput):
    """
    Predict a student's Math Score based on input features.
    Returns the predicted score as a float.
    """
    try:
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict], columns=FEATURE_COLUMNS)
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        return {
            "predicted_math_score": round(float(prediction), 2),
            "input_received": input_dict
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/retrain", tags=["Model Update"])
async def retrain(file: UploadFile = File(...)):
    """
    Upload a new CSV dataset to retrain the model.
    The CSV must have the same columns as the original training data.
    Triggers model retraining automatically when new data is uploaded.
    """
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error
        import warnings
        warnings.filterwarnings("ignore")

        # Read uploaded CSV
        contents = await file.read()
        new_df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Drop unnamed index column if present
        if "Unnamed: 0" in new_df.columns:
            new_df.drop(columns=["Unnamed: 0"], inplace=True)

        # Drop EthnicGroup if present
        if "EthnicGroup" in new_df.columns:
            new_df.drop(columns=["EthnicGroup"], inplace=True)

        # Fill missing values
        fill_map = {
            "ParentEduc": "unknown", "TestPrep": "none",
            "ParentMaritalStatus": "unknown", "PracticeSport": "never",
            "IsFirstChild": "no", "TransportMeans": "unknown",
            "WklyStudyHours": "unknown"
        }
        for col, val in fill_map.items():
            if col in new_df.columns:
                new_df[col].fillna(val, inplace=True)
        if "NrSiblings" in new_df.columns:
            new_df["NrSiblings"].fillna(0, inplace=True)

        # Encode categorical columns
        cat_cols = new_df.select_dtypes(include="object").columns.tolist()
        le = LabelEncoder()
        for col in cat_cols:
            new_df[col] = le.fit_transform(new_df[col].astype(str))

        # Split features and target
        X = new_df.drop(columns=["MathScore"])
        y = new_df["MathScore"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Fit new scaler and retrain model
        new_scaler = StandardScaler()
        X_train_scaled = new_scaler.fit_transform(X_train)
        X_test_scaled  = new_scaler.transform(X_test)

        new_model = RandomForestRegressor(
            n_estimators=100, max_depth=8, random_state=42, n_jobs=-1
        )
        new_model.fit(X_train_scaled, y_train)

        # Evaluate
        preds = new_model.predict(X_test_scaled)
        rmse  = np.sqrt(mean_squared_error(y_test, preds))

        # Save updated model and scaler
        joblib.dump(new_model,  MODEL_PATH)
        joblib.dump(new_scaler, SCALER_PATH)

        # Reload into memory
        global model, scaler
        model  = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)

        return {
            "message": "Model retrained and updated successfully.",
            "new_data_rows": len(new_df),
            "retrain_rmse": round(rmse, 4)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")
