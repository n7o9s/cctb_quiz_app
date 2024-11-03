import os
import json
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from models import Question, HistoryQuestion, User, Score
from datetime import datetime


# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

sample_questions = [
    {
        "question": "What does 'SUV' stand for?",
        "answerA": "Super Utility Vehicle",
        "answerB": "Sport Utility Vehicle",
        "answerC": "Standard Utility Vehicle",
        "answerD": "Speed Utility Vehicle",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which company produces the Corvette?",
        "answerA": "Ford",
        "answerB": "Chevrolet",
        "answerC": "Dodge",
        "answerD": "Toyota",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does the 'GT' in Ford GT stand for?",
        "answerA": "Grand Touring",
        "answerB": "General Transport",
        "answerC": "Giant Turbo",
        "answerD": "Grand Test",
        "correctAnswer": "answerA"
    },
    {
        "question": "What country is the car manufacturer Toyota from?",
        "answerA": "South Korea",
        "answerB": "Germany",
        "answerC": "Japan",
        "answerD": "China",
        "correctAnswer": "answerC"
    },
    {
        "question": "Which car brand uses a prancing horse as its logo?",
        "answerA": "Porsche",
        "answerB": "Ferrari",
        "answerC": "Lamborghini",
        "answerD": "Maserati",
        "correctAnswer": "answerB"
    },
    {
        "question": "What is the fastest production car in the world (as of 2023)?",
        "answerA": "Bugatti Chiron Super Sport 300+",
        "answerB": "Koenigsegg Jesko Absolut",
        "answerC": "Tesla Model S Plaid",
        "answerD": "SSC Tuatara",
        "correctAnswer": "answerD"
    },
    {
        "question": "What was the first car ever made?",
        "answerA": "Model T",
        "answerB": "Mercedes-Benz Patent Motorwagen",
        "answerC": "Rolls-Royce Silver Ghost",
        "answerD": "Ford Mustang",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which company produces the car model 'Mustang'?",
        "answerA": "Dodge",
        "answerB": "Ford",
        "answerC": "Chevrolet",
        "answerD": "Nissan",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does ABS stand for in car terminology?",
        "answerA": "Automated Braking System",
        "answerB": "Anti-lock Braking System",
        "answerC": "Auto-Balancing System",
        "answerD": "All-wheel Braking System",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which type of engine is the most common in sports cars?",
        "answerA": "V6",
        "answerB": "V8",
        "answerC": "Inline-4",
        "answerD": "V12",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which country is home to the car manufacturer Volvo?",
        "answerA": "Norway",
        "answerB": "Sweden",
        "answerC": "Finland",
        "answerD": "Germany",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does the 'T' in Tesla Model S stand for?",
        "answerA": "Turbo",
        "answerB": "Technology",
        "answerC": "Tesla",
        "answerD": "Traction",
        "correctAnswer": "answerC"
    },
    {
        "question": "What is the most popular car color worldwide?",
        "answerA": "White",
        "answerB": "Black",
        "answerC": "Red",
        "answerD": "Blue",
        "correctAnswer": "answerA"
    },
    {
        "question": "Which car manufacturer is known for the Beetle?",
        "answerA": "Fiat",
        "answerB": "Volkswagen",
        "answerC": "Honda",
        "answerD": "BMW",
        "correctAnswer": "answerB"
    },
    {
        "question": "What year did the Ford Mustang debut?",
        "answerA": "1959",
        "answerB": "1964",
        "answerC": "1970",
        "answerD": "1980",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does 'EV' stand for in the automotive industry?",
        "answerA": "Electric Vehicle",
        "answerB": "Engine Vehicle",
        "answerC": "Eco Vehicle",
        "answerD": "Enhanced Vehicle",
        "correctAnswer": "answerA"
    },
    {
        "question": "Which car company produces the 911 model?",
        "answerA": "Audi",
        "answerB": "Porsche",
        "answerC": "BMW",
        "answerD": "Mercedes-Benz",
        "correctAnswer": "answerB"
    },
    {
        "question": "What is the luxury brand of Toyota?",
        "answerA": "Lexus",
        "answerB": "Infiniti",
        "answerC": "Acura",
        "answerD": "Cadillac",
        "correctAnswer": "answerA"
    },
    {
        "question": "Which type of drivetrain is designed for all four wheels to receive power simultaneously?",
        "answerA": "FWD",
        "answerB": "RWD",
        "answerC": "AWD",
        "answerD": "2WD",
        "correctAnswer": "answerC"
    },
    {
        "question": "What is the purpose of a turbocharger in a car?",
        "answerA": "Increase fuel efficiency",
        "answerB": "Increase engine power",
        "answerC": "Reduce emissions",
        "answerD": "Improve handling",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which car brand’s logo consists of four interlocked rings?",
        "answerA": "BMW",
        "answerB": "Audi",
        "answerC": "Infiniti",
        "answerD": "Subaru",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does the term 'MPG' stand for in car fuel efficiency?",
        "answerA": "Miles per Gallon",
        "answerB": "Motor Power Gauge",
        "answerC": "Maximum Performance Grade",
        "answerD": "Mileage per Gear",
        "correctAnswer": "answerA"
    },
    {
        "question": "What was the first mass-produced electric car?",
        "answerA": "Tesla Roadster",
        "answerB": "Nissan Leaf",
        "answerC": "Chevrolet Volt",
        "answerD": "Toyota Prius",
        "correctAnswer": "answerB"
    },
    {
        "question": "What is the car model 'Civic' made by?",
        "answerA": "Honda",
        "answerB": "Toyota",
        "answerC": "Ford",
        "answerD": "Hyundai",
        "correctAnswer": "answerA"
    },
    {
        "question": "What is the legal blood alcohol limit for driving in most countries?",
        "answerA": "0.05%",
        "answerB": "0.08%",
        "answerC": "0.10%",
        "answerD": "0.12%",
        "correctAnswer": "answerB"
    },
    {
        "question": "What does the 'M' in BMW M series stand for?",
        "answerA": "Manual",
        "answerB": "Motorsport",
        "answerC": "Mechanic",
        "answerD": "Model",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which country is the brand Hyundai from?",
        "answerA": "Japan",
        "answerB": "China",
        "answerC": "South Korea",
        "answerD": "Germany",
        "correctAnswer": "answerC"
    },
    {
        "question": "What type of fuel do most Formula 1 cars use?",
        "answerA": "Diesel",
        "answerB": "Unleaded gasoline",
        "answerC": "Ethanol",
        "answerD": "Specialized fuel blends",
        "correctAnswer": "answerD"
    },
    {
        "question": "Which car is considered the first supercar?",
        "answerA": "Lamborghini Miura",
        "answerB": "Ferrari 250 GTO",
        "answerC": "Bugatti Veyron",
        "answerD": "Porsche 959",
        "correctAnswer": "answerA"
    },
    {
        "question": "What is a hybrid car?",
        "answerA": "A car with both a gas and diesel engine",
        "answerB": "A car that runs on gasoline and electricity",
        "answerC": "A car with interchangeable engines",
        "answerD": "A car that uses two types of fuel",
        "correctAnswer": "answerB"
    },
    {
        "question": "In which country did the 'Autobahn,' a highway with no speed limit, originate?",
        "answerA": "France",
        "answerB": "Italy",
        "answerC": "Germany",
        "answerD": "Switzerland",
        "correctAnswer": "answerC"
    }
]

sample_users = [
    {
        "first_name": "Alice",
        "last_name": "Smith",
        "number": "111-222-3333",
        "email": "alice.smith@example.com",
        "password": "Alice123"
    },
    {
        "first_name": "Bob",
        "last_name": "Johnson",
        "number": "444-555-6666",
        "email": "bob.johnson@example.com",
        "password": "Bob123"
    },
    {
        "first_name": "Charlie",
        "last_name": "Brown",
        "number": "777-888-9999",
        "email": "charlie.brown@example.com",
        "password": "Charlie123"
    }
]

sample_history_questions = [
    {
        "questions": [
            {
                "question_id": "6722e893fd70ca83b44d1e2a",
                "chosenAnswer": "answerB"
            },
            {
                "question_id": "6722e893fd70ca83b44d1e2b",
                "chosenAnswer": "answerC"
            }
        ]
    },
    {
        "questions": [
            {
                "question_id": "6722e893fd70ca83b44d1e2a",
                "chosenAnswer": "answerB"
            },
            {
                "question_id": "6722e893fd70ca83b44d1e2b",
                "chosenAnswer": "answerB"
            }
        ]
    },
    {
        "questions": [
            {
                "question_id": "6722e893fd70ca83b44d1e2a",
                "chosenAnswer": "answerD"
            },
            {
                "question_id": "6722e893fd70ca83b44d1e2b",
                "chosenAnswer": "answerA"
            }
        ]
    }
]

sample_scores = [
    {
        "score": [
            {
                "date": datetime.now(),
                "value": "10/50"
            }
        ]
    },
    {
        "score": [
            {
                "date": datetime.now(),
                "value": "48/50"
            }
        ]
    },
    {
        "score": [
            {
                "date": datetime.now(),
                "value": "37/50"
            }
        ]
    }
]

def seed_questions(client):
    """Insert sample questions into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    question_collection = db.Question   # Get the question collection

    # Clear the existing documents in the collection
    question_collection.delete_many({})  # Remove all documents

    # Insert sample questions in the database using the Question model
    questions_to_insert = [Question(**data) for data in sample_questions]
    inserted_ids = question_collection.insert_many([question.get() for question in questions_to_insert]).inserted_ids

    print(f"Seeded {len(sample_questions)} questions into Question collection.")
    return inserted_ids # Return list of question ObjectIds

def seed_users(client):
    """Insert sample users into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    user_collection = db.User   # Get the User collection

    # Clear the existing documents in the collection
    user_collection.delete_many({})  # Remove all documents

    # Insert sample questions in the database using the User model
    users_to_insert = [User(**data) for data in sample_users]
    inserted_ids = user_collection.insert_many([user.get() for user in users_to_insert]).inserted_ids

    print(f"Seeded {len(sample_users)} users into User collection.")
    return inserted_ids # Return list of user ObjectIds

def seed_score(client, user_ids):
    """Insert sample score into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    score_collection = db.Score   # Get the Score collection

    # Clear the existing documents in the collection
    score_collection.delete_many({})  # Remove all documents

    # Insert sample history questions in the database using the HistoryQuestion model
    scores_to_insert = []
    """for data in sample_scores:
        # Create a new Score instance for each entry
        score_entry = Score(
            user_id=ObjectId(data["user_id"]),
            score=data["score"]
        )
        scores_to_insert.append(score_entry)"""
    
    scores_to_insert = [
        Score(user_id=user_ids[i], score=sample_scores[i]["score"]) for i in range(len(sample_scores))
    ]

    # Insert the scores into the database
    score_collection.insert_many([score.get() for score in scores_to_insert])

    print(f"Seeded {len(sample_scores)} scores into Score collection.")

def seed_history(client, user_ids, question_ids):
    """Insert sample history into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    history_collection = db.HistoryQuestion   # Get the HistoryQuestion collection

    # Clear the existing documents in the collection
    history_collection.delete_many({})  # Remove all documents

    # Insert sample history questions in the database using the HistoryQuestion model
    histories_to_insert = []
    """for data in sample_history_questions:
        # Create a new HistoryQuestion instance for each entry
        history_entry = HistoryQuestion(
            user_id=ObjectId(data["user_id"]),
            questions=data["questions"]
        )
        histories_to_insert.append(history_entry)"""
    
    for i, user_id in enumerate(user_ids):
        questions = [
            {
                "question_id": question_ids[j % len(question_ids)],  # Cycle through question IDs
                "chosenAnswer": sample_history_questions[i]["questions"][j]["chosenAnswer"]
            } for j in range(len(sample_history_questions[i]["questions"]))
        ]
        histories_to_insert.append(HistoryQuestion(user_id=user_id, questions=questions))

    # Insert the histories into the database
    history_collection.insert_many([history.get() for history in histories_to_insert])

    print(f"Seeded {len(sample_history_questions)} histories into HistoryQuestion collection.")

    
def seed_db():
    """Insert samples into the database."""
    client = MongoClient(MONGO_URI)

    # Seed users and questions, storing their ObjectIds
    user_ids = seed_users(client)
    question_ids = seed_questions(client)

    # Seed scores and history questions with actual user and question ObjectIds
    seed_score(client, user_ids)
    seed_history(client, user_ids, question_ids)

    client.close()  # Close the MongoDB connection

if __name__ == "__main__":
    seed_db()