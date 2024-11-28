from flask import Blueprint, request, jsonify
from bson import ObjectId
from .db.mongo import mongo, object_id_to_str

main = Blueprint('main', __name__)

@main.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, Flask!"})

# 'GET All' APIs
@main.route('/users', methods=['GET'])
def get_all_users():
    users = mongo.db.User.find()  # Get all users from the User collection
    users_list = [object_id_to_str(user) for user in users]  # Convert ObjectId to string for each user
    return jsonify(users_list), 200

@main.route('/questions', methods=['GET'])
def get_all_questions():
    questions = mongo.db.Question.find()  # Get all questions from the User collection
    questions_list = [object_id_to_str(question) for question in questions]  # Convert ObjectId to string for each question
    return jsonify(questions_list), 200

# User APIs

@main.route('/user', methods=['POST'])
def add_user():
    data = request.json
    
    # Check if first_name, last_name, number, email and password are in the request
    if not data or 'first_name' not in data or 'last_name' not in data or 'number' not in data or 'email' not in data or 'first_name' not in data or 'password' not in data:
        return jsonify({"message": "First Name, Last Name, Number, Email and Paswword are required."}), 400

    new_user = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "number": data["number"],
        "email": data["email"],
        "password": data["password"]
    }

    new_user = mongo.db.User.insert_one(new_user)
    user = mongo.db.User.find_one({"email": data['email']})
    user.pop("password", None)  # Remove password from the dictionary

    return jsonify({"message": "Create account successful.", "data": object_id_to_str(user)}), 201

@main.route('/login', methods=['POST'])
def login_user():
    data = request.json

    # Check if email and password are in the request
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"message": "Email and password are required"}), 400

    reqEmail = data['email']
    reqPassword = data['password']

    # Fetch user from the database
    user = mongo.db.User.find_one({"email": reqEmail})
    if user:
        # Check the password
        if (user['password'] == reqPassword):
            # Successful login
            user.pop("password", None)  # Remove password from the dictionary
            return jsonify({"message": "Login successful.", "data": object_id_to_str(user)}), 200
        else:
            return jsonify({"message": "Invalid credentials."}), 401
    else:
        return jsonify({"message": "Invalid credentials."}), 401

@main.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    try:
        user = mongo.db.User.find_one({"_id": ObjectId(id)})
        if user:
            return jsonify(object_id_to_str(user)), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route('/user/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    update_fields = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "number": data.get("number"),
        "email": data.get("email"),
        "password": data.get("password")
    }
    result = mongo.db.User.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User updated"}), 200

@main.route('/user/<string:id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.User.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200
# Question APIs
@main.route('/question', methods=['POST'])
def add_question():
    data = request.json
    new_question = {
        "question": data.get("question"),
        "answerA": data.get("answerA"),
        "answerB": data.get("answerB"),
        "answerC": data.get("answerC"),
        "answerD": data.get("answerD"),
        "correctAnswer": data.get("correctAnswer")
    }
    result = mongo.db.Question.insert_one(new_question)
    new_question["_id"] = str(result.inserted_id)
    return jsonify(new_question), 201

@main.route('/question/<string:id>', methods=['GET'])
def get_question(id):
    question = mongo.db.Question.find_one({"_id": ObjectId(id)})
    if question:
        return jsonify(object_id_to_str(question)), 200
    return jsonify({"message": "Question not found"}), 404

@main.route('/question/<string:id>', methods=['PUT'])
def update_question(id):
    data = request.json
    update_fields = {
        "question": data.get("question"),
        "answerA": data.get("answerA"),
        "answerB": data.get("answerB"),
        "answerC": data.get("answerC"),
        "answerD": data.get("answerD"),
        "correctAnswer": data.get("correctAnswer")
    }
    result = mongo.db.Question.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

    if result.matched_count == 0:
        # If no document was matched, return a 404 error
        return jsonify({"error": "Question not found"}), 404
    
    return jsonify({"message": "Question updated"}), 200

@main.route('/question/<string:id>', methods=['DELETE'])
def delete_question(id):
    result = mongo.db.Question.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        # If no document was deleted, return a 404 error
        return jsonify({"error": "Question not found"}), 404
    
    return jsonify({"message": "Question deleted"}), 200