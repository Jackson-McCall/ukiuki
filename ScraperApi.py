from flask import Flask, jsonify
from flask_cors import CORS
from Scraper import scrape

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape')
def scrapeEndpoint():
    try:
        data = scrape()
        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)