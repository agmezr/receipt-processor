"""Main app file. 

Starts flask server and contains endpoints.
"""
from flask import Flask, request, jsonify
from src import models
from src.exceptions import ReceiptError
import logging

app = Flask(__name__)

# the in-memory structure used to store receipts points
receipts = {"test": 100}


@app.route("/receipt/process", methods=["POST"])
def process_receipt():
    data = request.json
    try:
        recepit = models.Receipt(data)
    except ReceiptError as e:
        logging.error(e)
        return jsonify(error=str(e)), 400
    recepit.calculate_points()
    receipts[recepit.uid] = recepit.total
    return jsonify(id=recepit.uid)


@app.route("/receipt/<path:uid>/points", methods=["GET"])
def get_receipt(uid):
    print(uid, receipts)
    if uid in receipts:
        return jsonify(points=receipts[uid])
    return jsonify(error="uid does not exists in list"), 404
