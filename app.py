from flask import Flask,render_template,redirect,request,flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

responses = []

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def survey_start():
    """Display Survey title and instructions"""
    return render_template("satisfaction-survey.html",survey=survey)

@app.route("/begin-survey", methods=["POST"])
def begin_survey():
    """Reset data stored and begin the survey"""
    responses.clear()

    return redirect("questions/0")

@app.route("/questions/<int:qid>")
def questions(qid):
    """Display question in survey and handle URL issues"""
    if (responses is None):
        # attempt to access questions before starting survey
        redirect("/")
    if (len(responses) == len(survey.questions)):
        # answered all questions
        return redirect("/complete")
    if (len(responses) != qid):
        # trying to access questions out of order
        flash(f"Invalid question id: {qid}")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html",id=qid,question=question)

@app.route("/answer", methods=["POST"])
def answer():
    """Handler questions answered and store results"""
    choice = request.form["answer"]

    responses.append(choice)

    if (len(responses) == len(survey.questions)):
        # All questions answered
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def complete():
    return render_template("complete.html",answers=responses)