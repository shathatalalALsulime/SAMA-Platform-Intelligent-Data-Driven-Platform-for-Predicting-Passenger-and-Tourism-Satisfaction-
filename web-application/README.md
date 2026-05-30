# 🛫 SAMA Platform 
## Intelligent Data-Driven Platform for Saudi Aviation Analytics

**BSc Graduation Project — UQU-DS-2025-F02**

---

## 🚀 Quick Start  

### Requirements 
```
Python 3.9+
```

### Step 1: Install Dependencies
```bash
pip install flask pandas numpy scikit-learn xgboost lightgbm openpyxl
```

### Step 2: Place Your Data 
Place `SAMA_Phase3_Sentiment.xlsx` in the project root folder (same folder as `app.py`)

### Step 3: Initialize Database 
```bash
python init_db.py
```
This will:
- Create SQLite database with 8 tables
- Load all 40,000 flight records
- Compute KPIs for airlines, airports, seasons
- Train AI prediction models (Delay Risk + Satisfaction)
- Generate early warning alerts

### Step 4: Run the Application 
```bash
python app.py
```
Open your browser: **http://localhost:5000**

---

## 📱 Pages 

| Page | URL | Description |
|------|-----|-------------|
| 🏠 Home | `/` | Overview with KPIs, airline cards, and charts |
| ✈️ Traveler Dashboard | `/traveler` | Compare airlines, routes, topic ratings |
| 📊 Airline Dashboard | `/airline` | Performance KPIs, trends, delay analysis |
| 🧠 AI Predictions | `/predictions` | Predict delay risk & satisfaction score |
| 💬 Sentiment Analysis | `/sentiment` | Arabic NLP results, reviews, charts |
| 🔔 Early Warning | `/alerts` | Real-time alerts for performance issues |

---

## 🏗️ Project Structure

```
sama_platform/
├── app.py                  # Flask web application
├── init_db.py              # Database setup & triggers model training
├── README.md               # This file
├── SAMA_Phase3_Sentiment.xlsx  # Input data (place here)
├── models/                 # ← ML Models (separate files)
│   ├── __init__.py
│   ├── model1_delay_risk.py         # Binary classification — delay prediction
│   ├── model2_delay_duration.py     # Regression — delay minutes estimation
│   ├── model3_satisfaction_class.py # Multi-class — satisfaction High/Med/Low
│   ├── model4_satisfaction_score.py # Regression — satisfaction 0-100
│   └── model5_seasonal_forecast.py  # Time-series — monthly forecast
├── data/
│   ├── sama.db            # SQLite database (auto-generated)
│   └── models.pkl         # All 5 trained models (auto-generated)
└── templates/
    ├── base.html          # Base template with navigation
    ├── home.html          # Landing page
    ├── traveler.html      # Traveler dashboard
    ├── airline.html       # Airline dashboard
    ├── predictions.html   # AI prediction page (runs all 5 models)
    ├── sentiment.html     # Sentiment analysis page
    └── alerts.html        # Early warning system
```

---

## 🔧 Technology Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (Phase 6)
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Charts:** Chart.js
- **ML Models:** Random Forest, XGBoost, LightGBM
- **NLP:** Custom Arabic lexicon-based sentiment analysis

---

## 📊 Integrated Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Feature Mapping | ✅ |
| 2 | Data Cleaning & Feature Engineering | ✅ |
| 3 | Arabic Sentiment Analysis | ✅ |
| 4 | KPIs & Exploratory Analysis | ✅ |
| 5 | Predictive Models | ✅ |
| 6 | Database Schema (SQLite) | ✅ |
| 7 | Interactive Dashboards (Flask) | ✅ |
| 8 | Early Warning System | ✅ |
