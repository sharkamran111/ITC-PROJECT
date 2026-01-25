import flask
import json
import os
from flask import Flask, request, render_template

# This will automatically look for templates/ folder
app = Flask(__name__)

# ---------------- CONFIGURATION ----------------
phones = []
DB_FILE = 'phones.json'

# ---------------- HELPERS ----------------
def load_phones():
    """Load phones from JSON file into global list"""
    global phones
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                phones = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {DB_FILE} is corrupted. Starting with empty list.")
            phones = []
    else:
        phones = []
        save_to_file()

def save_to_file():
    """Save the current list back to phones.json"""
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(phones, f, indent=4)
    except Exception as e:
        print(f"Error saving to file: {e}")

# Load data when app starts
load_phones()

# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template('index.html')

# 1. GET ALL
@app.route("/api/phones")
def get_phones():
    return flask.jsonify(phones)

# 2. GET ONE
@app.route("/api/phones/<int:id>")
def get_phone_by_id(id):
    for phone in phones:
        if phone['phoneid'] == id:
            return flask.jsonify(phone)
    return flask.jsonify({"error": "Phone not found"}), 404

# 3. SAVE (Create or Update)
@app.route("/api/phones/save", methods=['POST'])
def save_phone():
    try:
        new_phone = request.get_json()
        
        if not new_phone or 'phoneid' not in new_phone:
            return flask.jsonify({"error": "Invalid data"}), 400
        
        new_phone['phoneid'] = int(new_phone['phoneid'])
        new_phone['price'] = float(new_phone.get('price', 0))
        
        for i, phone in enumerate(phones):
            if phone['phoneid'] == new_phone['phoneid']:
                phones[i] = new_phone
                save_to_file()
                return flask.jsonify({"message": "Phone updated successfully"}), 200
        
        return flask.jsonify({"error": "Phone not found"}), 404
    
    except (ValueError, KeyError) as e:
        return flask.jsonify({"error": f"Invalid data: {str(e)}"}), 400

# 4. DELETE
@app.route("/api/phones/<int:id>", methods=['DELETE'])
def delete_phone(id):
    global phones
    initial_count = len(phones)
    
    phones = [p for p in phones if p['phoneid'] != id]
    
    if len(phones) < initial_count:
        save_to_file()
        return flask.jsonify({"message": "Phone deleted successfully"}), 200
    else:
        return flask.jsonify({"error": "Phone not found"}), 404

# 5. SEARCH
@app.route("/api/phones/search", methods=['POST'])
def search_phones():
    try:
        criteria = request.get_json()
        model = criteria.get('model', '').lower()
        
        filtered_phones = [
            p for p in phones
            if model in p.get('model', '').lower()
        ]
        
        return flask.jsonify(filtered_phones)
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)