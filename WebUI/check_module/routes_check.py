from flask import Blueprint, render_template, request, redirect, url_for, current_app

check_config_bp = Blueprint('check_config', __name__, template_folder='../../templates')

@check_config_bp.route('/check_config')
def check_config():
    return render_template("check_config.html")

@check_config_bp.route('/check_config/run')
def run_check_config():
    
    pass


