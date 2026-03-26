# Student Exam Score Prediction - Linear Regression Summative

## Mission
The goal of this project is to predict a student's Math Score based on a combination of lifestyle, demographic, and academic preparation features. By building and comparing multiple regression models, we aim to help educators and institutions identify students who may be at risk of underperforming, and understand which factors most strongly influence academic outcomes in mathematics.

## Problem Statement
Student academic performance is influenced by factors beyond classroom instruction — including parental education level, weekly study hours, test preparation, nutrition, and home environment. Traditional assessment methods react after the fact. This project builds a predictive model that estimates a student's Math Score based on measurable background and lifestyle factors, enabling proactive academic support.

## Dataset
- **Name:** Students Exam Scores Extended Dataset
- **Source:** https://www.kaggle.com/datasets/desalegngeb/students-exam-scores
- **File used:** Expanded_data_with_more_features.csv
- **Records:** 30,641 students
- **Features:** 14 columns (mix of numeric and categorical)

## Feature Description

| Column | Type | Description |
|---|---|---|
| Gender | Categorical | Student gender (male/female) |
| EthnicGroup | Categorical | Student ethnic group — dropped (low predictive value) |
| ParentEduc | Categorical | Parent's highest level of education |
| LunchType | Categorical | Standard or free/reduced lunch (proxy for socioeconomic status) |
| TestPrep | Categorical | Whether student completed a test preparation course |
| ParentMaritalStatus | Categorical | Marital status of parents |
| PracticeSport | Categorical | Frequency of sport practice (never / sometimes / regularly) |
| IsFirstChild | Categorical | Whether the student is the first child |
| NrSiblings | Numeric | Number of siblings |
| TransportMeans | Categorical | How student travels to school |
| WklyStudyHours | Categorical | Weekly study hours (less than 5 / 5-10 / more than 10) |
| ReadingScore | Numeric | Score on the reading exam |
| WritingScore | Numeric | Score on the writing exam |
| **MathScore** | **Numeric** | **Target variable — Math exam score to predict** |

## Project Structure

```
linear_regression_model/
├── README.md
├── summative/
│   ├── linear_regression/
│   │   ├── multivariate.ipynb       <- Main notebook (EDA + all 3 models)
│   │   ├── predict.py               <- Standalone prediction script
│   │   ├── best_model.pkl           <- Saved best-performing model
│   │   └── scaler.pkl               <- Saved StandardScaler
│   ├── API/
│   │   ├── prediction.py            <- FastAPI app
│   │   ├── requirements.txt         <- Python dependencies
│   │   ├── best_model.pkl           <- Model used by API
│   │   └── scaler.pkl               <- Scaler used by API
│   └── FlutterApp/
│       └── student_score_predictor/ <- Flutter mobile/desktop app
```

## Methodology

### 1. Exploratory Data Analysis
- Score distributions (histograms) for Math, Reading, and Writing scores
- Correlation heatmap to identify relationships between numeric features
- Scatterplots of Reading vs Math and Writing vs Math to visualize linear trends
- Boxplot of Math Score grouped by Test Preparation status

### 2. Feature Engineering
- Filled missing values with logical defaults per column (e.g. NrSiblings to 0, TestPrep to none)
- Dropped EthnicGroup — high cardinality with no ordinal meaning and near-zero correlation with MathScore
- Applied Label Encoding to convert all categorical columns to numeric
- Applied StandardScaler to normalize all features (fit on training data only)
- 80% training / 20% test split

### 3. Models Trained

| Model | Details |
|---|---|
| Linear Regression | SGDRegressor with Gradient Descent — loss curve tracked over 100 epochs |
| Decision Tree | DecisionTreeRegressor with max_depth=6 |
| Random Forest | RandomForestRegressor with 100 estimators and max_depth=8 |

### 4. Model Selection
- All three models evaluated using RMSE and R2 Score on the test set
- The model with the lowest RMSE was saved as best_model.pkl

## API

**Live Swagger UI:** https://student-math-predictor-f5kr.onrender.com/docs

**Prediction Endpoint:** POST https://student-math-predictor-f5kr.onrender.com/predict

**Retraining Endpoint:** POST https://student-math-predictor-f5kr.onrender.com/retrain

> Note: The API is hosted on Render free tier. If the first request is slow, wait 30 seconds for the instance to wake up then try again.

## How to Run the Notebook

**Install dependencies:**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn joblib notebook
```

**Run the notebook:**
```bash
cd summative/linear_regression
jupyter notebook multivariate.ipynb
```
Run all cells top to bottom: Kernel > Restart and Run All

**Run a single prediction:**
```bash
python predict.py
```

Expected output:
```
=== Student Math Score Prediction ===
Input sample  : {'Gender': 1, 'ParentEduc': 3, ...}
Predicted Math Score: 75.54
```

## How to Run the Flutter App

1. Make sure Flutter is installed on your machine
2. Clone this repository
3. Navigate to the Flutter app folder:
```bash
cd summative/FlutterApp/student_score_predictor
```
4. Install dependencies:
```bash
flutter pub get
```
5. Run on desktop:
```bash
flutter run -d windows
```
6. Or run on Android by connecting your phone and running:
```bash
flutter run
```
7. Enter student details in the input fields and press **Predict** to get the predicted Math Score

## Key Findings
- ReadingScore and WritingScore are the strongest predictors of MathScore with correlation above 0.80
- Students who completed test preparation scored 5 to 10 points higher on average in Math
- Students studying more than 10 hours per week consistently outperformed their peers
- NrSiblings had near-zero correlation with scores — retained as a weak but harmless feature
- Random Forest outperformed both Linear Regression and Decision Tree due to its ensemble nature

## Video Demo

https://youtu.be/DD0or-6neu0

## Technologies Used
- Python 3.10 and Jupyter Notebook
- pandas, numpy, matplotlib, seaborn
- scikit-learn: SGDRegressor, DecisionTreeRegressor, RandomForestRegressor, StandardScaler
- joblib for model persistence
- FastAPI, Uvicorn, Pydantic for the REST API
- Flutter and Dart for the mobile/desktop app
- Render for API hosting
