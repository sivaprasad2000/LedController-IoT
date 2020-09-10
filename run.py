from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Brightness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, unique=True, nullable=False)

db.drop_all()
db.create_all()

brightnessInitial = Brightness(value=50)
db.session.add(brightnessInitial)
db.session.commit()

@app.route('/', methods=['POST','GET'])
def mainpage():
    bright = Brightness.query.first()
    return render_template('index.html', initialB=bright.value)

@app.route('/change', methods=['POST','GET'])
def change():
    bright = Brightness.query.first()
    bright.value = request.form['brightness']
    db.session.add(bright)
    db.session.commit()
    print(bright.value)
    return bright.value

@app.route('/api', methods=['POST','GET'])
def api():
    bright = Brightness.query.first()
    return str(bright.value)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')