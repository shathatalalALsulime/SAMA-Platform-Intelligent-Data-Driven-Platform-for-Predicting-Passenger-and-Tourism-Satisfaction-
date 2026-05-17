# Data Cleaning & Feature Engineering

## Overview
This notebook focuses on data preprocessing, data quality auditing, inconsistency correction, feature engineering, and Arabic text cleaning for an airline operations and customer satisfaction dataset.

The goal of this stage is to prepare high-quality, reliable, and analysis-ready data for sentiment analysis, KPI evaluation, and predictive modeling.

---

## Main Tasks Performed

### 1. Dataset Loading
- Loaded the airline dataset using Pandas
- Checked dataset dimensions and date ranges
- Inspected airline distribution

---

### 2. Data Quality Audit
Performed several quality checks including:
- Missing value detection
- Duplicate Flight_ID detection
- Data type validation
- Date consistency checks

---

### 3. Inconsistency Detection & Correction
Identified and fixed multiple logical inconsistencies such as:
- Incorrect Delay_Category values
- Invalid seasonal assignments
- Unrealistic Satisfaction_Index relationships
- Incorrect Operational_Efficiency_Score behavior
- Duplicate flight identifiers

The following columns were recalculated or corrected:
- Delay_Category
- Event_Season
- Satisfaction_Index
- Operational_Efficiency_Score
- Flight_ID

---

### 4. Feature Engineering
Created several new features to support analysis and machine learning, including:
- Flight_Duration_Hours
- Departure_Hour
- Departure_Month
- Time_Period
- Route
- Total_Wait_Minutes
- Delay_Risk
- Satisfaction_Level
- Is_Peak_Season
- Weather_Severity
- Service_Quality_Score

---

### 5. Arabic Text Cleaning
Applied Arabic NLP preprocessing techniques including:
- URL removal
- English text removal
- Arabic normalization
- Diacritics removal
- Emoji and special character cleaning
- Repeated character normalization

Generated additional text features:
- Text_Length
- Word_Count

---

### 6. Final Validation
Performed validation checks to ensure:
- Logical consistency between flight status and delays
- Correct satisfaction score behavior
- Valid efficiency score relationships
- Unique flight identifiers

---

## Technologies Used
- Python
- Pandas
- NumPy
- Regular Expressions (re)

---

## Output
The notebook produces a fully cleaned and feature-engineered dataset ready for:
- Sentiment Analysis
- KPI Analysis
- Predictive Modeling
