from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import re
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import requests
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '770b0b8509abe280460e773fb9e4cb36c6f8d3271dcfdae3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# API config
HOTELS_API_KEY = "d6b438155amshdd1917f4ad00a2ep17549cjsnaeeefcb25e68 "
HOTELS_API_HOST = "https://serpapi.com/search.json?engine=google_hotels&q=H10+Port+Vell&check_in_date=2025-05-13&check_out_date=2025-05-14&adults=2&currency=USD&gl=us&hl=en"
TELEPORT_API_BASE = "https://api.makcorps.com/citysearch"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class SavedPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    city_name = db.Column(db.String(100), nullable=False)
    city_desc = db.Column(db.Text, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    places = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('saved_plans', lazy=True))

    def get_places(self):
        return json.loads(self.places)

with app.app_context():
    db.create_all()

places_df = pd.read_csv('dataset/Places.csv')

# UTILS
def slugify_city(city):
    return city.lower().replace(" ", "-")

def fetch_city_description(city):
    try:
        slug = slugify_city(city)
        url = TELEPORT_API_BASE.format(city=slug) + "details/"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        summary = data['categories'][0]['data'][0]['string_value']
        return summary
    except:
        return "No city description available."

def fetch_hotel(city, min_price, max_price):
    url = url = "https://serpapi.com/search.json?engine=google_hotels&q=H10+Port+Vell&check_in_date=2025-05-13&check_out_date=2025-05-14&adults=2&currency=USD&gl=us&hl=en"

    querystring = {
        "region_id": "6054439",  # Default India region. Replace with dynamic if needed.
        "locale": "en_US",
        "checkin_date": "2024-12-01",
        "sort_order": "REVIEW",
        "adults_number": "1",
        "domain": "IN",
        "currency": "INR"
    }
    headers = {
        "X-RapidAPI-Key": HOTELS_API_KEY,
        "X-RapidAPI-Host": HOTELS_API_HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        hotels = data.get("properties", [])
        for hotel in hotels:
            price = hotel.get("price", {}).get("lead", {}).get("amount")
            if price and min_price <= float(price) <= max_price:
                return hotel.get("name")
        return "No hotel found within budget."
    except Exception as e:
        return f"API error: {str(e)}"

def truncate_description(description, sentence_limit=2):
    description = re.sub(r'^\"|[\[\]\"]+', '', description)
    sentences = description.split('.')
    return '. '.join(sentences[:sentence_limit]).strip() + '.'

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('indexchatbot.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        city_name = request.form['city_name'].capitalize()
        duration_days = int(request.form['duration_days'])
        budget = float(request.form['budget'])

        city_desc = fetch_city_description(city_name)
        ideal_duration = duration_days
        best_time = "Anytime"

        city_places_df = places_df[places_df['City'].str.lower() == city_name.lower()]
        sorted_city_places_df = city_places_df.sort_values(by='Ratings', ascending=False)
        total_places = duration_days * 3
        top_places_df = sorted_city_places_df.head(total_places)
        places = [top_places_df.iloc[day * 3:(day + 1) * 3].to_dict('records') for day in range(duration_days)]

        min_price = budget * 0.8
        max_price = budget * 1.2
        recommended_hotel = fetch_hotel(city_name, min_price, max_price)

        return render_template(
            'results.html',
            city_name=city_name,
            duration_days=duration_days,
            city_desc=city_desc,
            ideal_duration=ideal_duration,
            best_time=best_time,
            places=places,
            recommended_hotel=recommended_hotel
        )

    return render_template('index.html')

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    city_name = request.form['city_name']
    city_desc = request.form['city_desc']
    duration_days = int(request.form['duration_days'])
    places = request.form.getlist('places[]')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    elements.append(Paragraph(f"Trip Plan for {city_name}", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Description: {city_desc}", normal_style))
    elements.append(Spacer(1, 12))

    for i, place in enumerate(places, 1):
        elements.append(Paragraph(f"{i}. {place}", normal_style))
        elements.append(Spacer(1, 12))
        if len(elements) > 30:
            elements.append(PageBreak())

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"{city_name}_trip.pdf", mimetype='application/pdf')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))



@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    saved_plans = SavedPlan.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user_name=user.username, user_email=user.email, saved_plans=[{
        'id': plan.id,
        'city_name': plan.city_name,
        'city_desc': plan.city_desc,
        'duration_days': plan.duration_days,
        'places': plan.get_places()
    } for plan in saved_plans])

@app.route('/save_plan', methods=['POST'])
def save_plan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    city_name = request.form['city_name']
    city_desc = request.form['city_desc']
    duration_days = int(request.form['duration_days'])
    places = request.form.getlist('places[]')

    new_plan = SavedPlan(
        user_id=session['user_id'],
        city_name=city_name,
        city_desc=city_desc,
        duration_days=duration_days,
        places=json.dumps(places)
    )
    db.session.add(new_plan)
    db.session.commit()
    return redirect(url_for('profile'))

@app.route('/delete_plan/<int:plan_id>', methods=['POST'])
def delete_plan(plan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    plan = SavedPlan.query.get(plan_id)
    if plan and plan.user_id == session['user_id']:
        db.session.delete(plan)
        db.session.commit()
    return redirect(url_for('profile'))

@app.route('/discover_more')
def discover_more():
    return render_template('discover_more.html')

if __name__ == '__main__':
    app.run(debug=True)
