from app import logger
from flask import redirect, url_for, render_template, request
from . import bp
import json


@bp.route('/')
@bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@bp.route('/')
@bp.route('/index', methods=['POST'])
def choose_role():
    if request.form['submit'] == 'Fenix Authentication':
        return redirect(url_for('auth.login'))
    
    elif request.form['submit'] == 'Company Authentication':
        return redirect(url_for('auth.get_company_login_form'))
    
    return redirect(url_for('landing_page.index'))


 