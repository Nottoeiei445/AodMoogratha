# app.py

from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Stock import Stock

app = Flask(__name__)

# Initialize the stock
stock = Stock()

# Example initial data
initial_data = [
    {'ID': 5, 'Name': "Item A", 'QTY': 5, 'IMG': "Image1.png"},
    {'ID': 4, 'Name': "Item B", 'QTY': 4, 'IMG': "Image2.png"},
    {'ID': 2, 'Name': "Item C", 'QTY': 3, 'IMG': "Image3.png"},
    {'ID': 3, 'Name': "Item D", 'QTY': 6, 'IMG': "Image4.png"},
]

for item in initial_data:
    stock.insert(item['ID'], item['Name'], item['QTY'], item['IMG'])

@app.route('/stock', methods=['GET'])
def get_stock():
    """
    Retrieve all stock items in in-order traversal.
    """
    return jsonify(stock.inOrder()), 200

@app.route('/stock/<int:ID>', methods=['GET'])
def get_item(ID):
    """
    Retrieve a specific stock item by ID.
    """
    item = stock.search(ID)
    if item:
        return jsonify({'ID': item.ID, 'Name': item.Name, 'QTY': item.QTY, 'IMG': item.IMG}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/stock', methods=['POST'])
def add_item():
    """
    Add a new stock item.
    Expects JSON with 'ID', 'Name', 'QTY', and 'IMG'.
    """
    data = request.get_json()
    if not data or 'ID' not in data or 'Name' not in data or 'QTY' not in data or 'IMG' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    inserted = stock.insert(data['ID'], data['Name'], data['QTY'], data['IMG'])
    if inserted:
        return jsonify({'message': 'Item added successfully'}), 201
    else:
        return jsonify({'error': 'Item with given ID already exists'}), 400

@app.route('/stock/<int:ID>', methods=['PUT'])
def update_item(ID):
    """
    Update an existing stock item's QTY and/or IMG.
    Expects JSON with 'QTY' and/or 'IMG'.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid data'}), 400
    updated = False
    if 'QTY' in data:
        updated = stock.updateQTY(ID, data['QTY']) or updated
    if 'IMG' in data:
        updated = stock.updateIMG(ID, data['IMG']) or updated
    if updated:
        return jsonify({'message': 'Item updated successfully'}), 200
    else:
        return jsonify({'error': 'Item not found or no valid fields to update'}), 404

@app.route('/stock/<int:ID>', methods=['DELETE'])
def delete_item(ID):
    """
    Delete a stock item by ID.
    """
    deleted = stock.delete(ID)
    if deleted:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
