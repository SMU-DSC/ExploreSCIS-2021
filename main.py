#!/usr/local/bin/python3

from flask import Flask, request, render_template, make_response, redirect, url_for, jsonify
from flask_sslify import SSLify
from flask_api import status

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity

from argon2 import PasswordHasher
from replit import db
import secrets

app = Flask(__name__, template_folder='templates')
sslify = SSLify(app)

# DO NOT TOUCH THIS TILL SECOND PART OF THE WORKSHOP
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
jwt = JWTManager(app)
ph = PasswordHasher()

# Create an endpoint that allows us to GET objects in the database
@app.route("/", methods=["GET"])
def index():
  user = "INSERT YOUR NAME HERE"

  if request.method == "GET":
    notes_key = 'notes_' + user
    if (notes_key in db.keys()):
      notes = db[notes_key]
    else:
      notes = ""
    return render_template('index.html', user=user, secret_notes=notes)


@app.route("/note", methods=["POST"])
def getNotes():
  user = "INSERT YOUR NAME HERE"

  if request.method == "POST":
    try:
      # Throws an error if key not found
      # Accessing form dictionary value
      notes = request.form['notes']
    except:
      return jsonify({"error": "Data fields are missing"}), status.HTTP_400_BAD_REQUEST
      
    # Insert new entry into database table
    notes_key = "notes_" + user
    db[notes_key] = notes
    return render_template('index.html', user=user, secret_notes=notes, success=True)
# ------------------------------------------------------------------- #

# -----------------------DO NOT TOUCH BELOW---------------------------#
def init_db():
  db['user_admin'] = secrets.randbits(20)
  db['notes_admin'] = "Admin Super Secret. No one must know!"

if __name__ == "__main__":
  init_db()
  app.run(host='0.0.0.0', port=8080)