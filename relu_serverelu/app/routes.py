
from flask import Blueprint, request, jsonify, render_template
from .device.display import setup_device, scroll_message

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/display', methods=['POST'])
def display_message():
    msg = request.form['message']
    scroll_message(msg)
    return jsonify({"message": "Message displayed: " + msg})
