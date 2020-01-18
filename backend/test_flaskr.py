import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "triviaapi"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'Why do birds suddenly appear, every time you are near?',
            'answer': 'Just like me, they long to be, close to you',
            'category': 5,
            'difficulty': 2
        }

        self.new_question_missing_data = {
            'question': 'What is the air-speed velocity of an unlaiden swallow?',
            'answer': 'What do you mean? An African or European swallow?',
            'difficulty': 1
        }

        self.new_question_data_out_of_range = {
            'question': 'The Hammers. The Hammers is the nickname of which English Football Club?',
            'answer': 'West Ham United',
            'category': 10,
            'difficulty': 12
        }

        self.quiz_example_1 = {
            'previous_questions':[15,14],
            'quiz_category':{
                'type': 'Geography',
                'id': 3
            }
        }

        self.quiz_example_2 = {
            'previous_questions':[10,11],
            'quiz_category':{
                'type': 'Sports',
                'id': 6
            }
        }

        self.quiz_example_3 = {
            'previous_questions':[10,11],
            'quiz_category':{
                'type': 'Politics',
                'id': 'seven'
            }
        }

        self.quiz_example_4 = {
            'previous_questions': [],
            'quiz_category':'Geography'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # GET CATEGORIES
    def test_retrieve_categories(self):
        # test request path
        res = self.client().get('/categories')
        # load the data received from the response
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check the response is 200 response
        self.assertEqual(data['success'], True) # Check json success = true
        self.assertEqual(data['total_categories'], 6) # Check total categories = 6

    # Can't test for this as the data is statically held in the table. The only failure is if the data is unavailable.
    # def test_500_sent_requesting_category_list(self):
    #     res = self.client().get('/categories')
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 500)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Internal Server Error. We don\'t quite know what happened here. Please consult the documentation to ensure your request is correctly formatted.')

# GET ALL QUESTIONS
    def test_retrieve_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check the response is 200 response
        self.assertEqual(data['success'], True) # Check json success = true
        self.assertTrue(data['total_questions']) # Check total_questions var is populated
        self.assertTrue(data['current_category']) # Check current_category var is populated
        self.assertTrue(data['categories']) # Check categories var is populated

    def test_404_sent_requesting_question_list(self):
        res = self.client().get('/questions?page=77')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# POST QUESTIONS
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_400_sent_create_question_missing_data(self):
        res = self.client().post('/questions', json=self.new_question_missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')

    def test_422_sent_unable_to_insert_question(self):
        res = self.client().post('/questions', json=self.new_question_data_out_of_range)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')

    def test_404_sent_creating_new_question(self):
        res = self.client().post('/questions?page=77', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# SEARCH QUESTIONS
    def test_search_questions(self):
        res = self.client().post('/questions', json=({'searchTerm': 'oCCe'}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_no_search_results_found(self):
        res = self.client().post('/questions', json=({'searchTerm': 'kerffuffelump'}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# DELETE QUESTIONS
    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_question_not_found(self):
        res = self.client().delete('/questions/09879876')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

    def test_405_method_not_allowed(self):
        res = self.client().delete('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed - please use an appropriate method with your request, or add a resource.')

# # GET QUESTIONS BY CATEGORY
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200) # Check the response is 200 response
        self.assertEqual(data['success'], True) # Check json success = true
        self.assertTrue(data['total_questions']) # Check total_questions var is populated
        self.assertTrue(data['current_category']) # Check current_category var is populated
        self.assertTrue(data['categories']) # Check categories var is populated

    def test_404_question_not_found(self):
        res = self.client().get('/categories/88/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

# QUIZ
    def test_retrieve_next_quiz_question(self):
        res = self.client().post('/quizzes', json=self.quiz_example_1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))

    def test_404_next_quiz_question_not_found(self):
        res = self.client().post('/quizzes', json=self.quiz_example_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The requested resource could not be found.')

    def test_422_sent_unable_to_filter_quiz_questions(self):
        res = self.client().post('/quizzes', json=self.quiz_example_3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit.')


    def test_400_sent_json_sent_for_quiz_questions_not_formatted_correctly(self):
        res = self.client().post('/quizzes', json=self.quiz_example_4)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unable to process the request due to invalid data. Please reformat the request and resubmit.')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
