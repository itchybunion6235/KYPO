from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Flag, Solves, User
from . import db
import json
import re
from werkzeug.security import check_password_hash
import hashlib
from datetime import datetime


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.sign_up'))
    if request.method == 'POST':
        # if request.form.get('owasp'):
        #     if 1 <= int(request.form.get('owasp')) <= 10:
        #         render_template('modal.html', user=current_user, text="Pisurka")
        flag = request.form.get('flag')
        flag = hashlib.sha256(str(flag).encode())
        confirm = Flag.query.filter_by(data=flag.hexdigest()).first()
        if confirm:
            flash('You have found the flag!', category='success')
            #user = User.query.filter_by(id=current_user.id).first()
            new_solution = Solves(solver=current_user.id, solved=confirm.id, timestamp=datetime.now())
            db.session.add(new_solution)
            db.session.commit()
        else:
            flash('No, that is not the flag!', category='error')
    else:
        pass
        
    return render_template("home.html", user=current_user)

@views.route('/robots.txt', methods=['GET'])
def robots():
    roboti = """
    <html>
    <body>
    <pre style="word-wrap: break-word; white-space: pre-wrap;">User-Agent: *
    Disallow: /secretpage/ 
    flag{Cleartext_storage_of_sensitive_information}
    Crawl-Delay: 5 
    </pre>
    </body>
    </html>
    """
    return roboti

@views.route('/secretpage', methods=['GET'])
def secretpage():
    argument = request.args.get('user_id')
    if argument == '1':
        return render_template("secretpage.html", user=current_user, text="447778af3675310f74bbd1c8f38e8e0e", redir=False)
    else:
        return render_template("secretpage.html", user=current_user, text="This is secret page only for authorized users", redir=True)
    
@views.route('/sqli', methods=['GET'])
def sqli():
    query=''
    if request.args.get('username'):
        argument = request.args.get('username')
        query = 'SELECT score from sqli where username="' + argument + '"'
    if not bool(query):
        return 'Please insert a username to check. /sqli?username=<username>'
    try:
        res = db.engine.execute(query)
        res = json.dumps([dict(r) for r in res])
        if res:
            return "User's score is: " + res
        else:
            return "User does not exist."
    except Exception as e:
        pepe = re.findall('\[.*\]',str(e))
        return str(pepe)

@views.route('/ssrf')
def follow_url():
    url = request.args.get('url', '')
    import subprocess
    proc = subprocess.Popen(["curl", url], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    if url:
        return out

    return "no url parameter provided"

@views.route('/iaaf', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin':
            if check_password_hash('sha256$2a6o0cAiFyUb1VZ9$3009b0ac2d42993b7977343cb32650dae4628a66cbc2898c90768f9c73412270', password):
                flash('Logged in successfully!', category='success')
                return render_template("secretpage.html", user=current_user, text="This is the admin's secret flag{IAAF}", redir=True)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("iaaf.html", user=current_user)
