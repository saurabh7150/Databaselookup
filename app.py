from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_BASE = "https://api-rc-cibil-ei8h.onrender.com"

@app.route('/hello')
def home():
    return "Welcome to the Lookup Portal!"

@app.route('/', methods=['GET', 'POST'])
def car_lookup():
    today_cars = None
    car_data = None
    cibil_data = None
    pan_data = None
    error = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'car':
            id_number = request.form.get('id_number')
            if id_number:
                try:
                    response = requests.get(f"{API_BASE}/get_car", params={'id_number': id_number})
                    if response.status_code == 200:
                        car_data = response.json().get('data')
                    else:
                        error = response.json().get('message') or response.json().get('error')
                except Exception as e:
                    error = f"Error calling get_car: {str(e)}"
            else:
                error = "Please provide an ID number."

        elif action == 'cibil':
            pan = request.form.get('pan')
            if pan:
                try:
                    response = requests.get(f"{API_BASE}/get_cibil", params={'pan': pan})
                    if response.status_code == 200:
                        cibil_data = response.json().get('data')
                    else:
                        error = response.json().get('message') or response.json().get('error')
                except Exception as e:
                    error = f"Error calling get_cibil: {str(e)}"
            else:
                error = "Please provide a PAN."

        elif action == 'pan':
            mobile = request.form.get('mobile')
            if mobile:
                try:
                    response = requests.get(f"{API_BASE}/get_pan_by_mobile", params={'mobile': mobile})
                    if response.status_code == 200:
                        pan_data = response.json()
                    else:
                        error = response.json().get('message') or response.json().get('error')
                except Exception as e:
                    error = f"Error calling get_pan_by_mobile: {str(e)}"
            else:
                error = "Please provide a mobile number."
        elif action == 'today_cars':
            try:
                response = requests.get(f"{API_BASE}/get_today_cars")
                if response.status_code == 200:
                    today_cars = response.json().get("data", [])
                    if not today_cars:
                        error = "No car records found for today."
                else:
                    error = response.json().get("error")
            except Exception as e:
                error = f"Error calling get_today_cars: {str(e)}"
        

    return render_template(
    'car_lookup.html',
    car_data=car_data,
    cibil_data=cibil_data,
    pan_data=pan_data,
    today_cars=today_cars,
    error=error
)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
