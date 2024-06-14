from flask import Blueprint, request, jsonify
from repository import employee, tokens
from flasgger import swag_from

employee_blueprint = Blueprint("employee", __name__, url_prefix="/employee")

# Inisialisasi ID untuk karyawan
next_id = 1

@employee_blueprint.before_request
def authenticate():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Login required"}), 401

    username = tokens.get(token)
    if not username:
        return jsonify({"message": "Login required"}), 401

    print(f"Authenticated user: {username}")

    request.username = username

@employee_blueprint.route("/add", methods=["POST"])
@swag_from("docs/add_employee.yml")
def post_employee():
    global next_id
    employee_data = request.json.get("employee")
    if not employee_data:
        return jsonify({"message": "employee required"}), 400
    
    username = getattr(request, "username", "anonymous")
    employee_entry = {
        "id": next_id,
        "username": username,
        "employee": employee_data
    }
    employee.append(employee_entry)
    next_id += 1
    return jsonify({"message": "employee added", "id": employee_entry["id"]}), 201

@employee_blueprint.route("/list", methods=["GET"])
@swag_from("docs/list_employee.yml")
def get_employee():
    return jsonify(employee), 200

@employee_blueprint.route("/get/<int:employee_id>", methods=["GET"])
@swag_from("docs/id_employee.yml")
def get_employee_id(employee_id):
    detail_employee = next((zoo for zoo in employee if zoo.get("id") == employee_id), None)
    if detail_employee:
        return jsonify(detail_employee), 200
    else:
        return jsonify({"message": "employee not found"}), 404

@employee_blueprint.route("/delete/<int:employee_id>", methods=["DELETE"])
@swag_from("docs/delete_employee.yml")
def delete_employee(employee_id):
    global next_id
    detail_employee = next((zoo for zoo in employee if zoo.get("id") == employee_id), None)
    if detail_employee:
        employee.remove(detail_employee)
        # Atur ulang ID
        employee.sort(key=lambda x: x['id'])  # Sortir berdasarkan ID untuk menjaga urutan
        for index, zoo in enumerate(employee, start=1):
            zoo['id'] = index
        next_id = len(employee) + 1  # Setel next_id ke ID berikutnya yang tersedia
        return jsonify({"message": "employee deleted"}), 200
    else:
        return jsonify({"message": "employee not found"}), 404

@employee_blueprint.route("/update/<int:employee_id>", methods=["PUT"])
@swag_from("docs/update_employee.yml")
def update_employee(employee_id):
    employee_data = request.json.get("employee")
    if not employee_data:
        return jsonify({"message": "employee required"}), 400
    
    detail_employee = next((zoo for zoo in employee if zoo.get("id") == employee_id), None)
    if detail_employee:
        detail_employee["employee"] =employee_data
        return jsonify({"message": "employee updated"}), 200
    else:
        return jsonify({"message": "employee not found"}), 404