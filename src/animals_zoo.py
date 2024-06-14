from flask import Blueprint, request, jsonify
from repository import animal, tokens
from flasgger import swag_from

animals_blueprint = Blueprint("animal", __name__, url_prefix="/animal")

# Inisialisasi ID untuk hewan
next_id = 1

@animals_blueprint.before_request
def authenticate():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Login required"}), 401

    username = tokens.get(token)
    if not username:
        return jsonify({"message": "Login required"}), 401

    print(f"Authenticated user: {username}")

    request.username = username

@animals_blueprint.route("/add", methods=["POST"])
@swag_from("docs/add_animal.yml")
def post_animal():
    global next_id
    animal_data = request.json.get("animal")
    if not animal_data:
        return jsonify({"message": "Animal required"}), 400
    
    username = getattr(request, "username", "anonymous")
    animal_entry = {
        "id": next_id,
        "username": username,
        "animal": animal_data
    }
    animal.append(animal_entry)
    next_id += 1
    return jsonify({"message": "Animal added", "id": animal_entry["id"]}), 201

@animals_blueprint.route("/list", methods=["GET"])
@swag_from("docs/list_animals.yml")
def get_animal():
    return jsonify(animal), 200

@animals_blueprint.route("/get/<int:animal_id>", methods=["GET"])
@swag_from("docs/id_animals.yml")
def get_animal_id(animal_id):
    detail_animal = next((zoo for zoo in animal if zoo.get("id") == animal_id), None)
    if detail_animal:
        return jsonify(detail_animal), 200
    else:
        return jsonify({"message": "Animal not found"}), 404

@animals_blueprint.route("/delete/<int:animal_id>", methods=["DELETE"])
@swag_from("docs/delete_animal.yml")
def delete_animal(animal_id):
    global next_id
    detail_animal = next((zoo for zoo in animal if zoo.get("id") == animal_id), None)
    if detail_animal:
        animal.remove(detail_animal)
        # Atur ulang ID
        animal.sort(key=lambda x: x['id'])  # Sortir berdasarkan ID untuk menjaga urutan
        for index, zoo in enumerate(animal, start=1):
            zoo['id'] = index
        next_id = len(animal) + 1  # Setel next_id ke ID berikutnya yang tersedia
        return jsonify({"message": "Animal deleted"}), 200
    else:
        return jsonify({"message": "Animal not found"}), 404

@animals_blueprint.route("/update/<int:animal_id>", methods=["PUT"])
@swag_from("docs/update_animal.yml")
def update_animal(animal_id):
    animal_data = request.json.get("animal")
    if not animal_data:
        return jsonify({"message": "Animal required"}), 400
    
    detail_animal = next((zoo for zoo in animal if zoo.get("id") == animal_id), None)
    if detail_animal:
        detail_animal["animal"] = animal_data
        return jsonify({"message": "Animal updated"}), 200
    else:
        return jsonify({"message": "Animal not found"}), 404
