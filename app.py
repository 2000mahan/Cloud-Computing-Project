import os
import redis
from hashlib import sha256
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect

load_dotenv(os.getenv('ENV_FILE', '.env'))

app = Flask(__name__)
rdb = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'), password=os.getenv('REDIS_SECRET'))

@app.route('/shortener', methods=['POST'])
def shortener():
    # Getting post url
    url = request.form['u']
    # Shortening url using sha hash
    hashed = sha256(url.encode()).hexdigest()
    shortened = hashed[:5]

    rdb.set(shortened, url, ex=int(os.getenv('URL_EX')))

    return jsonify({
        "shortened": shortened
    })

@app.route('/<shortened>', methods=['GET'])
def redirector(shortened):
    url = rdb.get(shortened)
    if url is None:
        return jsonify({
            "status": 404,
            "message": "Requested URL not found."
        }), 404
    
    return redirect(url.decode(), code=302)

if __name__ == '__main__':
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))
