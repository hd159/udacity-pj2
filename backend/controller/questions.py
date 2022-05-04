from asyncio.windows_events import NULL
from flask import abort, jsonify, request
from flask_cors import cross_origin
from sqlalchemy import func
from .categories import mappingCategories
from . import routes
from models import Category, db, Question
QUESTIONS_PER_PAGE = 2

def mappingQuestions(questions):
    result = []
    for question in questions:
        res = {
            "id": question.id,
            "question": question.question,
            "answer": question.answer,
            "difficulty": question.difficulty,
            "category": question.category_id
        }
        result.append(res)
    return result

# get questions per page
@routes.route("/questions")
@cross_origin()
def get_questions():
    try:
        page = request.args.get("page", 1, type=int)
        offset = (page - 1)*QUESTIONS_PER_PAGE
        currentCategory = request.args.get("currentCategory", None, type=str)
        res_questions = Question.query.order_by(Question.id.desc()).offset(offset).limit(QUESTIONS_PER_PAGE).all()
        totalQuestions = Question.query.count()
        all_categories  = Category.query.all()
        categories = mappingCategories(all_categories)
        questions = mappingQuestions(res_questions)
        return jsonify({
        'questions': questions,
        'total_questions': totalQuestions,
        'categories': categories,
        'current_category': currentCategory
        })
    except Exception as e:
        abort(500)

    
# create new question
@routes.route("/questions", methods=['POST'])
@cross_origin()
def add_question():
    try:
        body = request.get_json()
        new_question = body.get("question")
        new_answer = body.get("answer")
        new_difficulty = body.get("difficulty")
        new_category = body.get("category")
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category_id=new_category)

        question.insert()
        
        return jsonify(
            {
                "success": True,
                "status": 201
            }
        )

    except Exception as e:
        abort(422)

# get questions by category
@routes.route("/categories/<int:category_id>/questions")
@cross_origin()
def get_question_by_category(category_id):
    try:
        # page = request.args.get("page", 1, type=int)
        # offset = (page - 1)*QUESTIONS_PER_PAGE
        currentCategory = request.args.get("currentCategory", None, type=str)
        res_questions = Question.query.order_by(Question.id.desc()).filter(category_id == Question.category_id).all()
        totalQuestions = len(res_questions)
        questions = mappingQuestions(res_questions)
        return jsonify({
        "questions": questions,
        "total_questions": totalQuestions,
        "current_category": currentCategory
        })

    except Exception as e:
        abort(422)

# get questions by search term
@routes.route("/questions/search", methods=['POST'])
@cross_origin()
def get_questions_by_search_term():
    try:
        currentCategory = request.args.get("currentCategory", None, type=str)
        search_term = request.get_json()['searchTerm']
        filterByQuestion = func.lower(Question.answer).contains(func.lower(search_term))
        res_questions =  Question.query.filter(filterByQuestion).order_by(Question.id.desc()).all()
        totalQuestions = len(res_questions)
        questions = mappingQuestions(res_questions)
        return jsonify({
            "questions": questions,
            "totalQuestions": totalQuestions,
            "currentCategory": currentCategory
        })
    except Exception as e:
        abort(422)

# delete question by id
@routes.route("/questions/<int:question_id>", methods=['DELETE'])
@cross_origin()
def delete_question(question_id):
    try:
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()

        return jsonify(
            {
                "success": True,
                "msg": "deleted"
            }
        )
   
        
    except Exception as e:
        abort(422)

# get questions quizzes
@routes.route("/quizzes", methods=['POST'])
@cross_origin()
def get_questions_quizzes():
    try:
        # currentCategory = request.args.get("currentCategory", None, type=str)
        # search_term = request.get_json()['searchTerm']
        # filterByQuestion = func.lower(Question.answer).contains(func.lower(search_term))
        # res_questions =  Question.query.filter(filterByQuestion).order_by(Question.id.desc()).all()
        # totalQuestions = len(res_questions)
        # questions = mappingQuestions(res_questions)
        return jsonify({
            "question": {
                "id": 1,
                "question": "This is a question",
                "answer": "This is an answer",
                "difficulty": 5,
                "category": 4
            }
        })
    except Exception as e:
        abort(422)