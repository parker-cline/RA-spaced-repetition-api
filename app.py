import os
from flask import Flask, request, abort, jsonify
from more_itertools import one
from flask_cors import CORS
from models import setup_db, User, Question, UserQuestion, db_drop_and_create_all, db_add_data

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    """ uncomment at the first time running the app """
    #db_drop_and_create_all()
    #db_add_data()

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'kris-test': 'Menon RA Group 2 custom API'})

    @app.route("/user", methods=['GET', 'POST'])
    def getuser():
        if request.method == 'GET':
            try:
                users = User.query.all()
                user = [entry.name for entry in users]
                return jsonify({"users": user}), 200
            except:
                abort(500)
        if request.method == 'POST':
            try:
                data = request.json
                name = data["name"]
                new_user = User(name=name)
                new_user.insert()
                return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "See you tomorrow!"
                        }],
                        "contexts": ["ebm", "api"]
                    }), 200
            except:
                abort(500)
                
    @app.route("/checkuser", methods=['POST'])
    def checkuser():
        if request.method == 'POST':
            try:
                data = request.json
                usr = data["name"]
                
                if bool(User.query.filter_by(name=usr).first()):
                    return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "Welcome back, we'll continue from last time."
                        }],
                        "userVariables": [{
                            "name": "exist",
                            "value": "1"
                        }],
                        "contexts": ["ebm", "api"]
                    }), 200
                
                return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "This is the first time we're meeting. Nice to meet you. I'll have to ask you some questions first."
                        }],
                        "userVariables": [{
                            "name": "exist",
                            "value": "0"
                        }],
                        "contexts": ["ebm", "api"]
                    }), 200
                
            except:
                abort(500)

    @app.route("/getquestion", methods=['GET'])
    def random_question_getter():
        if request.method == 'GET':
            try:
                # select question that user has not done yet
                # and is not in the user's history
                all_userquestions = UserQuestion.query.all()
                # decrement intervals
                for userquestion in all_userquestions:
                    if userquestion.curr_time > 0:
                        userquestion.curr_time = userquestion.curr_time - 1
                        userquestion.update()
                    elif userquestion.curr_time < 0:
                        userquestion.curr_time = 0
                        userquestion.update()

                curr_userquestion = UserQuestion.query.filter_by(
                    curr_time=0, user_id=1).first()
                if not curr_userquestion:
                    return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "No questions left for now!"
                        }],
                        "contexts": ["ebm", "api"]
                    }), 200
                else:
                    curr_question = curr_userquestion.question
                curr_user = User.query.filter_by(id=1).first()
                curr_user.curr_question_id = curr_question.id
                curr_user.update()
                return jsonify({
                    "format":
                    "ebm-api-response",
                    "version":
                    1,
                    "responses": [{
                        "type": "text",
                        "text": curr_question.question
                    }],
                    "userVariables": [{
                        "name": "question",
                        "value": "2"
                    }],
                    "contexts": ["ebm", "api"]
                })
            except:
                abort(500)

    @app.route("/answer", methods=['POST'])
    def check_answer():
        if request.method == 'POST':
            try:
                data = request.json
                user_answer = data["answer"]
                curr_question_id = User.query.filter_by(
                    id=1).one().curr_question_id
                curr_answer = Question.query.filter_by(
                    id=curr_question_id).one().answer
                curr_userquestion = UserQuestion.query.filter_by(
                    user_id=1, question_id=curr_question_id).first()
                if user_answer == curr_answer:
                    if not curr_userquestion:
                        curr_userquestion = UserQuestion(
                            user_id=1,
                            question_id=curr_question_id,
                            curr_time=2,
                            interval=2)
                        curr_userquestion.insert()
                    else:
                        curr_userquestion.interval = curr_userquestion.interval * 2
                        curr_userquestion.curr_time = curr_userquestion.interval
                        curr_userquestion.update()
                    return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "Let's see ... "
                        }],
                        "userVariables": [{
                            "name": "correct",
                            "value": "1"
                        }],
                        "contexts": ["ebm", "api"]
                    }),200
                else:
                    if not curr_userquestion:
                        curr_userquestion = UserQuestion(
                            user_id=1,
                            question_id=curr_question_id,
                            curr_time=1,
                            interval=1)
                        curr_userquestion.insert()
                    else:
                        curr_userquestion.interval = 1
                        curr_userquestion.curr_time = 1
                        curr_userquestion.update()
                    return jsonify({
                        "format":
                        "ebm-api-response",
                        "version":
                        1,
                        "responses": [{
                            "type": "text",
                            "text": "Let's see ... "
                        }],
                        "userVariables": [{
                            "name": "correct",
                            "value": "-1"
                        }],
                        "contexts": ["ebm", "api"]
                    }),200
            except:
                abort(500)

    @app.route("/ebmtest2", methods=['GET', 'POST'])
    def test2():
        if request.method == 'GET':
            return jsonify({'ebm-test2': ''})
        if request.method == 'POST':
            try:
                return jsonify({
                    "format":
                    "ebm-api-response",
                    "version":
                    1,
                    "responses": [{
                        "type": "text",
                        "text": "Moving to the next question"
                    }],
                    "userVariables": [{
                        "name": "question",
                        "value": "2"
                    }],
                    "contexts": ["ebm", "api"]
                })
            except:
                abort(500)

    @app.route("/reset", methods=['GET'])
    def reset_data():
        if request.method == 'GET':
            try:
                db_drop_and_create_all()
                db_add_data()
                return jsonify({"message": "success"}), 200
            except:
                abort(500)

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
