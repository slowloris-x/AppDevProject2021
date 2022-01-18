from flask import Flask, render_template, session
from user_controller import user_controller
from inventory_controller import inventory_controller

app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(inventory_controller)
app.secret_key = 'MyFlaskWebAppKey'

@app.before_first_request
def before_first_request():
    session.clear()

@app.route('/')
def home():
    if session:
        user = session['user_id']
    else:
        user = None
    return render_template('home.html', user=user)


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/login')
def login_page():
    return render_template('login.html')



if __name__ == '__main__':
    app.run(port=5001,debug=True)
