# Student Exam Score Prediction

Mission: Predict a students Math Score using lifestyle, parental, and academic features to help educators identify at-risk students early and improve academic support strategies.

Dataset: Students Exam Scores Extended Dataset from Kaggle (Expanded_data_with_more_features.csv), containing 30,641 student records with 14 features including study hours, parental education, test preparation status, and reading/writing scores. Link: https://www.kaggle.com/datasets/desalegngeb/students-exam-scores

Models used: Linear Regression with Gradient Descent (SGDRegressor), Decision Tree Regressor, and Random Forest Regressor. The best-performing model is saved as best_model.pkl and used for inference via predict.py.

Repo structure: summative/linear_regression/ contains the main notebook (multivariate.ipynb), prediction script (predict.py), and saved model files. API/ and FlutterApp/ are reserved for future tasks.
