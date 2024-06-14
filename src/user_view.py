from flask import Blueprint, request, jsonify
from uuid import uuid4
from repository import users, tokens
from flasgger import swag_from

user_blueprint = Blueprint("user", __name__, url_prefix="/user")


@user_blueprint.route("register", methods=["POST"])
@swag_from("docs/user_registration.yml")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = password
    return jsonify({"message": "User created"}), 201


@user_blueprint.route("/login", methods=["POST"])
@swag_from("docs/user_login.yml")
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if users.get(username) != password:
        return jsonify({"message": "Invalid username or password"}), 401

    token = str(uuid4())
    tokens[token] = username
    return jsonify({"message": "Logged in", "token": token}), 200
