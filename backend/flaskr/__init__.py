import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


# Function to paginate the questions
def paginate_questions(request, selection):
    # if page number is not provided, default to 1 - ('page', 1, type=int)
    page = request.args.get('page', 1, type=int)

    # Generate the list slicing values [start:end]
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Format in JSON using format function in the class Question
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def retrieve_categories():

        # Get all the categories order by id
        categories = Category.query.order_by('id').all()

        # print(len(categories))
        # if there are no categories, abort
        if len(categories) == 0:
            abort(404)

        formatted_categories = {}
        count_categories = 0

        # # List comprehension & format function to format the data in json
        # all_categories = [formatted_categories[category.id] = category for category in categories]

        for category in categories:
            formatted_categories[category.id] = category.type
            count_categories += 1

        return jsonify(
            {
                'success': True,
                'categories': formatted_categories,
                'total_categories': count_categories
            }
        ), 200

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def retrieve_questions():
        questions = Question.query.order_by('id').all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        # formatted_categories = [category.format() for category in categories]
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            # selection = Question.query.order_by('id').all()
            # current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'delete_question_id': question_id
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category_id = body.get('category', None)
        # print("category: ", new_category_id)
        # print("type: ", type(new_category_id))

        new_difficulty = body.get('difficulty', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category_id, difficulty=new_difficulty)
            question.insert()

            category_type = Category.query.get(new_category_id).type

            all_questions = Question.query.order_by(Question.id).all()
            # current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'created': question.id,
                'current_category': category_type,
                'total_questions': len(all_questions)
            })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search/questions', methods=['POST'])
    def search_questions():
        """ An endpoint to handle POST - search request /search/questions

        Get all the questions based on the search term.
        Returns all the questions which is the search term is a substring of the question.

        """
        try:
            body = request.get_json()

            searchTerm = body.get('searchTerm', '')

            if searchTerm:
                selection = Question.query.order_by(Question.id).filter(
                            Question.question.ilike('%{}%'.format(searchTerm)))
                current_questions = paginate_questions(request, selection)

                if len(current_questions) == 0:
                    abort(404)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all()),
                    'current_category': None
                })
        except:
            print("Inside the except")
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # / categories /${id} / questions
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_question_by_category(category_id):
        try:
            selection = Question.query.filter(Question.category == str(category_id)).all()

            current_questions = paginate_questions(request, selection)

            if len(selection) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        # input from the frontend
        body = request.get_json()

        # input coming from the front end
        # #-> previous_questions: previousQuestions,
        # #-> quiz_category: this.state.quizCategory,
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        # print("quiz_category: ", quiz_category)

        try:
            # If the ALL category is selected, don't filter the questions with category
            # Else filter the questions with the selected category
            # And also don't select the previous questions, state maintained by the frontend
            if quiz_category['id'] == 0:
                # quiz = Question.query.all()
                quiz = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                quiz = Question.query.filter(Question.category == quiz_category['id'],
                                             Question.id.notin_(previous_questions)).all()

            formatted_questions = [question.format() for question in quiz]

            print('formatted questions: ', formatted_questions)
            # If there are not questions left
            if len(formatted_questions) == 0:
                return jsonify({
                    'success': True,
                    'question': None
                })

            # pick a random question using - random.choice function
            random_question = random.choice(formatted_questions)

            # if random_question:
            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })

        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # Handle bad request - the server could not understand the request due to invalid syntax.
    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({'success': False, 'error': 400, 'message': 'bad request'}),
            400
        )

    # Handle not found - The server can not find the requested resource
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({'success': False, 'error': 404, 'message': 'resource not found'}),
            404,
        )

    # The request method is known by the server but is not supported by the target resource.
    # For example, an API may not allow calling DELETE to remove a resource.
    @app.errorhandler(405)
    def method_not_found(error):
        return (
            jsonify({'success': False, 'error': 405, 'message': 'method not found'}),
            405
        )

    # The request was well-formed but was unable to be followed due to semantic errors.
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({'success': False, 'error': 422, 'message': 'unprocessable'}),
            422
        )

    # Testing dev env - verified
    @app.route('/', methods=['GET'])
    @cross_origin()  # Route specific CORS via decorator
    def index():
        return jsonify({
            'success': True,
            'message': "Hello, cross-origin-World!!!"
        })

    return app

