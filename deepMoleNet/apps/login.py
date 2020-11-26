import os
from flask import render_template, request, flash, redirect, url_for,session,escape,make_response
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from apps.forms import RegisterForm, LoginForm
from apps.data import Info, db
from apps import app

app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "register_page"
login_manager.login_message_category = 'warning'
login_manager.login_message = u'请先登录'

@login_manager.user_loader
def user_loader(user_id):
    user = Info.query.get(int(user_id))
    return user

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    registerform = RegisterForm()
    # loginform = LoginForm()
    if request.method == 'POST':
        fs = request.files["license"]
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # email2 = request.form.get('email2')
        # password2 = request.form.get('password2')
        if registerform.validate_on_submit():
            if fs.filename != "":
                file_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], email +".pdf")
                fs.save(file_path)

            email_vadidate = Info.query.filter_by(email=email).first()
            if email_vadidate:
                flash(message='Email exist.', category='err')
            else:
                try:
                    user_info = Info(username=username, email=email, password=password)
                    db.session.add(user_info)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                #flash(message='Register successfully, welcome to login!', category='ok')
                return redirect(url_for("login_page",useremail = email))

    return render_template('login/register.html', form=registerform)

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    # if current_user.is_authenticated:
    #     return redirect(url_for("user"))
    loginform = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if loginform.validate_on_submit():

            email_vadidate = Info.query.filter_by(email=email).first()

            if not email_vadidate:

                flash(message="Cannot find this email,register first!", category='err')

            else:
                if not email_vadidate.check_pwd(str(password)):
                    flash(message='Wrong password', category='err')


                else:
                        # flash(message='Welcome',category='ok')
                    if not email_vadidate.check_license():
                        flash(message='We are checking you license', category='err')

                    else:

                        login_user(email_vadidate)
                        print(session)
                        user_name = email_vadidate.get_username()
                        # return rcedirect(url_for("/"))
                        return render_template('homepage/index.html',user_name=user_name)

    return render_template('login/login.html', form=loginform)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/')
def not_login():
    return render_template('homepage/index.html')
