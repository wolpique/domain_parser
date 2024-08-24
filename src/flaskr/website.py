import logging
from flask import Flask, app, jsonify, request

from .db import get_db, save_data
from .whois import get_data, get_response
from flask_caching import Cache

app = Flask(__name__)
logger = logging.getLogger(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

@app.route('/lookup_whois', methods=['GET'])
@cache.cached(timeout=300) 
def lookup():
    domain_name = request.args.get('domain_name')
    if not domain_name:
        return jsonify({'error': 'Domain name is required'}), 400
    logger.debug(f'Looking up domain: {domain_name}') 

    soup = get_response(domain_name)
    if not soup:
        return jsonify({'error': f'Failed to retrieve data for {domain_name}'}), 500

    whois_data = get_data(soup)
    if not whois_data:
        return jsonify({'error': 'No WHOIS data found'}), 404

    db = get_db()
    
    try:
        save_data(db, domain_name, whois_data)
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
        return jsonify({'error': 'Failed to save data'}), 500

    return jsonify(whois_data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

