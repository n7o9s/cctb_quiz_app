import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from models import Question, User
# Load environment variables from .env file
load_dotenv()

# Get the MongoDB URI from the environment variable
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE = os.getenv("MONGO_DATABASE")

sample_questions = [
    {
        "question": "What is a car?",
        "answerA": "Vehicle.",
        "answerB": "Chemical.",
        "answerC": "Treasure.",
        "answerD": "Food.",
        "answerE": "Animal.",
        "correctAnswer": "answerA"
    },
    {
        "question": "Which company produces the Mustang?",
        "answerA": "Honda.",
        "answerB": "Chevrolet.",
        "answerC": "Toyota.",
        "answerD": "Ford.",
        "answerE": "Nissan.",
        "correctAnswer": "answerD"
    },
    {
        "question": "What does SUV stand for?",
        "answerA": "Small Utility Vehicle.",
        "answerB": "Super Urban Vehicle.",
        "answerC": "Sport Utility Vehicle.",
        "answerD": "Sports Utility Van.",
        "answerE": "Standard Utility Vehicle.",
        "correctAnswer": "answerC"
    },
    {
        "question": "What is the main function of a catalytic converter?",
        "answerA": "Enhance braking.",
        "answerB": "Increase fuel efficiency.",
        "answerC": "Improve acceleration.",
        "answerD": "Reduce emissions.",
        "answerE": "Increase horsepower.",
        "correctAnswer": "answerD"
    },
    {
        "question": "Which of these is a luxury car brand?",
        "answerA": "Toyota.",
        "answerB": "Mercedes-Benz.",
        "answerC": "Honda.",
        "answerD": "Ford.",
        "answerE": "Chevrolet.",
        "correctAnswer": "answerB"
    },
    {
        "question": "What type of engine does a Tesla use?",
        "answerA": "Hydrogen.",
        "answerB": "Diesel.",
        "answerC": "Gasoline.",
        "answerD": "Hybrid.",
        "answerE": "Electric.",
        "correctAnswer": "answerE"
    },
    {
        "question": "What is the purpose of a car's suspension system?",
        "answerA": "Increase horsepower.",
        "answerB": "Increase fuel efficiency.",
        "answerC": "Enhance acceleration.",
        "answerD": "Reduce weight.",
        "answerE": "Provide comfort and handling.",
        "correctAnswer": "answerE"
    },
    {
        "question": "What is a common feature of all-wheel drive vehicles?",
        "answerA": "Power is sent to only the rear wheels.",
        "answerB": "Power is sent to only the front wheels.",
        "answerC": "Power is sent to all four wheels.",
        "answerD": "It is always a manual transmission.",
        "answerE": "It has no traction control.",
        "correctAnswer": "answerC"
    },
    {
        "question": "What does ABS stand for in vehicles?",
        "answerA": "Automatic Braking System.",
        "answerB": "Anti-lock Braking System.",
        "answerC": "Advanced Brake System.",
        "answerD": "Auxiliary Brake System.",
        "answerE": "All Brake Systems.",
        "correctAnswer": "answerB"
    },
    {
        "question": "Which fuel type is most commonly used in cars?",
        "answerA": "Diesel.",
        "answerB": "Electric.",
        "answerC": "Ethanol.",
        "answerD": "Gasoline.",
        "answerE": "Natural Gas.",
        "correctAnswer": "answerD"
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

def seed_questions(client):
    """Insert sample questions into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    question_collection = db.Question   # Get the question collection

    # Clear the existing documents in the collection
    question_collection.delete_many({})  # Remove all documents

    # Insert sample questions in the database using the Question model
    questions_to_insert = [Question(**data) for data in sample_questions]
    question_collection.insert_many([question.get() for question in questions_to_insert])

    print(f"Seeded {len(sample_questions)} questions into Question collection.")

def seed_users(client):
    """Insert sample users into the database."""
    db = client[MONGO_DATABASE]  # Use specifiend Database
    user_collection = db.User   # Get the question collection

    # Clear the existing documents in the collection
    user_collection.delete_many({})  # Remove all documents

    # Insert sample questions in the database using the User model
    users_to_insert = [User(**data) for data in sample_users]
    user_collection.insert_many([user.get() for user in users_to_insert])

    print(f"Seeded {len(sample_users)} users into User collection.")
    
def seed_db():
    """Insert samples into the database."""
    client = MongoClient(MONGO_URI)

    # Call all seed helper functions
    seed_questions(client)
    seed_users(client)

    client.close()  # Close the MongoDB connection

if __name__ == "__main__":
    seed_db()