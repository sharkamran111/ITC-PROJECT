from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

phones =[]

def loadphones():
            with open('phones.json', 'r') as f:
                data = json.load(f)
                return data


def savephones(phones):
        with open('phones.json', 'w') as f:
            json.dump(phones, f, indent=2, ensure_ascii=False)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/phones', methods=['GET'])
def get_phones():
    phones = loadphones()
    return jsonify(phones)

@app.route('/api/phones/update', methods=['POST'])
def update_phone():
    phones = loadphones()
    updated_data = request.json
    phone_id = updated_data.get('phoneid')
    found = False
    for i, phone in enumerate(phones):
        if str(phone.get('phoneid')) == str(phone_id) or phone.get('phoneid') == phone_id:
            phones[i] = updated_data
            found = True
            print(f"Updated phone ID {phone_id}")
            break
    savephones(phones)
    return jsonify({'success': True, 'phone': updated_data}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)
