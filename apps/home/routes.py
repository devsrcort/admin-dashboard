# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests

class Client(object):
    def __init__(self):        
        self.id = 0
        self.name = ""
        self.phonenumer = ""
        self.email = ""
        self.wallet_address = ""
        self.balance = 0
        self.withdraw_limit = 0

@blueprint.route('/index')
@login_required
def index():
    return route_dashboard(1)

@blueprint.route('/dashboard')
@login_required
def route_dashboard(pagenum):
    users = load_client(1);
    return render_template('home/dashboard.html', segment='index', client=users)

@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/ping')
def ping():
    return render_template("home/page-ping.html", segment=ping)


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

def load_client(pagenum):
    res = requests.get('http://srt-wallet.io/users/getuser?page=%d' % pagenum)

    users = [];

    for item in res.json()['users']:
        user = Client();
        user.id = item["id"]
        user.name = item["name"]
        user.phonenumer = item["phonenumer"]
        user.email = item["email"]
        user.wallet_address = item["wallet_address"]
        user.balance = item["balance"]
        user.withdraw_limit = item["withdraw_limit"]
        
        users.append(user)
    
    return users;
    