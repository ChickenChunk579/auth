from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
import hashlib

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    passwordHash = db.Column(db.String, unique=False, nullable=False)

@app.route("/auth/login")
def login():
    user = User.query.filter_by(username=request.args.get("username")).first()
    if user:
        if request.args.get("passwordHash") == user.passwordHash:
            return json.dumps({
                "result": "ok"
            })
        else:
            return json.dumps({
                "result": "fail"
            })
    else :
        return json.dumps({
            "result": "fail"
        })

@app.route("/auth/signup")
def signup():
    newUser = User(username=request.args.get("username"), passwordHash=hashlib.md5(request.args.get("password").encode("utf-8")).hexdigest())
    db.session.add(newUser)
    db.session.commit()

    return json.dumps({
        "result": "ok"
    })

if __name__ == "__main__":
    app.run("0.0.0.0", port=8000, debug=True)