import flask
import json
from flask import Flask, request, render_template

app = Flask(__name__)

# Global phones data
phones = []

def load_phones():
    """Load phones from JSON file into global phones list"""
    global phones
    # Changed to read from phones.json
    with open('phones.json', 'r') as f:
        phones = json.load(f)

# Initialize phones data on startup
load_phones()

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------- Phones Routes ----------------
@app.route("/api/phones")
def get_phones():
    return flask.jsonify(phones)

@app.route("/api/phones/<int:id>")
def get_phone_by_id(id):
    for phone in phones:
        # Check against 'phoneid' instead of 'bookid'
        if phone['phoneid'] == id:
            return flask.jsonify(phone)
    return flask.jsonify({"error": "Phone not found"}), 404

@app.route("/api/phones/save", methods=['POST'])
def save_phone():
    new_phone = request.get_json()
    # Convert phoneid to int for comparison
    new_phone['phoneid'] = int(new_phone['phoneid'])
    
    for i, phone in enumerate(phones):
        if phone['phoneid'] == new_phone['phoneid']:
            phones[i] = new_phone
            return flask.jsonify({"message": "Phone updated successfully"}), 200 
            
    return flask.jsonify({"error": "Phone not found"}), 404

@app.route("/api/phones/search", methods=['POST'])
def search_phones():
    criteria = request.get_json()
    # Search by 'model' instead of 'title'
    model = criteria.get('model', '').lower()
    
    filtered_phones = [
        phone for phone in phones
        if (model in phone['model'].lower() if model else True)
    ]
    
    return flask.jsonify(filtered_phones)

if __name__ == "__main__":
    # Development server
    app.run(debug=True, host="0.0.0.0", port=5500)