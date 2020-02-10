import os
import random

from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from models import Category, Question, setup_db
from utils import get_all_categories, paginate_questions, return_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """Returns all categories
        as a dictionary.
        """
        return jsonify({
            'success': True,
            'categories': get_all_categories(),
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """Returns a list of questions along
        with all categories.
        """
        question_resp = return_questions(request)
        return jsonify({
            'success': True,
            'questions': question_resp['current_questions'],
            'total_questions': question_resp['total_questions'],
            'categories': get_all_categories(),
            'current_category': None,
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Delete the question with the id question_id
        if question does not exist returns 404.
        """
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        try:
            question.delete()
            question_resp = return_questions(request)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': question_resp['current_questions'],
                'total_questions': question_resp['total_questions']
            })
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """Creates a new question or searches
        for question containing search_term.
        """
        body = request.get_json()
        validated_body = {}
        search_term = body.get('searchTerm', None)
        if search_term is None:
            required_fields = ['question', 'answer', 'category', 'difficulty']
            for field in required_fields:
                resp = body.get(field, None)
                if resp is None:
                    abort(400)
                validated_body[field] = resp
            question_resp = return_questions(request)

            try:
                question = Question(
                    question=validated_body['question'],
                    answer=validated_body['answer'],
                    category=validated_body['category'],
                    difficulty=validated_body['difficulty'])
                question.insert()
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': question_resp['current_questions'],
                    'total_questions': question_resp['total_questions']
                }), 201
            except:
                abort(422)
        else:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            resp = paginate_questions(questions, request)
            return jsonify({
                'success': True,
                'questions': resp['current_questions'],
                'total_questions': resp['total_questions']
            })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        """Return all questions in the
        specified category.
        """
        questions = Question.query.filter_by(category=category_id).all()
        if len(questions) == 0:
            abort(404)
        resp = paginate_questions(questions, request)
        return jsonify({
            'success': True,
            'questions': resp['current_questions'],
            'total_questions': resp['total_questions'],
            'current_category': category_id,
        })

    @app.route('/quizzes', methods=['POST'])
    def generate_question():
        """Picks a question a random and
        returns it.
        """
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        category = body.get('quiz_category')
        questions = []
        if category['id'] == 0:
            questions = Question.query.filter(
                ~Question.id.in_(previous_questions))
        else:
            questions = Question.query.filter_by(
              category=category['id']
              ).filter(
                ~Question.id.in_(previous_questions))
        formated_questions = [question.format() for question in questions]
        if len(formated_questions) == 0:
            abort(404)
        random_question = random.randint(0, len(formated_questions) - 1)
        return jsonify({
            'success': True,
            'question': formated_questions[random_question]
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed."
        })

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error."
        })

    return app
