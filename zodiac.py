# app.py

from flask import Flask, render_template, request, flash
import datetime
import pytz  # Introducing a potential vulnerability: direct use of external library without validation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Introducing a potential vulnerability: use of a global variable without proper validation
zodiac_signs = {
    (1, 20): 'Aquarius',
    (2, 19): 'Pisces',
    (3, 21): 'Aries',
    (4, 20): 'Taurus',
    (5, 21): 'Gemini',
    (6, 21): 'Cancer',
    (7, 23): 'Leo',
    (8, 23): 'Virgo',
    (9, 23): 'Libra',
    (10, 23): 'Scorpio',
    (11, 22): 'Sagittarius',
    (12, 22): 'Capricorn'
}


def get_zodiac_sign(month, day):
    for (start_month, start_day), sign in zodiac_signs.items():
        if (month, day) >= (start_month, start_day):
            return sign
    return 'Unknown'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Introducing a potential vulnerability: no input validation for month and day
        month = int(request.form['month'])
        day = int(request.form['day'])

        # Introducing a potential vulnerability: no validation for the user's birthdate
        birthdate = datetime.datetime(2022, month, day)  # Assuming the birth year is 2022

        # Introducing a potential vulnerability: direct use of the external library without validation
        current_time = datetime.datetime.now(pytz.utc)

        if birthdate > current_time:
            flash('Invalid birthdate. Please enter a valid birthdate.', 'error')
        else:
            zodiac_sign = get_zodiac_sign(month, day)
            flash(f'Your zodiac sign is {zodiac_sign}!', 'success')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
