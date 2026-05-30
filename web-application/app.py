"""
SAMA Platform — Flask Web Application
Phases 6, 7, 8 Integrated: Database + Dashboards + Early Warning
With User Authentication: Traveler & Airline portals
"""
import os
import sqlite3
import json
import pickle
import hashlib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'sama_platform_2025_secret_key_uqu'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'sama.db')
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'models.pkl')

# Airport name mapping
AIRPORTS = {
    'RUH': {'en': 'Riyadh', 'ar': 'الرياض'},
    'JED': {'en': 'Jeddah', 'ar': 'جدة'},
    'DMM': {'en': 'Dammam', 'ar': 'الدمام'},
    'MED': {'en': 'Madinah', 'ar': 'المدينة المنورة'},
    'AHB': {'en': 'Abha', 'ar': 'أبها'},
    'GIZ': {'en': 'Jazan', 'ar': 'جازان'},
}

AIRLINE_COLORS = {'Saudia': '#006B3F', 'Flynas': '#7B2D8E', 'Flyadeal': '#E31837'}


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_kpi(kpi_type, group_value, metric_name):
    conn = get_db()
    row = conn.execute("SELECT metric_value FROM kpis WHERE kpi_type=? AND group_value=? AND metric_name=?",
                       (kpi_type, group_value, metric_name)).fetchone()
    conn.close()
    return row['metric_value'] if row else 0


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def login_required(role=None):
    """Check if user is logged in and optionally check role"""
    if 'user_id' not in session:
        return False
    if role and session.get('role') != role:
        return False
    return True


# ============================================================
# AUTH ROUTES
# ============================================================

@app.route('/')
def landing():
    """Landing page — choose traveler or airline login"""
    if 'user_id' in session:
        if session['role'] == 'traveler':
            return redirect(url_for('traveler_home'))
        else:
            return redirect(url_for('airline_dashboard'))
    return render_template('landing.html')


@app.route('/login/traveler', methods=['GET', 'POST'])
def login_traveler():
    if request.method == 'POST':
        user_id = request.form['user_id'].strip()
        password = request.form['password'].strip()
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE user_id=? AND password=?",
                           (user_id, hash_pw(password))).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = 'traveler'
            return redirect(url_for('traveler_home'))
        else:
            flash('رقم المستخدم أو كلمة المرور غير صحيحة — Invalid User ID or Password', 'error')
    return render_template('login.html', role='traveler')


@app.route('/login/airline', methods=['GET', 'POST'])
def login_airline():
    if request.method == 'POST':
        user_id = request.form['user_id'].strip()
        password = request.form['password'].strip()
        conn = get_db()
        user = conn.execute("SELECT * FROM airline_accounts WHERE user_id=? AND password=?",
                           (user_id, hash_pw(password))).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = 'airline'
            session['airline_name'] = user['airline_name']
            return redirect(url_for('airline_dashboard'))
        else:
            flash('رقم المستخدم أو كلمة المرور غير صحيحة — Invalid User ID or Password', 'error')
    return render_template('login.html', role='airline')


@app.route('/register/traveler', methods=['GET', 'POST'])
def register_traveler():
    if request.method == 'POST':
        name = request.form['name'].strip()
        user_id = request.form['user_id'].strip()
        password = request.form['password'].strip()
        # Validate 8-digit user ID
        if len(user_id) != 8 or not user_id.isdigit():
            flash('رقم المستخدم يجب أن يكون 8 أرقام — User ID must be 8 digits', 'error')
            return render_template('register.html', role='traveler')
        if len(password) < 4:
            flash('كلمة المرور قصيرة جداً — Password too short', 'error')
            return render_template('register.html', role='traveler')
        conn = get_db()
        existing = conn.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,)).fetchone()
        if existing:
            conn.close()
            flash('رقم المستخدم مستخدم بالفعل — User ID already exists', 'error')
            return render_template('register.html', role='traveler')
        conn.execute("INSERT INTO users (user_id, name, password) VALUES (?,?,?)",
                    (user_id, name, hash_pw(password)))
        conn.commit()
        conn.close()
        flash('تم إنشاء الحساب بنجاح! — Account created successfully!', 'success')
        return redirect(url_for('login_traveler'))
    return render_template('register.html', role='traveler')


@app.route('/register/airline', methods=['GET', 'POST'])
def register_airline():
    if request.method == 'POST':
        name = request.form['name'].strip()
        user_id = request.form['user_id'].strip()
        password = request.form['password'].strip()
        airline_name = request.form['airline_name'].strip()
        if len(user_id) != 8 or not user_id.isdigit():
            flash('رقم المستخدم يجب أن يكون 8 أرقام — User ID must be 8 digits', 'error')
            return render_template('register.html', role='airline')
        conn = get_db()
        existing = conn.execute("SELECT user_id FROM airline_accounts WHERE user_id=?", (user_id,)).fetchone()
        if existing:
            conn.close()
            flash('رقم المستخدم مستخدم بالفعل — User ID already exists', 'error')
            return render_template('register.html', role='airline')
        conn.execute("INSERT INTO airline_accounts (user_id, name, password, airline_name) VALUES (?,?,?,?)",
                    (user_id, name, hash_pw(password), airline_name))
        conn.commit()
        conn.close()
        flash('تم إنشاء الحساب بنجاح! — Account created successfully!', 'success')
        return redirect(url_for('login_airline'))
    return render_template('register.html', role='airline')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


# ============================================================
# API ENDPOINTS
# ============================================================

@app.route('/api/alerts')
def api_alerts():
    """API endpoint for real-time alert polling"""
    if not login_required('airline'):
        return jsonify({'error': 'unauthorized'}), 401
    conn = get_db()
    airline = session.get('airline_name', '')
    rows = conn.execute("""
        SELECT * FROM alerts WHERE is_active=1
        AND (airline=? OR airline IS NULL)
        ORDER BY severity DESC, created_at DESC
    """, (airline,)).fetchall()
    conn.close()
    alerts_list = [dict(r) for r in rows]
    return jsonify({'alerts': alerts_list, 'count': len(alerts_list)})


# ============================================================
# TRAVELER ROUTES (requires traveler login)
# ============================================================

@app.route('/traveler')
def traveler_home():
    """Traveler home — airline overview"""
    if not login_required('traveler'):
        return redirect(url_for('login_traveler'))
    conn = get_db()
    overall = {}
    for metric in ['total_flights', 'ontime_rate', 'avg_satisfaction', 'positive_rate', 'avg_delay', 'complaint_rate', 'cancelled_rate']:
        overall[metric] = get_kpi('overall', 'all', metric)

    airlines_data = []
    for airline in ['Saudia', 'Flynas', 'Flyadeal']:
        airlines_data.append({
            'name': airline,
            'color': AIRLINE_COLORS[airline],
            'flights': int(get_kpi('airline', airline, 'total_flights')),
            'ontime': round(get_kpi('airline', airline, 'ontime_rate'), 1),
            'satisfaction': round(get_kpi('airline', airline, 'avg_satisfaction'), 1),
            'sentiment': round(get_kpi('airline', airline, 'positive_rate'), 1),
        })

    alert_count = conn.execute("SELECT COUNT(*) FROM alerts WHERE is_active=1").fetchone()[0]
    conn.close()
    return render_template('home.html', overall=overall, airlines=airlines_data, alert_count=alert_count, user=session)


@app.route('/traveler/compare')
def traveler_compare():
    """Traveler — airline comparison & route insights"""
    if not login_required('traveler'):
        return redirect(url_for('login_traveler'))
    conn = get_db()

    # Airline comparison
    airlines = []
    for airline in ['Saudia', 'Flynas', 'Flyadeal']:
        data = {'name': airline, 'color': AIRLINE_COLORS[airline]}
        for m in ['total_flights','ontime_rate','avg_satisfaction','avg_sentiment','positive_rate',
                  'avg_delay','avg_service','complaint_rate','avg_checkin','avg_boarding','avg_baggage']:
            data[m] = round(get_kpi('airline', airline, m), 1)
        airlines.append(data)

    # Top routes by satisfaction
    routes = conn.execute("""
        SELECT f.origin_city || ' → ' || f.destination_city as route,
               f.airline_name,
               ROUND(AVG(p.satisfaction_index), 1) as avg_sat,
               ROUND(AVG(CASE WHEN f.flight_status='On-time' THEN 1.0 ELSE 0.0 END)*100, 1) as ontime_pct,
               COUNT(*) as flights
        FROM flights f JOIN passengers p ON f.flight_id = p.flight_id
        GROUP BY route, f.airline_name
        HAVING flights > 100
        ORDER BY avg_sat DESC LIMIT 15
    """).fetchall()

    # Topic ratings per airline
    topics = conn.execute("""
        SELECT r.topic, f.airline_name,
               ROUND(AVG(r.sentiment_score), 3) as avg_sent,
               ROUND(AVG(CASE WHEN r.sentiment_category='إيجابي' THEN 1.0 ELSE 0.0 END)*100, 1) as pos_pct,
               COUNT(*) as cnt
        FROM reviews r JOIN flights f ON r.flight_id = f.flight_id
        GROUP BY r.topic, f.airline_name
        ORDER BY r.topic, avg_sent DESC
    """).fetchall()

    conn.close()
    return render_template('traveler.html', airlines=airlines, routes=routes, topics=topics, airports=AIRPORTS, user=session)


@app.route('/airline')
def airline_dashboard():
    """Airline dashboard — KPIs, trends, performance"""
    if not login_required('airline'):
        return redirect(url_for('login_airline'))
    selected = session.get('airline_name', 'Saudia')
    return _render_airline_dashboard(selected)


@app.route('/airline/competitor')
def airline_competitor():
    """Airline dashboard — viewing a competitor"""
    if not login_required('airline'):
        return redirect(url_for('login_airline'))
    selected = request.args.get('view', session.get('airline_name', 'Saudia'))
    if selected not in ['Saudia', 'Flynas', 'Flyadeal']:
        selected = session.get('airline_name', 'Saudia')
    return _render_airline_dashboard(selected, is_competitor=True)


def _render_airline_dashboard(selected, is_competitor=False):
    """Shared logic for airline and competitor dashboards"""
    conn = get_db()

    # Main KPIs
    kpis = {}
    for m in ['total_flights','ontime_rate','avg_satisfaction','avg_sentiment','positive_rate',
              'avg_delay','avg_efficiency','avg_service','complaint_rate','avg_checkin','avg_boarding','avg_baggage']:
        kpis[m] = round(get_kpi('airline', selected, m), 1)

    # Monthly trends
    monthly = conn.execute("""
        SELECT t.departure_month, t.departure_year,
               ROUND(AVG(p.satisfaction_index), 1) as avg_sat,
               ROUND(AVG(f.delay_minutes), 1) as avg_delay,
               ROUND(AVG(CASE WHEN f.flight_status='On-time' THEN 1.0 ELSE 0.0 END)*100, 1) as ontime_pct,
               COUNT(*) as flights
        FROM flights f
        JOIN passengers p ON f.flight_id = p.flight_id
        JOIN temporal t ON f.flight_id = t.flight_id
        WHERE f.airline_name = ?
        GROUP BY t.departure_year, t.departure_month
        ORDER BY t.departure_year, t.departure_month
    """, (selected,)).fetchall()

    # Topic breakdown
    topics_raw = conn.execute("""
        SELECT r.topic,
               COUNT(*) as cnt,
               ROUND(AVG(r.sentiment_score), 3) as avg_sent,
               ROUND(AVG(CASE WHEN r.sentiment_category='سلبي' THEN 1.0 ELSE 0.0 END)*100, 1) as neg_pct
        FROM reviews r JOIN flights f ON r.flight_id = f.flight_id
        WHERE f.airline_name = ?
        GROUP BY r.topic ORDER BY cnt DESC
    """, (selected,)).fetchall()
    topics = [dict(r) for r in topics_raw]

    # Delay reasons
    delay_reasons_raw = conn.execute("""
        SELECT delay_reason, COUNT(*) as cnt,
               ROUND(AVG(delay_minutes), 1) as avg_delay
        FROM flights WHERE airline_name=? AND delay_reason != 'No Delay'
        GROUP BY delay_reason ORDER BY cnt DESC
    """, (selected,)).fetchall()
    delay_reasons = [dict(r) for r in delay_reasons_raw]

    # Airport performance
    airport_perf = conn.execute("""
        SELECT f.destination_city,
               ROUND(AVG(p.satisfaction_index), 1) as avg_sat,
               ROUND(AVG(CASE WHEN f.flight_status='On-time' THEN 1.0 ELSE 0.0 END)*100, 1) as ontime_pct,
               COUNT(*) as flights
        FROM flights f JOIN passengers p ON f.flight_id = p.flight_id
        WHERE f.airline_name = ?
        GROUP BY f.destination_city ORDER BY avg_sat DESC
    """, (selected,)).fetchall()

    conn.close()
    return render_template('airline.html', selected=selected, kpis=kpis,
                         monthly=monthly, topics=topics, delay_reasons=delay_reasons,
                         airport_perf=airport_perf, airports=AIRPORTS,
                         airline_colors=AIRLINE_COLORS, user=session,
                         is_competitor=is_competitor, my_airline=session.get('airline_name',''))


@app.route('/predictions', methods=['GET', 'POST'])
def predictions():
    """Prediction page — ALL 5 models run on user input"""
    if not login_required():
        return redirect(url_for('landing'))
    result = None
    if request.method == 'POST':
        try:
            with open(MODEL_PATH, 'rb') as f:
                model_data = pickle.load(f)

            le_dict = model_data['label_encoders']

            # Get form values
            form = request.form
            airline = form['airline']
            origin = form['origin']
            destination = form['destination']
            aircraft = form['aircraft']
            weather = form['weather']
            month = int(form['month'])
            day = form['day']
            hour = int(form['hour'])
            load = float(form['load_factor'])
            service = int(form['service_rating'])
            checkin = int(form['checkin_time'])
            boarding = int(form['boarding_time'])
            baggage = int(form['baggage_time'])

            # Derived features
            season_map = {12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',
                          6:'Summer',7:'Summer',8:'Summer',9:'Autumn',10:'Autumn',11:'Autumn'}
            season = season_map[month]
            is_peak = 1 if month in [1,2,3,6,10,11,12] else 0
            is_weekend = 1 if day in ['Thursday','Friday'] else 0
            holiday = 1 if is_peak else 0
            time_period = 'Morning' if 5<=hour<12 else ('Afternoon' if 12<=hour<17 else ('Evening' if 17<=hour<21 else 'Night'))
            ws_map = {'Clear':'Clear','Sunny':'Clear','Hot':'Clear','Cloudy':'Moderate','Humid':'Moderate','Rain':'Moderate','Sandstorm':'Severe','Fog':'Severe'}
            weather_sev = ws_map.get(weather, 'Clear')

            # Encode helper
            def enc(col, val):
                try: return le_dict[col].transform([val])[0]
                except: return 0

            # ========== MODEL 1: Delay Risk ==========
            delay_input = [
                enc('Airline_Name',airline), enc('Origin_City',origin), enc('Destination_City',destination),
                enc('Aircraft_Type',aircraft), load, 40, enc('Weather_Condition2',weather),
                25, 15, enc('Season',season), enc('Day_of_Week',day),
                holiday, is_peak, is_weekend, hour, month, 7000,
                enc('Crowd_Level','Medium'), enc('Airport_Crowd_Level','Medium'),
                enc('Time_Period',time_period), enc('Weather_Severity',weather_sev), 0.0
            ]
            delay_prob = model_data['delay_risk_model'].predict_proba([delay_input])[0][1]
            delay_risk = 'High' if delay_prob > 0.5 else ('Medium' if delay_prob > 0.25 else 'Low')

            # ========== MODEL 2: Delay Duration ==========
            delay_duration_pred = model_data['delay_duration_model'].predict([delay_input])[0]
            delay_duration_pred = max(5, min(180, delay_duration_pred))

            # ========== MODEL 3 & 4: Satisfaction (needs operational features) ==========
            # Build satisfaction feature vector (delay_features + operational features)
            is_delayed = 1 if delay_prob > 0.5 else 0
            est_delay_min = delay_duration_pred if is_delayed else 0
            flight_status_code = enc('Flight_Status', 'Delayed' if is_delayed else 'On-time')

            sat_input = delay_input + [
                est_delay_min, flight_status_code, service,
                checkin, boarding, baggage, 0,
                enc('Connection_Flag','Direct'), enc('Ticket_Type','Non-refundable'),
                enc('Customer_Segment','Leisure'), enc('Loyalty_Status','Not Enrolled')
            ]

            # Model 3: Satisfaction Level
            sat_level_pred = model_data['sat_class_model'].predict([sat_input])[0]
            sat_level_map = {0: 'Low', 1: 'Medium', 2: 'High'}
            sat_level = sat_level_map.get(sat_level_pred, 'Medium')
            sat_level_proba = model_data['sat_class_model'].predict_proba([sat_input])[0]

            # Model 4: Satisfaction Score
            sat_score = model_data['sat_score_model'].predict([sat_input])[0]
            sat_score = max(0, min(100, sat_score))

            # ========== MODEL 5: Seasonal Forecast ==========
            forecast_airline_enc = model_data['forecast_airline_encoder']
            try:
                airline_code = forecast_airline_enc.transform([airline])[0]
            except:
                airline_code = 0
            # Use reasonable defaults for lag features (overall averages)
            forecast_input = [month, airline_code, load, 7000, 500, 61.0, 8.0, -0.1, 20.0]
            seasonal_sat = model_data['forecast_sat_model'].predict([forecast_input])[0]
            seasonal_del = model_data['forecast_del_model'].predict([forecast_input])[0]
            seasonal_risk = 'High' if seasonal_del > 25 else ('Medium' if seasonal_del > 18 else 'Low')

            result = {
                # Model 1
                'delay_probability': round(delay_prob * 100, 1),
                'delay_risk': delay_risk,
                # Model 2
                'delay_duration': round(delay_duration_pred, 0),
                # Model 3
                'sat_level': sat_level,
                'sat_level_proba': {
                    'Low': round(sat_level_proba[0] * 100, 1),
                    'Medium': round(sat_level_proba[1] * 100, 1),
                    'High': round(sat_level_proba[2] * 100, 1),
                },
                # Model 4
                'sat_score': round(sat_score, 1),
                # Model 5
                'seasonal_sat': round(seasonal_sat, 1),
                'seasonal_del': round(seasonal_del, 1),
                'seasonal_risk': seasonal_risk,
            }
        except Exception as e:
            import traceback
            result = {'error': str(e), 'trace': traceback.format_exc()}

    return render_template('predictions.html', result=result, airports=AIRPORTS, user=session)


@app.route('/alerts')
def alerts():
    """Early warning system"""
    if not login_required('airline'):
        return redirect(url_for('login_airline'))
    conn = get_db()
    all_alerts = conn.execute("""
        SELECT * FROM alerts WHERE is_active=1 ORDER BY 
        CASE severity WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
        created_at DESC
    """).fetchall()
    conn.close()
    return render_template('alerts.html', alerts=all_alerts, user=session)


@app.route('/sentiment')
def sentiment():
    """Sentiment analysis page"""
    if not login_required():
        return redirect(url_for('landing'))
    conn = get_db()

    # Overall sentiment
    sent_dist = [dict(r) for r in conn.execute("""
        SELECT sentiment_category, COUNT(*) as cnt,
               ROUND(AVG(sentiment_score), 3) as avg_score
        FROM reviews GROUP BY sentiment_category
    """).fetchall()]

    # Sentiment by airline
    sent_airline = [dict(r) for r in conn.execute("""
        SELECT f.airline_name, r.sentiment_category, COUNT(*) as cnt
        FROM reviews r JOIN flights f ON r.flight_id = f.flight_id
        GROUP BY f.airline_name, r.sentiment_category
    """).fetchall()]

    # Sample reviews
    pos_reviews = conn.execute("""
        SELECT r.tweet_text, r.sentiment_score, r.topic, f.airline_name
        FROM reviews r JOIN flights f ON r.flight_id = f.flight_id
        WHERE r.sentiment_category = 'إيجابي'
        ORDER BY r.sentiment_score DESC LIMIT 10
    """).fetchall()

    neg_reviews = conn.execute("""
        SELECT r.tweet_text, r.sentiment_score, r.topic, f.airline_name
        FROM reviews r JOIN flights f ON r.flight_id = f.flight_id
        WHERE r.sentiment_category = 'سلبي'
        ORDER BY r.sentiment_score ASC LIMIT 10
    """).fetchall()

    conn.close()
    return render_template('sentiment.html', sent_dist=sent_dist, sent_airline=sent_airline,
                         pos_reviews=pos_reviews, neg_reviews=neg_reviews, user=session)


@app.route('/api/chart/<chart_type>')
def api_chart(chart_type):
    """API endpoints for chart data"""
    conn = get_db()
    data = {}

    if chart_type == 'monthly_trend':
        airline = request.args.get('airline', 'Saudia')
        rows = conn.execute("""
            SELECT t.departure_month as month, t.departure_year as year,
                   ROUND(AVG(p.satisfaction_index),1) as sat,
                   ROUND(AVG(f.delay_minutes),1) as delay,
                   ROUND(AVG(CASE WHEN f.flight_status='On-time' THEN 1.0 ELSE 0.0 END)*100,1) as ontime
            FROM flights f JOIN passengers p ON f.flight_id=p.flight_id JOIN temporal t ON f.flight_id=t.flight_id
            WHERE f.airline_name=?
            GROUP BY year, month ORDER BY year, month
        """, (airline,)).fetchall()
        data = {'labels': [f"{r['year']}-{r['month']:02d}" for r in rows],
                'satisfaction': [r['sat'] for r in rows],
                'delay': [r['delay'] for r in rows],
                'ontime': [r['ontime'] for r in rows]}

    elif chart_type == 'airline_comparison':
        for airline in ['Saudia','Flynas','Flyadeal']:
            data[airline] = {
                'ontime': round(get_kpi('airline', airline, 'ontime_rate'),1),
                'satisfaction': round(get_kpi('airline', airline, 'avg_satisfaction'),1),
                'positive': round(get_kpi('airline', airline, 'positive_rate'),1),
                'service': round(get_kpi('airline', airline, 'avg_service'),1),
                'efficiency': round(get_kpi('airline', airline, 'avg_efficiency'),1),
            }

    elif chart_type == 'delay_by_airline':
        rows = conn.execute("""
            SELECT airline_name,
                   SUM(CASE WHEN flight_status='On-time' THEN 1 ELSE 0 END) as ontime,
                   SUM(CASE WHEN flight_status='Delayed' THEN 1 ELSE 0 END) as delayed,
                   SUM(CASE WHEN flight_status='Cancelled' THEN 1 ELSE 0 END) as cancelled
            FROM flights GROUP BY airline_name
        """).fetchall()
        data = {r['airline_name']: {'ontime':r['ontime'],'delayed':r['delayed'],'cancelled':r['cancelled']} for r in rows}

    elif chart_type == 'sentiment_topics':
        rows = conn.execute("""
            SELECT topic, ROUND(AVG(sentiment_score),3) as score, COUNT(*) as cnt
            FROM reviews GROUP BY topic ORDER BY score
        """).fetchall()
        data = {'topics': [r['topic'] for r in rows], 'scores': [r['score'] for r in rows], 'counts': [r['cnt'] for r in rows]}

    conn.close()
    return jsonify(data)


if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print("Database not found. Run init_db.py first.")
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
