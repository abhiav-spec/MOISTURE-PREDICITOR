from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

# Basic prediction logic (same as used to generate the dataset)
def predict_moisture(temp, humidity, soil_type, rainfall, wind_speed, sunlight, irrigation):
    base_moisture = 50 + rainfall * 2 - sunlight * 1.5 - wind_speed * 0.5

    if soil_type == 'Clayey':
        base_moisture += 5
    elif soil_type == 'Sandy':
        base_moisture -= 5

    if irrigation == 'Yes':
        base_moisture += 10

    base_moisture += (humidity - 50) * 0.2
    base_moisture = max(0, min(100, round(base_moisture, 1)))
    return base_moisture

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        temp = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        soil_type = request.form['soilType']
        rainfall = float(request.form['rainfall'])
        wind_speed = float(request.form['windSpeed'])
        sunlight = float(request.form['sunlight'])
        irrigation = request.form['irrigation']

        moisture = predict_moisture(temp, humidity, soil_type, rainfall, wind_speed, sunlight, irrigation)
        print(moisture)

        return render_template('index.html', moisture=moisture)

    return render_template('index.html', moisture=None)

if __name__ == '__main__':
    app.run(debug=True)
