# Sentiment Analysis

## Overview
This notebook focuses on performing advanced Arabic sentiment analysis on airline passenger reviews and tweets related to customer experience, delays, onboard services, and operational efficiency.

The analysis combines:
- Arabic NLP preprocessing
- Lexicon-based sentiment scoring
- Machine learning classification
- Topic classification
- KPI and correlation analysis

The objective is to understand passenger opinions, classify customer sentiment, and measure the relationship between operational performance and passenger satisfaction.

---

## Dataset Information

- Dataset Size: 40,000 records
- Language: Arabic (Saudi dialect + Modern Standard Arabic)
- Domain: Airline passenger reviews and operational feedback

Main columns used:
- Tweet_Text
- Sentiment_Category
- Topic
- Satisfaction_Index
- Delay_Minutes
- Airline_Name
- Operational_Efficiency_Score

---

## Main Tasks Performed

### 1. Arabic Text Preprocessing
Applied comprehensive Arabic NLP preprocessing techniques including:
- URL removal
- English character and number removal
- Arabic text normalization
- Diacritics removal
- Character repetition reduction
- Stopword removal
- Noise cleaning

Generated processed text columns:
- `text_processed`
- `text_no_stopwords`

---

### 2. Arabic Sentiment Lexicon Construction
Built custom Arabic sentiment lexicons specifically designed for airline reviews:
- Positive sentiment lexicon
- Negative sentiment lexicon
- Negation word handling
- Sentiment intensifiers

The lexicon supports:
- Saudi dialect expressions
- Context-aware sentiment scoring
- Negation detection
- Weighted sentiment polarity

---

### 3. Lexicon-Based Sentiment Analysis
Implemented a custom sentiment scoring system that:
- Calculates sentiment polarity scores
- Detects positive and negative word counts
- Handles negation and intensifiers
- Produces normalized sentiment values

Generated features:
- `Sentiment_Score`
- `Positive_Word_Count`
- `Negative_Word_Count`
- `Sentiment_Predicted`

---

### 4. Sentiment Validation
Compared predicted sentiment labels against original human-labeled sentiment data.

Results:
- Lexicon agreement with original labels: 99.6%
- Neutral class detection added to the dataset
- Misclassification analysis performed

---

### 5. TF-IDF Feature Engineering
Applied TF-IDF vectorization for machine learning text representation using:
- Unigrams and bigrams
- Feature filtering
- Vocabulary optimization

Configuration:
- Max features: 8000
- N-gram range: (1,2)
- Sublinear TF scaling

---

### 6. Machine Learning Sentiment Classification
Trained multiple machine learning models for sentiment classification:

Models used:
- Logistic Regression
- Linear SVM
- Random Forest

Evaluation metrics:
- Accuracy
- Weighted F1-score
- Cross-validation performance
- Classification reports

Best model:
- Logistic Regression

Performance:
- Test Accuracy: 100%
- Weighted F1 Score: 1.0000
- Cross-validation F1: 0.8787

---

### 7. Important Sentiment Indicators
Extracted the most influential positive and negative textual indicators using Logistic Regression coefficients.

Examples:
- Positive indicators:
  - ممتازة
  - خدمة
  - أنصح
  - تجربة حلوة

- Negative indicators:
  - سيئة
  - تأخير
  - قديمة
  - ضاعت

---

### 8. Topic Classification
Implemented rule-based topic classification for passenger complaints and reviews.

Topics detected:
- Flight Delays
- Seat Comfort
- Staff Behavior
- Meal Quality
- Cleanliness
- Service Efficiency
- Overall Experience

Generated features:
- `Topic_Predicted`
- `Topic_Confidence`

---

### 9. KPI & Business Analysis
Generated airline-level sentiment KPIs including:
- Average sentiment score
- Positive review percentage
- Negative review percentage
- Satisfaction averages
- Topic-based issue analysis

Performed:
- Airline comparison
- Seasonal sentiment analysis
- Topic severity analysis

---

### 10. Correlation Analysis
Analyzed the relationship between sentiment and operational metrics such as:
- Delay minutes
- Wait times
- Complaints logged
- Service quality
- Satisfaction index

---

### 11. Satisfaction Score Integration
Integrated sentiment scores into passenger satisfaction calculations.

Created:
- Updated `Satisfaction_Index`
- `Satisfaction_Level`
- `Service_Quality_Score`

Observed:
- Positive correlation between sentiment and satisfaction
- Higher satisfaction for positive reviews
- Lower satisfaction for negative sentiment

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Regular Expressions (re)
- TF-IDF Vectorization
- Logistic Regression
- Linear SVM
- Random Forest

---

## Output

The notebook produces:
- Clean Arabic text representations
- Sentiment classification results
- Topic classification labels
- Machine learning sentiment predictions
- Airline KPI metrics
- Operational insight analysis
- Satisfaction and service quality indicators
