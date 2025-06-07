from dataclasses import asdict
from flask import Flask, jsonify, request
from flask_cors import CORS

from game_engine import Player, generate_offer_list
from game_engine.casting import generate_talent_pool
from game_engine.profile import add_completed_project, get_profile_summary
from game_engine.production import simulate_production
from game_engine.release import evaluate_release as engine_evaluate_release

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
    # Keep the actual Talent objects in session for later use
    SESSION.setdefault("talent_pools", {})[role] = pool
    return jsonify([t.to_dict() for t in pool])


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
    """Wrapper around :func:`simulate_production` from ``game_engine``."""
    return simulate_production(project, cast)


def evaluate_release(project, quality, cast):
    """Wrapper around :func:`evaluate_release` from ``game_engine``."""
    return engine_evaluate_release(project, quality, cast)


@app.route("/select_cast", methods=["POST"])
def select_cast():
    data = request.get_json(force=True)
    selections = data.get("selections", {})

    pools = SESSION.get("talent_pools", {})
    selected: list = []
    for role, tid in selections.items():
        try:
            tid = int(tid)
        except (TypeError, ValueError):
            continue
        pool = pools.get(role, [])
        talent = next((t for t in pool if t.id == tid), None)
        if talent:
            selected.append(talent)

    SESSION["selected_cast"] = selected
    return jsonify({"selected_cast": [t.to_dict() for t in selected]})


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
    cast = SESSION.get("selected_cast", [])
    if not project or not production or not player:
        return jsonify({"error": "Production not completed"}), 400

    quality = production.get("final_quality_score")
    release_results = evaluate_release(project, quality, cast)
    completed = dict(project)
    completed.update(release_results)
    add_completed_project(player, completed)
    SESSION.pop("talent_pools", None)

    SESSION.pop("selected_project", None)
    SESSION.pop("selected_cast", None)
    SESSION.pop("production_result", None)
    return jsonify(release_results)
