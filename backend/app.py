from dataclasses import asdict
from flask import Flask, jsonify, request
from flask_cors import CORS
import random

from game_engine import Player, generate_offer_list
from game_engine.casting import generate_talent_pool
from game_engine.profile import add_completed_project, get_profile_summary

# Simple in-memory session store
SESSION = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key'
CORS(app)

# --- PHASE 1: Game Start & Project Selection ---

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json(force=True)
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    player = Player(name)
    SESSION["player"] = player

    return jsonify(asdict(player))


@app.route("/get_projects", methods=["GET"])
def get_projects():
    player = SESSION.get("player")
    if not player:
        return jsonify({"error": "Game not started"}), 400

    offers = generate_offer_list()
    SESSION["offers"] = offers
    return jsonify({"offers": offers})


@app.route("/get_talent_pool", methods=["GET"])
def get_talent_pool():
    """Return a generated talent pool for the requested role."""

    role = request.args.get("role")
    if not role:
        return jsonify({"error": "Role is required"}), 400

    pool = generate_talent_pool(role)
    SESSION["talent_pool"] = [t.to_dict() for t in pool]
    return jsonify(SESSION["talent_pool"])


@app.route("/get_profile", methods=["GET"])
def get_profile():
    """Return a summary of the current player's career so far."""
    player = SESSION.get("player")
    if not player:
        return jsonify({"error": "Game not started"}), 400

    summary = get_profile_summary(player)
    return jsonify(summary)


@app.route("/select_project", methods=["POST"])
def select_project():
    data = request.get_json(force=True)
    project_id = data.get("project_id")
    offers = SESSION.get("offers", [])
    selected = next((o for o in offers if o.get("id") == project_id), None)
    if not selected:
        return jsonify({"error": "Invalid project id"}), 400

    SESSION["selected_project"] = selected
    return jsonify({"selected_project": selected})


# --- PHASE 2: Casting, Production, and Release ---

def run_production(project, cast):
    """Simulate a production run and return result dictionary."""
    quality = random.randint(1, 100)
    delays = random.choice([0, 1, 2])  # simple delay indicator
    notes = f"Production completed with {len(cast)} cast members."
    return {"quality": quality, "delays": delays, "notes": notes}


def evaluate_release(project, quality):
    """Simulate release evaluation."""
    scores = {
        "critics": random.randint(1, 10),
        "audience": random.randint(1, 10),
    }
    profit = random.randint(10000, 1000000)
    awards = random.choice([
        [],
        ["Best Picture"],
        ["Audience Choice"],
    ])
    summary = random.choice([
        "Critics called it a surprise hit!",
        "Mixed reception but solid earnings.",
        "A flop at the box office.",
    ])
    return {
        "scores": scores,
        "profit": profit,
        "awards": awards,
        "summary": summary,
    }


@app.route("/select_cast", methods=["POST"])
def select_cast():
    data = request.get_json(force=True)
    cast_ids = data.get("cast_ids", [])
    # Ensure cast ids are integers in case they come in as strings
    try:
        cast_ids = [int(cid) for cid in cast_ids]
    except (TypeError, ValueError):
        cast_ids = []

    pool = SESSION.get("talent_pool", [])
    selected = [t for t in pool if t.get("id") in cast_ids]
    SESSION["selected_cast"] = selected
    return jsonify({"selected_cast": selected})


@app.route("/start_production", methods=["POST"])
def start_production():
    project = SESSION.get("selected_project")
    cast = SESSION.get("selected_cast", [])
    if not project or not cast:
        return jsonify({"error": "Project or cast missing"}), 400
    result = run_production(project, cast)
    SESSION["production_result"] = result
    return jsonify(result)


@app.route("/release_project", methods=["POST"])
def release_project():
    project = SESSION.get("selected_project")
    production = SESSION.get("production_result")
    player = SESSION.get("player")
    if not project or not production or not player:
        return jsonify({"error": "Production not completed"}), 400
    release_results = evaluate_release(project, production.get("quality"))
    add_completed_project(player, project, release_results)
    SESSION.pop("selected_project", None)
    SESSION.pop("selected_cast", None)
    SESSION.pop("production_result", None)
    return jsonify(release_results)
