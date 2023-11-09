from boggle import Boggle
from flask import Flask, render_template,session, request,jsonify

boggle_game = Boggle()

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"

@app.route("/")
def show_board():
    """Sets up a board to start a game"""

    board = boggle_game.make_board()
    session['board'] = board
    highscore =session.get("highscore",0)
    score = session.get("score",0)
    nOfPlay = session.get("nOfPlay", 0)
    return render_template("index.html", board = board,highscore = highscore, score=score, nOfPlay = nOfPlay)



@app.route("/check-word")
def check_word():
    """Checks if the word is valid and shows a message accordingly"""
    word = request.args["word"]
    board = session['board']
    result = boggle_game.check_valid_word(board,word)
    print(result)
    return jsonify({"result":result})



@app.route("/store-score", methods=["POST"])
def store_score():
    """Stores the current game status"""
    score = request.json["score"]
    highscore = session.get("highscore",0)
    nOfPlay = session.get("nOfPlay",0)

    session["highscore"] = max(score,highscore)   
    session["nOfPlay"] = nOfPlay + 1

    return jsonify(newRecord = highscore > score)