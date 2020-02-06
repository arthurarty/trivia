from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def get_all_categories():
    """
    Gets all categories form db and formats
    to returns a dictionary containing them
    """
    categories = Category.query.all()
    category_dict = {category.id: category.type for category in categories}
    return category_dict


def paginated_questions(request):
    """
    Query db to get all questions and format
    to return a list of dict itemas
    """
    all_questions = Question.query.order_by(Question.id).all()
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]
    response = {
        'current_questions': current_questions,
        'total_questions': len(all_questions)
    }
    return response
