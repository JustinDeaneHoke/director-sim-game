+51
-0

from flask import Flask, jsonify, request
from flask_cors import CORS

from game_engine import Player, generate_offer_list

# Simple in-memory session store
SESSION = {}

app = Flask(__name__)
CORS(app)


@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json(force=True)
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    player = Player(name)
    SESSION["player"] = player

    return jsonify(player.to_dict())


@app.route("/get_projects", methods=["GET"])
def get_projects():
    player = SESSION.get("player")
    if not player:
        return jsonify({"error": "Game not started"}), 400

    offers = generate_offer_list()
    SESSION["offers"] = offers
    return jsonify({"offers": offers})


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


if __name__ == "__main__":
    app.run(debug=True)
