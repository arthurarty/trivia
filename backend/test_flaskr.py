import json
import os
import unittest

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Category, Question, setup_db
from sample_data import (all_categories, category_four, category_four_404,
                         incomplete_question, new_question, search_term,
                         unprocessable_question)


load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.getenv('TEST_DB_URL')

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        """Check if categories are returned"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_questions(self):
        """Check if questions are returned"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question(self):
        """Test ability to delete question"""
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 9).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 9)
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    def test_404_if_question_doesnt_exist(self):
        """Ensure 404 is returned on deleting
        question that does not exist.
        """
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_new_question(self):
        """Test ability to delete question"""
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        questions = data['questions']
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(questions), 0)

    def test_create_incomplete_question(self):
        """question missing required field should
        result in 400.
        """
        res = self.client().post('/questions', json=incomplete_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_unprocessable_question(self):
        """Unprocessable question"""
        res = self.client().post('/questions', json=unprocessable_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        """Test get questions by category"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        questions = data['questions']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(questions), 0)

    def test_get_questions_by_category_doenst_exist(self):
        """Test get category that doesn't exist"""
        res = self.client().get('/categories/10000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        """Test search questions"""
        res = self.client().post('/questions', json=search_term)
        data = json.loads(res.data)
        questions = data['questions']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(len(questions), 0)

    def test_play_quiz(self):
        """Test ability to return random question"""
        res = self.client().post('/quizzes', json=all_categories)
        data = json.loads(res.data)
        question = data['question']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotIn(question['id'], all_categories['previous_questions'])

    def test_play_quiz_category(self):
        """Test play quiz by category"""
        res = self.client().post('/quizzes', json=category_four)
        data = json.loads(res.data)
        question = data['question']
        category = category_four['quiz_category']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question['category'], category['id'])
        self.assertNotIn(question['id'], category_four['previous_questions'])

    def test_quiz_404(self):
        """Ensure quizzes endpoint returns 404
        if questions are done
        """
        res = self.client().post('/quizzes', json=category_four_404)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
