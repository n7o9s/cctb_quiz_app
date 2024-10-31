# Define the database models here
from bson import ObjectId

# Question Collection
class Question:
    def __init__(self, question: str, answerA: str, answerB: str, 
                 answerC: str, answerD: str, 
                 correctAnswer: str, _id: ObjectId = None):
        self._id = _id or ObjectId()  # Automatically generate an ObjectId
        self.question = question
        self.answerA = answerA
        self.answerB = answerB
        self.answerC = answerC
        self.answerD = answerD
        self.correctAnswer = correctAnswer

    def get(self):
        """Return the Question object as a dictionary for database storage."""
        return {
            "_id": str(self._id),  # Convert ObjectId to string for JSON serialization
            "question": self.question,
            "answerA": self.answerA,
            "answerB": self.answerB,
            "answerC": self.answerC,
            "answerD": self.answerD,
            "correctAnswer": self.correctAnswer
        }

    def set(cls, data):
        """Set the attributes of the Question object from a dictionary."""
        return cls(
            question=data.get("question"),
            answerA=data.get("answerA"),
            answerB=data.get("answerB"),
            answerC=data.get("answerC"),
            answerD=data.get("answerD"),
            correctAnswer=data.get("correctAnswer")
        )
    

class User:
    def __init__(self, first_name: str, last_name: str, number: str,
                 email: str, password: str,_id: ObjectId = None):
        self._id = _id or ObjectId()  # Automatically generate a new ObjectId
        self.first_name = first_name
        self.last_name = last_name
        self.number = number
        self.email = email
        self.password = password

    def get(self):
        return {
            "_id": str(self._id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "number": self.number,
            "email": self.email,
            "password": self.password
        }