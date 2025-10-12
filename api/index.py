from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
import json
import math
import os
import requests

app = Flask(__name__)
CORS(app)  # habilita CORS para todas as rotas

# garante que o arquivo JSON seja lido mesmo no ambiente serverless
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "..", "riftbound_cards.json")

with open(JSON_PATH, "r", encoding="utf-8") as f:
    LOL_CARDS = json.load(f)

@app.route("/")
def root():
    base_url = request.host_url.rstrip("/")
    endpoints = [
        {"name": "Listar cartas", "url": f"{base_url}/cards?name=annie"},
        {"name": "Buscar carta por código/id/nome", "url": f"{base_url}/cards/origins-202298"}
    ]
    return render_template("home.html", endpoints=endpoints)

@app.route("/cards")
def get_cards():
    filters = {
        "id": request.args.get("id"),
        "code": request.args.get("code"),
        "name": request.args.get("name"),
    }
    filtered = []
    for card in LOL_CARDS:
        match = True
        for field, value in filters.items():
            if value:
                card_val = str(card.get(field, "")).lower()
                if str(value).lower() not in card_val:
                    match = False
                    break
        if match:
            filtered.append(card)
    try:
        limit = min(int(request.args.get("limit", 25)), 100)
    except ValueError:
        limit = 25
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1
    total = len(filtered)
    total_pages = math.ceil(total / limit) if limit > 0 else 1
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]
    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "totalPages": total_pages,
        "data": paginated
    })

@app.route("/cards/<value>")
def get_card(value):
    value = value.lower()
    for card in LOL_CARDS:
        if str(card.get("id", "")).lower() == value or str(card.get("code", "")).lower() == value:
            return jsonify(card)
    return jsonify({"error": "Card not found"}), 404

@app.after_request
def add_cache_headers(resp):
    resp.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate=600"
    return resp
    
# não precisa de app.run() – o Vercel já usa a variável app
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(port=5001, debug=True)
