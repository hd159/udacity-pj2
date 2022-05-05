import datetime
import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import setup_db
from controller import *


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        # """Define test variables and initialize app."""
        self.app = Flask(__name__)
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres:postgres@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)
        self.app.register_blueprint(routes)
        # # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Anansi Boys", "answer": "Neil Gaiman", "category": 1, "difficulty": 2}

    # test get book
    def test_get_question(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

        pass
    
    
    # test create book 
    def test_create_new_book(self):
        new_question = {"question": f"Anansi Boys {datetime.datetime.now()}", "answer": "Neil Gaiman", "category": 1, "difficulty": 2}
        res = self.client().post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # test create fail if already question 
    def test_404_if_question_exist(self):
        question_exist = {"question": "Anansi Boys", "answer": "Neil Gaiman", "category": 1, "difficulty": 2}
        res = self.client().post("/questions", json=question_exist)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    # test get book by categories
    def test_get_question_by_categories(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["msg"], "deleted")

    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_get_quizze(self):
        body = {
            "quiz_category": {"id": 1},
            "previous_questions": []
        }
        res = self.client().post("/quizzes", json=body)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["question"]))

    def tearDown(self):
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()