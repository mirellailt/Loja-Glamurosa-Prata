from flask import Blueprint, app, render_template, request, redirect, url_for, jsonify

main_bp = Blueprint('main', __name__, template_folder='templates')
@main_bp.route('/')
def index():
    return render_template('index.html')

