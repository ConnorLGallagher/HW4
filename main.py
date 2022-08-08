from email.charset import add_codec
import os
from flask import Flask, render_template, session, redirect, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY']='oursecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class company(db.Model):
    __tablename__="companies"

    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.Text)
    phone= db.Column(db.Text)
    email= db.Column(db.Text)
    address= db.Column(db.Text)

    def __init__(self, name, phone, email, address):
        self.name=name
        self.phone=phone
        self.email=email
        self.address=address

db.create_all()
@app.route('/', methods=['GET','POST'])
def index(): 
    companies=company
    if request.method == "POST":
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        address=request.form['address']
        newpost=company(name,phone,email,address)
        db.session.add(newpost)
        db.session.commit()
    return render_template('index.html',companies=companies)
@app.route('/deleteEntry/<pid>', methods=['GET','POST'])
def deleteEntry(pid):
    pid=pid
    if request.method == "POST":
        delm=company.query.get(pid)
        db.session.delete(delm)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("deletePost.html",pid=pid)
@app.route('/editEntry/<pid>', methods=['GET','POST'])
def editEntry(pid):
    pid=pid
    post=company.query.get(pid)
    if request.method == "POST":
        name=request.form['name']
        phone=request.form['phone']
        email=request.form['email']
        address=request.form['address']
        newpost=company(name,phone,email,address)
        delm=company.query.get(pid)
        db.session.delete(delm)
        db.session.commit()
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("editPost.html",pid=pid, post=post)
if __name__ == '__main__':
    app.run(debug=True)
