from flask import Flask, request, jsonify
from config import Config
from model import mongo, object_id_to_str

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo.init_app(app)

# User APIs
@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "contact_number": data.get("contact_num")
    }
    result = mongo.db.users.insert_one(new_user)
    new_user["_id"] = str(result.inserted_id)
    return jsonify(new_user), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = mongo.db.users.find_one({"email": data.get("email")})
    if user:
        return jsonify(object_id_to_str(user)), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    if user:
        return jsonify(object_id_to_str(user)), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<string:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    update_fields = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "contact_number": data.get("contact_num")
    }
    mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
    return jsonify({"message": "User updated"}), 200

@app.route('/user/<string:id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "User deleted"}), 204

# Question APIs
@app.route('/question', methods=['POST'])
def add_question():
    data = request.json
    new_question = {"question_text": data.get("question_text")}
    result = mongo.db.questions.insert_one(new_question)
    new_question["_id"] = str(result.inserted_id)
    return jsonify(new_question), 201

@app.route('/question/<string:id>', methods=['GET'])
def get_question(id):
    question = mongo.db.questions.find_one({"_id": ObjectId(id)})
    if question:
        return jsonify(object_id_to_str(question)), 200
    return jsonify({"message": "Question not found"}), 404

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = mongo.db.questions.find()
    return jsonify([object_id_to_str(q) for q in questions]), 200

# Alternatives APIs
@app.route('/question/<string:question_id>/alternative', methods=['POST'])
def add_alternative(question_id):
    data = request.json
    new_alternative = {
        "question_id": question_id,
        "alternative_text": data.get("alternative_text")
    }
    result = mongo.db.alternatives.insert_one(new_alternative)
    new_alternative["_id"] = str(result.inserted_id)
    return jsonify(new_alternative), 201

@app.route('/question/<string:question_id>/alternatives', methods=['GET'])
def get_alternatives(question_id):
    alternatives = mongo.db.alternatives.find({"question_id": question_id})
    return jsonify([object_id_to_str(a) for a in alternatives]), 200

# Other CRUD endpoints for `Card`, `Score`, `HistoryQuestion`, etc., would follow the same pattern.

if __name__ == '__main__':
    app.run(debug=True)