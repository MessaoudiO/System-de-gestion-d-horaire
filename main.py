from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
import datetime
from collections import defaultdict
from random import randint #retourne un nombre par hasard in range[a,b]
from tabulate import tabulate



local_server= True
app = Flask(__name__,template_folder='templates')
app.secret_key='oussama'



login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))



# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/omnivox'
db=SQLAlchemy(app)

days = 5
periods = 6
recess_break_aft = 3 
section = None

def dt(time):
    return datetime.datetime.combine(datetime.date.today(), time)

def timetable():
    periods = ["8:00 - 9:30","9:30 - 11:00","11:00 - 12:30","1:30 - 3:00","3:00 - 4:30"]
    courses= ["IA","DT","POC","IA"]
    day = ['Lundi', 'Mardi', 'Wednesday', 'Thrusday', 'Friday']
    board=[]



    for x in range(7):
        board.append(["_"] * 10)
    for i in range(7):
        board[i][3] = "Ps"
        board[i][6] = "Ps"

    k = 0
    for j in range(1, 6):
        board[j][0] = days[k]
        k += 1


table_data= [['Jour/Heure' ,'8:00 - 9:30','9:30 - 11:00','Break','1:30 - 3:00','3:00 - 4:30'],
             ['Lundi','IA','POC',' ','ENG','MATH'],
             ['Mardi','IA','POC',' ','ENG','MATH'],
             ['Mercredi','FCC','DT',' ','ESP','BDD'],
             ['Mardi','IA','POC',' ','FR','PE'],
             ['Mardi','FCC','DT',' ','PH','CH']]

with open('mytable.html', 'w') as f:
    f.write(tabulate(table_data, headers="firstrow", tablefmt='html'))




class Admin(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(1000))

class Prof(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(60))
    username=db.Column(db.String(60))
    password=db.Column(db.String(60))




class Cours:
    def __init__(self, id, lvnr, name, lecturers):
        self.id = int(id)
        self.lvnr = int(lvnr)
        self.name = name
        self.name_short = ""
        self.category = ""
        
        self.lecturers = [_.strip() for _ in lecturers.split(",")]
        
        self.appointments = []
        self.occurrences = []





    
class Course(db.Model):
    course_id=db.Column(db.Integer,primary_key=True)
    course_code=db.Column(db.String(60))
    course_name=db.Column(db.String(60))



class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    Nom=db.Column(db.String(60))
    faculty_name=db.Column(db.String(60))
    course_name=db.Column(db.String(60))
    password=db.Column(db.String(250))
    username=db.Column(db.String(250))
    session=db.Column(db.String(60))

    
    

class addtable(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    faculty=db.Column(db.String(250))
    course=db.Column(db.String(250))
    room=db.Column(db.String(250))
    start_time=db.Column(db.String(250))
    end_time=db.Column(db.String(250))
    prof=db.Column(db.String(250))
    jour=db.Column(db.String(250))

class Room(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    room=db.Column(db.String(250))



@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/homePR')
def homePR():
    

    return render_template('homePR.html')


@app.route('/home')
@login_required
def home():

    return render_template('home.html',)

@app.route('/homeST')
def homeST():
    query=Student.query.all()

    return render_template('homeST.html',query=query)

@app.route("/search")
def search():
    query=Course.query.all()


    return render_template("search.html",query=query)

@app.route("/searchaction",methods=['POST','GET'])
def searchA():
     
    
    query=addtable.query.all()    
     
     
    
    return render_template("searchaction.html",query=query)

@app.route("/schedule")
def schedule():

    query=addtable.query.all()
    
    


    return render_template("schedule.html",query=query)

@app.route("/scheduleST")
def scheduleST(id):
    query=addtable.query.filter_by(id=id).first()
    query2=db.session.query.all()


    return render_template("scheduleST.html",query2=query2)

@app.route("/schedulePR")
def schedulePR():
    
    query2=db.session.query.all()


    return render_template("schedulePR.html",query2=query2)

@app.route('/list')
@login_required
def showlist():
    query=addtable.query.all()
    return render_template('list.html',query=query)

#Add et Delete
@app.route("/delete/<string:id>",methods=['POST','GET'])
@login_required
def delete(id):
    post=addtable.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    
    flash("Slot Deleted Successful","danger")
    return redirect('/list')


#Section de Login

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        username=request.form.get('username')
        password=request.form.get('password')
        user=Admin.query.filter_by(username=username).first()
        

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Vous etes connecte","primary")
            return render_template('home.html')
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')


@app.route('/student',methods=['POST','GET'])
def loginST():
    
    return render_template('homeST.html')

@app.route('/loginPR',methods=['POST','GET'])
def loginPR():
    if request.method == "POST":
        username=request.form.get('name')
        password=request.form.get('password')
        user=Prof.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Vous etes connecte","primary")
            return render_template('homePR.html')
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('LoginPR.html')   


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

app.run(debug=True)