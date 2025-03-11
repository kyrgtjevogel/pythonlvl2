from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['POST'])
def forecast():
    country = request.form.get('country')
    city = request.form.get('city')

    api_key = '0d92fb02309b4cb58cc103229242711'  # Vervang dit met je eigen API-sleutel

    # API-aanroep URL
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city},{country}&days=3'
    response = requests.get(url)
    data = response.json()

    # Haal de weersvoorspelling voor 3 dagen uit de JSON
    forecast_days = data['forecast']['forecastday']

    # Converteer de datum naar de dag van de week in het Nederlands
    dagen_nederlands = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
    for day in forecast_days:
        date_object = datetime.datetime.strptime(day['date'], "%Y-%m-%d")
        day_of_week = date_object.weekday()  # Krijg een integer (0=maandag, 6=zondag)
        day['day_of_week'] = dagen_nederlands[day_of_week]  # Voeg de dag in het Nederlands toe aan de data

    return render_template('forecast.html', country=country, city=city, forecast_days=forecast_days)

if __name__ == '__main__':
    app.run(debug=True)
