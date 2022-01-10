from flask import Flask, render_template, session
from user_controller import user_controller

app = Flask(__name__)
app.register_blueprint(user_controller)
app.secret_key = 'MyFlaskWebAppKey'


@app.route('/')
def home():
    user = session['user_id']
    return render_template('home.html', user=user)


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/login')
def login_page():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(port=5001,debug=True)
