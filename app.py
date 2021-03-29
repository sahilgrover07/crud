from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fname= db.Column(db.String(100))
    lname= db.Column(db.String(100))
    dob=db.Column(db.Date)
    due = db.Column(db.Integer)

    def __init__(self, fname, lname, dob, due):
        self.fname= fname
        self.lname= lname
        self.dob= dob
        self.due= due
@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template("index.html", student= all_data)

@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        fname = request.form['fname']
        lname = request.form['lname']
        dob=request.form['dob']
        due= request.form['due']
  
        my_data = Data(fname,lname, dob, due)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Student Inserted Successfully")
 
        return redirect(url_for('index'))
@app.route('/update', methods =['GET','POST'])
def update():

    if request.method == 'POST':
        mydata= Data.query.get(request.form.get('id'))
        mydata.fname = request.form['fname']
        mydata.lname = request.form['lname']
        mydata.dob = request.form['dob']
        mydata.due = request.form['due']
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET','POST'])
def delete(id):
    mydata= Data.query.get(id)
    db.session.delete(mydata)
    db.session.commit()
    flash("Employee Deleted")
    return redirect(url_for('index'))

if __name__ == '__main__':
  
    app.run(debug=True)
