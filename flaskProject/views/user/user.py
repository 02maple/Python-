from flask import Flask, session, render_template, redirect, Blueprint, request
from utils.query import query
from utils.errorResponse import errorResponse

ub = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

# 登录路由地址 url 以 /login 开头，接收get post请求
@ub.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        def filter_fn(user):
            return request.form['username'] in user and request.form['password'] in user

        users = query("select * from user", [], 'select')
        login_success = list(filter(filter_fn, users))
        if not len(login_success):
            return errorResponse('Account or password is incorrect')

        session['username'] = request.form['username']

        return redirect('/page/home')



@ub.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('sign-up.html')
    else:
        if request.form['password'] != request.form['checkPassword']:
            return errorResponse('Enter a different password')
        # 该函数将传入表单中的username字段取出，用于后续与数据库中做对比
        def filter_fn(user):
            return request.form['username'] in user
        # 查询数据库，表中的用户数据
        users = query("select * from user", [], 'select')
        filter_list = list(filter(filter_fn, users))
        if len(filter_list):
            return errorResponse('User already exists!')
        else:
            query('insert into user(username,password) values (%s, %s)',
                  [request.form['username'], request.form['password']])

        return redirect('/user/login')


@ub.route('/logOut')
def logOut():
    session.clear()
    return redirect('/user/login')