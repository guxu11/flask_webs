import os
from flask import render_template, request, flash, redirect, url_for,session,escape,make_response
from apps.forms import RegisterForm, LoginForm, XG_k_Form, XG_uk_Form, Predict_Form
from apps.data import Info, db, FL_K, FL_UK
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
import pandas as pd
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
                        return redirect(url_for("index"))

    return render_template('login/login.html', form=loginform)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))



@app.route('/')

def index():
    return render_template("zeolite/index.html")

@app.route('/DFT/cn',methods=['GET','POST'])

def DFT():
    '''
    path = " "
    js_variable = request.form
    dict1 = dict(js_variable)
    for i in dict1:
        path = dict1[i]
    url = path
    print(url)
    '''

    return render_template("zeolite/DFT.html")



@app.route('/XGboost/cn',methods=['GET','POST'])

def XGboost():
    err1 = " "
    err2 = " "
    data1=[" "," "," "," "," "]
    data2 = [" ", " ", " ", " "]
    xg_k_form = XG_k_Form()
    xg_uk_form = XG_uk_Form()
    if xg_k_form.validate_on_submit():
        name = xg_k_form.name.data
        name_query = FL_K.query.filter_by(Zeolite = name).first()
        if not name_query:
            err1 = "未能查到"
        else:
            data1 = [name_query.getDataK()[0],name_query.getDataK()[1],name_query.getDataK()[2],name_query.getDataK()[3],name_query.getDataK()[4]]

    if xg_uk_form.validate_on_submit():
        veff = xg_uk_form.veff.data
        pld = xg_uk_form.pld.data
        rdls = xg_uk_form.rdls.data

        data_query_veff = FL_UK.query.filter_by(Veff=veff).all()
        if not data_query_veff:
            err2 ="未能查到"
        else:
            for tuple in data_query_veff:
                    if  tuple.checkDataUK(rdls,pld):
                        err2 = " "
                        data2 = [tuple.getDataUK()[0],tuple.getDataUK()[1],tuple.getDataUK()[2],tuple.getDataUK()[3]]
                        break
                    else:
                        err2 = "未能查到"


    return render_template("zeolite/XGboost.html",xg_k_form=xg_k_form,xg_uk_form=xg_uk_form,err1 = err1,err2=err2,data1=data1,data2=data2)



@app.route('/DIY/cn',methods=['GET','POST'])

def DIY():
    predict_form = Predict_Form()
    veff = " "
    pld = " "
    rdls = " "
    result = " "
    if predict_form.validate_on_submit():
        veff = predict_form.veff.data
        pld = predict_form.pld.data
        rdls = predict_form.rdls.data

        data={
                1: [veff],
                2: [pld],
                3: [rdls]
            }
        x_new=pd.DataFrame(data)

        from apps.ml_data_zeo_feature3 import model
        y_pred_train = model.predict(x_new)
        result=y_pred_train[0]

    return render_template("zeolite/DIY.html",form = predict_form,veff = veff,pld=pld,rdls=rdls,eb=result)


@app.route('/index/en')

def index_en():
    return render_template("zeolite/index_en.html")


@app.route('/DFT/en',methods=['GET','POST'])

def DFT_en():

    return render_template("zeolite/DFT_en.html")
@app.route('/DIY/en',methods=['GET','POST'])

def DIY_en():
    predict_form = Predict_Form()
    veff = " "
    pld = " "
    rdls = " "
    result = " "
    if predict_form.validate_on_submit():
        veff = predict_form.veff.data
        pld = predict_form.pld.data
        rdls = predict_form.rdls.data

        data={
                1: [veff],
                2: [pld],
                3: [rdls]
            }
        x_new=pd.DataFrame(data)
        from apps.ml_data_zeo_feature3 import model
        y_pred_train = model.predict(x_new)
        result=y_pred_train[0]

    return render_template("zeolite/DIY_en.html",form = predict_form,veff = veff,pld=pld,rdls=rdls,eb=result)

@app.route('/XGboost/en',methods=['GET','POST'])

def XGboost_en():
    err1 = " "
    err2 = " "
    data1=[" "," "," "," "," "]
    data2 = [" ", " ", " ", " "]
    xg_k_form = XG_k_Form()
    xg_uk_form = XG_uk_Form()
    if xg_k_form.validate_on_submit():
        name = xg_k_form.name.data
        name_query = FL_K.query.filter_by(Zeolite = name).first()
        if not name_query:
            err1 = "Not Found"
        else:
            data1 = [name_query.getDataK()[0],name_query.getDataK()[1],name_query.getDataK()[2],name_query.getDataK()[3],name_query.getDataK()[4]]

    if xg_uk_form.validate_on_submit():
        veff = xg_uk_form.veff.data
        pld = xg_uk_form.pld.data
        rdls = xg_uk_form.rdls.data

        data_query_veff = FL_UK.query.filter_by(Veff=veff).all()
        if not data_query_veff:
            err2 ="Not Found"
        else:
            for tuple in data_query_veff:
                    if  tuple.checkDataUK(rdls,pld):
                        err2 = " "
                        data2 = [tuple.getDataUK()[0],tuple.getDataUK()[1],tuple.getDataUK()[2],tuple.getDataUK()[3]]
                        break
                    else:
                        err2 = "Not Found"


    return render_template("zeolite/XGboost_en.html",xg_k_form=xg_k_form,xg_uk_form=xg_uk_form,err1 = err1,err2=err2,data1=data1,data2=data2)

@app.route('/')
def not_login():

    return render_template("zeolite/index.html")


