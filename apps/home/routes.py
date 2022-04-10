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
    return route_dashboard()

@blueprint.route('/dashboard')
@login_required
def route_dashboard():
    users = load_client();
    return render_template('home/dashboard.html', segment='index', client=users)

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

@blueprint.route('/popupTokenTransfer')
def popupTokenTransfer():
    walletAddr = request.args.get('walletAddr')
    return render_template("popup/popup-token-transfer.html", segment=popupTokenTransfer, addr=walletAddr)

@blueprint.route('/popupTokenTransferAll')
def popupTokenTransferAll():
    return render_template("popup/popup-token-transferall.html", segment=popupTokenTransferAll)

@blueprint.route('/popupTokenRevertAll')
def popupTokenRevertAll():
    return render_template("popup/popup-token-revertall.html", segment=popupTokenRevertAll)

@blueprint.route('/popupLockWalletAll')
def popupLockWalletAll():
    return render_template("popup/popup-lock-wallet-all.html", segment=popupLockWalletAll)

@blueprint.route('/popupTokenApproveAll')
def popupTokenApproveAll():
    return render_template("popup/popup-token-approveAll.html", segment=popupTokenApproveAll)

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

def load_client():
    
    API_BASE = 'https://app.dev.srt-wallet.io'
    
    res = requests.get(API_BASE + '/users/getuser?page=%d' % 1)

    users = [];

    for item in res.json()['users']:
        user = Client();
        user.id = item["id"]
        user.name = item["name"]
        user.phonenumer = item["phonenumer"]
        user.email = item["email"]
        user.wallet_address = item["wallet_address"]
        
        if (user.balance != None):
            user.balance = item["balance"].replace("000000000000000000", "")
        else:
            user.balance = "0"
        user.withdraw_limit = item["withdraw_limit"]
        
        users.append(user)
    
    return users;