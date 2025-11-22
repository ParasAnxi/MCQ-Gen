from flask import Blueprint, render_template, request, send_file, session, redirect, url_for, flash
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
import spacy

from .models import tokenizer, max_length, model
from .nlp_utils import generate_mcqs
from .pdf_utils import process_pdf, draw_multiline_text
from .url_utils import process_url
from .database import db, UserResponse, QuizSession, UserFeedback
from .learning_resources import get_learning_resources

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = ""
        if "url" in request.form and request.form["url"]:
            text = process_url(request.form["url"])
        elif "manual_text" in request.form and request.form["manual_text"]:
            text = request.form["manual_text"]
        elif "files[]" in request.files:
            files = request.files.getlist("files[]")
            for file in files:
                if file.filename.endswith(".pdf"):
                    text += process_pdf(file)
                elif file.filename.endswith(".txt"):
                    text += file.read().decode("utf-8")

        num_questions = int(request.form["num_questions"])
        mcqs = generate_mcqs(text, tokenizer, max_length,
                             model, num_questions=num_questions)
        mcqs_with_index = [(i + 1, mcq) for i, mcq in enumerate(mcqs)]
        
        # Generate unique session ID for this quiz
        quiz_session_id = str(uuid.uuid4())
        session["quiz_session_id"] = quiz_session_id
        session["mcqs"] = mcqs_with_index
        
        # Create quiz session record
        quiz_session = QuizSession(
            session_id=quiz_session_id,
            total_questions=len(mcqs_with_index)
        )
        db.session.add(quiz_session)
        db.session.commit()
        
        return render_template("mcqs.html", mcqs=mcqs_with_index)

    return render_template("index.html")


@main.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    quiz_session_id = session.get("quiz_session_id")
    mcqs = session.get("mcqs", [])
    
    if not quiz_session_id or not mcqs:
        flash("No active quiz session found.", "error")
        return redirect(url_for("main.index"))
    
    # Initialize spacy for keyword extraction
    nlp = spacy.load("en_core_web_md")
    
    correct_count = 0
    user_responses = []
    
    # Process each answer
    for index, mcq in mcqs:
        question_stem, choices, correct_answer = mcq
        user_answer_key = f"answer{index}"
        
        if user_answer_key in request.form:
            selected_choice_index = int(request.form[user_answer_key])
            selected_answer = chr(65 + selected_choice_index)  # Convert to A, B, C, D
            
            # Extract keyword from the question for learning resources
            doc = nlp(question_stem)
            nouns = [token.text for token in doc if token.pos_ == "NOUN"]
            subject_keyword = nouns[0] if nouns else "general"
            
            # Check if answer is correct
            is_correct = selected_answer == correct_answer
            if is_correct:
                correct_count += 1
            
            # Save user response
            user_response = UserResponse(
                session_id=quiz_session_id,
                question_index=index,
                selected_answer=selected_answer,
                correct_answer=correct_answer,
                question_text=question_stem,
                subject_keyword=subject_keyword
            )
            user_responses.append(user_response)
            db.session.add(user_response)
    
    # Update quiz session
    quiz_session = QuizSession.query.filter_by(session_id=quiz_session_id).first()
    if quiz_session:
        quiz_session.correct_answers = correct_count
        quiz_session.score_percentage = (correct_count / len(mcqs)) * 100
        quiz_session.completed = True
    
    db.session.commit()
    
    return redirect(url_for("main.result"))


@main.route("/result")
def result():
    quiz_session_id = session.get("quiz_session_id")
    mcqs = session.get("mcqs", [])
    
    if not quiz_session_id:
        flash("No quiz session found.", "error")
        return redirect(url_for("main.index"))
    
    # Get quiz session and user responses
    quiz_session = QuizSession.query.filter_by(session_id=quiz_session_id).first()
    user_responses = UserResponse.query.filter_by(session_id=quiz_session_id).all()
    
    # Create response mapping for easy lookup
    response_map = {resp.question_index: resp for resp in user_responses}
    
    # Prepare detailed results with learning resources
    detailed_results = []
    for index, mcq in mcqs:
        question_stem, choices, correct_answer = mcq
        user_response = response_map.get(index)
        
        if user_response:
            is_correct = user_response.selected_answer == correct_answer
            learning_resources = None
            
            # Get learning resources for incorrect answers
            if not is_correct:
                learning_resources = get_learning_resources(user_response.subject_keyword)
            
            detailed_results.append({
                'question_index': index,
                'question_stem': question_stem,
                'choices': choices,
                'correct_answer': correct_answer,
                'selected_answer': user_response.selected_answer,
                'is_correct': is_correct,
                'learning_resources': learning_resources,
                'subject_keyword': user_response.subject_keyword
            })
    
    return render_template("result.html", quiz_session=quiz_session,  detailed_results=detailed_results, mcqs=mcqs)


@main.route("/download_pdf", endpoint="download_pdf") 
def download_pdf():
    mcqs = session.get("mcqs", [])
    if not mcqs:
        return "No MCQs to download.", 400

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica", 12)

    y_position = height - 40
    margin = 30
    max_width = width - 2 * margin

    for index, mcq in mcqs:
        question, choices, correct_answer = mcq
        y_position = draw_multiline_text(
            pdf, f"Q{index}: {question}?", margin, y_position, max_width)
        options = ["A", "B", "C", "D"]
        for i, choice in enumerate(choices):
            y_position = draw_multiline_text(
                pdf, f"{options[i]}: {choice}", margin + 20, y_position, max_width)
        pdf.drawString(margin + 20, y_position,
                       f"Correct Answer: {correct_answer}")
        y_position -= 20
        if y_position < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = height - 40

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="mcqs.pdf", mimetype="application/pdf")


@main.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    quiz_session_id = session.get("quiz_session_id")
    
    if not quiz_session_id:
        flash("No active quiz session found.", "error")
        return redirect(url_for("main.index"))
    
    # Process feedback for each question
    for key, value in request.form.items():
        if key.startswith("rating_"):
            question_index = int(key.split("_")[1])
            rating = int(value)
            comment_key = f"comment_{question_index}"
            comment = request.form.get(comment_key, "")
            
            feedback = UserFeedback(
                session_id=quiz_session_id,
                question_index=question_index,
                rating=rating,
                comment=comment
            )
            db.session.add(feedback)
    
    db.session.commit()
    flash("Thank you for your feedback!", "success")
    return redirect(url_for("main.result"))


@main.route("/admin/dashboard")
def admin_dashboard():
    # Get feedback statistics
    total_sessions = QuizSession.query.filter_by(completed=True).count()
    avg_score = db.session.query(db.func.avg(QuizSession.score_percentage)).filter_by(completed=True).scalar()
    
    # Get recent feedback
    recent_feedback = db.session.query(UserFeedback, UserResponse).join(
        UserResponse, 
        (UserFeedback.session_id == UserResponse.session_id) & 
        (UserFeedback.question_index == UserResponse.question_index)
    ).order_by(UserFeedback.timestamp.desc()).limit(20).all()
    
    # Get average ratings by question type/keyword
    keyword_ratings = db.session.query(
        UserResponse.subject_keyword,
        db.func.avg(UserFeedback.rating).label('avg_rating'),
        db.func.count(UserFeedback.id).label('feedback_count')
    ).join(UserFeedback, 
        (UserResponse.session_id == UserFeedback.session_id) & 
        (UserResponse.question_index == UserFeedback.question_index)
    ).group_by(UserResponse.subject_keyword).all()
    
    return render_template("admin_dashboard.html", 
                         total_sessions=total_sessions,
                         avg_score=avg_score or 0,
                         recent_feedback=recent_feedback,
                         keyword_ratings=keyword_ratings)
