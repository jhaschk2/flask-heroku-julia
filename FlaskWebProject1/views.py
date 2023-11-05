from datetime import datetime
import email
from flask import flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from FlaskWebProject1 import app
import sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class events(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    title = db.Column("title", db.String(100))
    date = db.Column("date", db.DateTime)
    description = db.Column("description", db.String(1000))
    
    def __init__(self, name, title, date, description):
        self.name = name
        self.title = title
        self.date = date
        self.description = description
        


@app.route('/')
@app.route('/form', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return render_template('form.html')
    
        name = request.form["nm"]
        title = request.form["ttl"]
        date = request.form["dt"]
        description = request.form["desc"]
        
        event = events(name, title, date, description)
        db.session.add(event)
        db.session.commit()

        flash("Event submitted!")
        

    else: 
        return render_template('form.html')
    
if __name__ == "__main__":
    db.create_all()