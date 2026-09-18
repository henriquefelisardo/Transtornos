import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.conf import settings
import os
import sys

# Import InferenceEngine from the root directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import InferenceEngine

def get_engine_state(request):
    """Reconstructs the engine from the session's answers"""
    engine = InferenceEngine("knowledge_base.json")
    answers = request.session.get("answers", {})
    for q_id, weight in answers.items():
        engine.process_answer(q_id, weight)
    return engine

def load_disorder_details(disorder_id):
    try:
        with open("disorder_details.json", "r", encoding="utf-8") as f:
            details = json.load(f)
            return details.get(disorder_id)
    except FileNotFoundError:
        return None

def index(request):
    if request.method == "POST":
        show_log = request.POST.get("show_log") == "on"
        request.session["show_log"] = show_log
        request.session["answers"] = {}  # Reset game state
        return redirect("question")
    return render(request, "index.html")

def question(request):
    engine = get_engine_state(request)
    answers = request.session.get("answers", {})
    question_count = len(answers)
    max_questions = 50
    show_log = request.session.get("show_log", True)

    stop, result = engine.check_stop_conditions()
    
    # Check stop conditions
    if stop or question_count >= max_questions:
        return redirect("result")

    q = engine.get_next_question()
    if not q:
        return redirect("result")

    # Prepare leaderboard
    top_disorders = []
    if show_log:
        sorted_disorders = sorted(engine.scores.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (d_id, score) in enumerate(sorted_disorders):
            name = engine.active_disorders.get(d_id, engine.disorders[0]).get("name", d_id) if d_id in engine.active_disorders else d_id
            top_disorders.append({
                "rank": i + 1,
                "name": name,
                "score": f"{score:+.2f}"
            })

    context = {
        "question": q,
        "question_count": question_count + 1,
        "max_questions": max_questions,
        "show_log": show_log,
        "top_disorders": top_disorders,
    }
    return render(request, "question.html", context)

def answer(request):
    if request.method == "POST":
        q_id = request.POST.get("question_id")
        weight = float(request.POST.get("weight"))
        
        # Save to session
        answers = request.session.get("answers", {})
        answers[q_id] = weight
        request.session["answers"] = answers
        
    return redirect("question")

def undo(request):
    if request.method == "POST":
        answers = request.session.get("answers", {})
        if answers:
            # Remove the last inserted answer
            last_key = list(answers.keys())[-1]
            del answers[last_key]
            request.session["answers"] = answers
    return redirect("question")

def result(request):
    engine = get_engine_state(request)
    stop, result_obj = engine.check_stop_conditions()
    
    # If hit max limit without a strict stop condition
    if not result_obj and engine.active_disorders:
        best_id = max(engine.scores, key=engine.scores.get)
        result_obj = engine.active_disorders[best_id]
        
    context = {"result": None}
    
    if result_obj:
        score = engine.scores[result_obj['id']]
        details = load_disorder_details(result_obj['id'])
        context["result"] = {
            "name": result_obj["name"],
            "score": f"{score:.2f}",
            "details": details
        }
        
    return render(request, "result.html", context)
