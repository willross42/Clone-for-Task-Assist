import requests
import logging
import os
from flask import Flask, jsonify, request
from src.detect import detect_filetype

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
app = Flask(__name__)


# Default view with instructions on uses
@app.route('/')
def default():
    logging.info("app.default: missing 'evaluate/'")
    return jsonify({
        'error': 'To check catalogue file format, enter localhost:5000/evaluate/?= followed by url source.'
    }), 400


# URL evaluation view
@app.route('/evaluate/')
def catalog_type():
    # Retrieve catalogue url as 'link'
    link = request.args.get('link')
    logging.info("app.catalogue_type: url: %s", link)
    # If not provide, return message instructing user
    if not link:
        return jsonify({
            "incomplete": "Add ?link= followed by catalogue url to make the detection."
        }), 400

    # Otherwise attempt to retrieve file extension for catalogue and return format in json response
    cat_ext = "Unknown"
    try:
        cat_ext = detect_filetype(link)
        return jsonify({
            "format": cat_ext,
            "url": link
        }), 200

    # If unable to identify file extension return json error message
    except requests.RequestException:
        return jsonify({
            "url": link,
            "error": "File format unknown or unrecognizable."
        }), 400

    finally:
        logging.info("app.catalogue_type: Catalogue file extension detected - %s", cat_ext)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)