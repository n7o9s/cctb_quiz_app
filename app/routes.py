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
    new_user = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "number": data.get("number"),
        "email": data.get("email"),
        "password": data.get("password")
    }
    result = mongo.db.User.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    return jsonify(new_user), 201

@main.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = mongo.db.User.find_one({"email": data.get("email")})
    if user:
        return jsonify(object_id_to_str(user)), 200
    return jsonify({"message": "User not found"}), 404

@main.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    user = mongo.db.User.find_one({"_id": ObjectId(str(id))})
    if user:
        return jsonify(object_id_to_str(user)), 200
    return jsonify({"message": "User not found"}), 404

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
    mongo.db.User.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    return jsonify({"message": "User updated"}), 200

@main.route('/user/<string:id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.User.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "User deleted"}), 204

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