# Prediction Models

## Overview
This notebook focuses on building predictive machine learning models for airline operational analysis and passenger experience forecasting.

The project applies classification and regression techniques to predict:
- Flight delay risk
- Delay duration
- Passenger satisfaction levels
- Operational performance indicators

The models use engineered operational, weather, passenger, and sentiment-related features to support predictive analytics and decision-making in airline operations.

---

## Dataset Information

The dataset contains airline operational and passenger service records including:
- Flight schedules
- Flight status
- Delay information
- Passenger satisfaction
- Weather conditions
- Operational efficiency
- Airline information
- Service ratings
- Seasonal and crowd indicators

Main columns used:
- Airline_Name
- Flight_Status
- Delay_Minutes
- Satisfaction_Index
- Weather_Condition2
- Load_Factor
- Tourist_Flow
- Crowd_Level
- Sentiment_Score
- Operational_Efficiency_Score
- Departure_DateTime
- Arrival_DateTime

---

## Main Tasks Performed

### 1. Feature Engineering
Created multiple predictive features including:
- Delay_Risk
- Satisfaction_Level
- Departure_Hour
- Departure_Month
- Departure_Year
- Is_Weekend
- Time_Period
- Weather_Severity
- Route
- Flight_Duration_Hours

Derived additional operational and temporal features from datetime and airline records.

---

### 2. Data Preprocessing
Performed preprocessing operations including:
- Label Encoding for categorical variables
- Datetime transformation
- Feature extraction
- Missing value handling
- Target variable generation

Prepared structured datasets suitable for machine learning models.

---

## Predictive Models

### Model 1 — Flight Delay Risk Prediction
Built a classification model to predict whether a flight will be delayed.

#### Algorithm Used
- Random Forest Classifier

#### Features Used
Included:
- Airline information
- Route data
- Weather conditions
- Passenger demand indicators
- Seasonal factors
- Sentiment scores
- Operational variables

#### Evaluation Metrics
Evaluated using:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Cross Validation

Generated:
- Classification Report
- Confusion Matrix
- ROC Curve
- Feature Importance Analysis

---

### Model 2 — Delay Duration Prediction
Built a regression model to predict flight delay duration in minutes.

The model estimates expected operational delay severity using operational and environmental features.

#### Regression Techniques Used
- Machine Learning Regression Models
- Ensemble-based prediction methods

#### Evaluation Metrics
Measured using:
- RMSE
- MAE
- R² Score

---

### Model 3 — Satisfaction Prediction
Built predictive models to estimate passenger satisfaction levels based on:
- Operational efficiency
- Delays
- Service quality
- Waiting times
- Passenger sentiment

Predicted satisfaction categories such as:
- High
- Medium
- Low

---

## Model Evaluation & Validation

Applied:
- Train/Test Split
- Stratified Cross Validation
- Performance benchmarking
- Comparative model evaluation

Generated validation metrics to assess model reliability and generalization performance.

---

## Visualization & Analysis

Generated analytical visualizations including:
- Confusion matrices
- ROC curves
- Feature importance charts
- Performance comparison graphs
- Operational trend visualizations

Used visualization techniques to explain model behavior and prediction quality.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- LightGBM
- Matplotlib
- Seaborn

---

## Output

The notebook produces:
- Predictive machine learning models
- Delay risk predictions
- Delay duration forecasts
- Passenger satisfaction predictions
- Feature importance analysis
- Classification & regression evaluation metrics
- Operational performance insights
