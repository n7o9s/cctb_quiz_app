from model import User, Question, Alternative, Card, Score, HistoryQuestion, db
from config import Config
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# User APIs
@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        contact_number=data.get('contact_num')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.contact_number = data.get('contact_num', user.contact_number)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 204

# Question APIs
@app.route('/question', methods=['POST'])
def add_question():
    data = request.json
    new_question = Question(question_text=data.get('question_text'))
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"id": new_question.id}), 201

@app.route('/question/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get_or_404(id)
    return jsonify({"id": question.id, "question_text": question.question_text})

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{"id": q.id, "question_text": q.question_text} for q in questions])

@app.route('/question/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get_or_404(id)
    data = request.json
    question.question_text = data.get('question_text', question.question_text)
    db.session.commit()
    return jsonify({"id": question.id, "question_text": question.question_text})

@app.route('/question/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get_or_404(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted"}), 204

# Alternatives APIs
@app.route('/question/<int:question_id>/alternative', methods=['POST'])
def add_alternative(question_id):
    data = request.json
    new_alternative = Alternative(
        question_id=question_id,
        alternative_text=data.get('alternative_text')
    )
    db.session.add(new_alternative)
    db.session.commit()
    return jsonify({"id": new_alternative.id}), 201

@app.route('/question/<int:question_id>/alternatives', methods=['GET'])
def get_alternatives(question_id):
    alternatives = Alternative.query.filter_by(question_id=question_id).all()
    return jsonify([{"id": a.id, "alternative_text": a.alternative_text} for a in alternatives])

@app.route('/alternative/<int:id>', methods=['PUT'])
def update_alternative(id):
    alternative = Alternative.query.get_or_404(id)
    data = request.json
    alternative.alternative_text = data.get('alternative_text', alternative.alternative_text)
    db.session.commit()
    return jsonify({"id": alternative.id, "alternative_text": alternative.alternative_text})

@app.route('/alternative/<int:id>', methods=['DELETE'])
def delete_alternative(id):
    alternative = Alternative.query.get_or_404(id)
    db.session.delete(alternative)
    db.session.commit()
    return jsonify({"message": "Alternative deleted"}), 204

# Cards APIs
@app.route('/quiz/<int:quiz_id>/cards', methods=['GET'])
def get_quiz_cards(quiz_id):
    cards = Card.query.filter_by(question_id=quiz_id).all()
    return jsonify([{"id": c.id} for c in cards])

@app.route('/card/<int:id>', methods=['GET'])
def get_card(id):
    card = Card.query.get_or_404(id)
    return jsonify({"id": card.id, "question_id": card.question_id})

@app.route('/card', methods=['POST'])
def add_card():
    data = request.json
    new_card = Card(question_id=data.get('question_id'))
    db.session.add(new_card)
    db.session.commit()
    return jsonify({"id": new_card.id}), 201

@app.route('/card/<int:id>', methods=['PUT'])
def update_card(id):
    card = Card.query.get_or_404(id)
    data = request.json
    card.question_id = data.get('question_id', card.question_id)
    db.session.commit()
    return jsonify({"id": card.id, "question_id": card.question_id})

@app.route('/card/<int:id>', methods=['DELETE'])
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({"message": "Card deleted"}), 204

# Score APIs
@app.route('/score', methods=['POST'])
def add_score():
    data = request.json
    new_score = Score(
        user_id=data.get('user_id'),
        quiz_id=data.get('quiz_id')
    )
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"id": new_score.id}), 201

@app.route('/score/user/<int:user_id>', methods=['GET'])
def get_user_scores(user_id):
    scores = Score.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": s.id, "quiz_id": s.quiz_id} for s in scores])

@app.route('/score/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz_scores(quiz_id):
    scores = Score.query.filter_by(quiz_id=quiz_id).all()
    return jsonify([{"id": s.id, "user_id": s.user_id} for s in scores])

# HistoryQuestion APIs
@app.route('/historyQuestion', methods=['POST'])
def add_history_question():
    data = request.json
    new_history_question = HistoryQuestion(
        user_id=data.get('user_id'),
        question_id=data.get('question_id')
    )
    db.session.add(new_history_question)
    db.session.commit()
    return jsonify({"id": new_history_question.id}), 201

@app.route('/historyQuestion/user/<int:user_id>', methods=['GET'])
def get_user_history_questions(user_id):
    history_questions = HistoryQuestion.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": hq.id, "question_id": hq.question_id} for hq in history_questions])

if __name__ == '__main__':
    app.run(debug=True)
