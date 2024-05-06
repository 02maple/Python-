from flask import Flask, session, render_template, redirect, Blueprint, request

pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')


@pb.route('/home')
def home():
    username = session.get('username')
    return render_template('index.html', username=username)
