from app import logger
from flask import jsonify, Response, request, redirect, session, url_for, current_app
from . import bp, client
import json
import os
from .handlers.tecnico_client_handler import TecnicoClientHandler
from .handlers.auth_handler import AuthHandler

#student login
@bp.route('/login')
def login():
   
    url = TecnicoClientHandler.get_authentication_url(client)
    
    return redirect(url, code=302)

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(url_for('/'))
    
    fenix_auth_code = request.args.get('code')

    if fenix_auth_code is not None:
        session['fenix_auth_code'] = fenix_auth_code
        
        user = TecnicoClientHandler.get_user(client, fenix_auth_code)
        person = TecnicoClientHandler.get_person(client, user)
    
        session['name'] = person['name']
        session['username'] = person['username']
        session['first_time_login'] = False

        if AuthHandler.check_for_user() is False:
            logger.info("New user created.")
            
        logger.info('User authenticated!')

        return redirect(url_for('user_dashboard.dashboard'))
    
    else:
        return redirect(url_for('/'))
    

@bp.route('/logout', methods=['GET'])
def logout():
    session.pop('fenix_auth_code', None)
    session.pop('name', None)
    session.pop('username', None)
    return redirect(url_for('landing_page.index'))