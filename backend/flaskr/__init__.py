import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging

from  sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
logging.basicConfig(level=logging.DEBUG)


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def get_category_list():
    # get full list of categories
    categories = Category.query.order_by(Category.id).all()
    # declare list for storing categories
    catlist = {}
    # loop through categories and append the id and type to the list
    for cat in categories:
        catlist[str(cat.id)]=cat.type

    return catlist

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories. - COMPLETE
    '''

    # GET CATEGORIES
    @app.route('/')
    def index():
        return jsonify({"test":"name"})
    @app.route('/categories')
    def retrieve_categories():
        current_categories = get_category_list()

        if not current_categories:
            abort(500)
        else:
            return jsonify({
            'success': True,
            'categories': current_categories,
            'total_categories': len(current_categories)
            })


    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories. - COMPLETE

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    # GET QUESTIONS (NOT BY CATEGORY)

    @app.route('/questions')
    def retrieve_all_questions():
        selection = Question.query.order_by(Question.id).all()

        current_questions = paginate_questions(request, selection)
        catlist = get_category_list()

        if not current_questions:
            abort(404)
        else:
            return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': 'all',
            'categories': catlist
            })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score. - COMPLETE

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab. - COMPLETE
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question. - COMPLETE

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start. - COMPLETE
    '''


    # POST QUESTIONS

    @app.route('/questions', methods=['POST'])
    def create_search_question():
        new_question = request.json.get('question', None)
        new_answer = request.json.get('answer', None)
        new_category = request.json.get('category', None)
        new_difficulty = request.json.get('difficulty', None)
        search_term = request.json.get('searchTerm', None)

        if search_term is None:
            if (new_question is None) or (new_answer is None) or (new_category is None) or (new_difficulty is None):
                abort(400)
            else:
                # CREATE question functionality
                question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                try:
                    question.insert()
                except:
                    abort(422)

                # return question data
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                if not current_questions:
                    abort(404)
                else:
                    return jsonify({
                        'success': True,
                        'created': new_question,
                        'questions': current_questions,
                        'total_questions': len(Question.query.all())
                    })
        else:
            # Text search question functionality
            selection = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
            current_questions = paginate_questions(request, selection)

            if not current_questions:
                abort(404)
            else:
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection),
                })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID. - COMPLETE

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    - COMPLETE
    '''


    # DELETE QUESTIONS

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id==question_id).one_or_none()

        if question is None:
            abort(404)
        else:
            question.delete()

        # return selection for display
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if not current_questions:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category. - COMPLETE

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown. - #TODO - NOT WORKING PROPERLY IN FRONTEND (category chosen is one in front of what is displayed)
    '''


    # GET QUESTIONS (BASED ON CATEGORY - OR ALL)
    # Instructions say POST request, but this doesn't make much sense. Front end configured for GET request, so have done this instead
    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_by_category(category_id):

        # use category_id of 0 for all questions
        if category_id == 0:
            selection = Question.query.order_by(Question.id).all()
        else:
            # # Query the categories table to find the id of the category
            # selected_cat = Category.query.filter(Category.type.ilike(category)).one_or_none()
            # selection = Question.query.filter(Question.category==selected_cat.id).order_by(Question.id).all()

            selection = Question.query.filter(Question.category==category_id).order_by(Question.id).all()

        current_questions = paginate_questions(request, selection)
        catlist = get_category_list()

        if not current_questions:
            abort(404) # TODO - REQUIRE specific error message here
        else:
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': selection[0].category,
                'categories': catlist
            })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions. - COMPLETE

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. - COMPLETE
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        error = 422

        previous_questions = request.json.get('previous_questions', None)
        quiz_category = request.json.get('quiz_category', None)

        try:
            # retrieve category_id from quiz_category dictionary
            category = quiz_category.get('id')

            prevques = []
            for question in previous_questions:
                prevques.append(question)
        except:
            abort(400)

        try:
            # frontend sets value of 'ALL' categories to 'click'
            if category == 0:
                next_question = Question.query.filter(~Question.id.in_(prevques)).order_by(func.random()).first()
            else:
                next_question = Question.query.filter(Question.category==category).filter(~Question.id.in_(prevques)).order_by(func.random()).first()

            if not next_question:
                error = 404
                abort()
            else:
                return jsonify({
                    'success': True,
                    'question': next_question.format()
                })
        except:
            abort(error)


    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Unable to process the request due to invalid data. Please reformat the request and resubmit."
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "The requested resource could not be found."
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed - please use an appropriate method with your request, or add a resource."
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "The request was valid, but there was an issue during processing. Data may be out of range. Please consult the documentation and resubmit."
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error. We don't quite know what happened here. Please consult the documentation to ensure your request is correctly formatted."
        }), 500



    return app
