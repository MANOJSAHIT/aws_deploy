from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

import re
import pyodbc
import urllib

from datetime import datetime
from datetime import timedelta
app = Flask(__name__)


server = 'tcp:simplydo.database.windows.net'
database = 'simplydodb'
username = 'simplydoadmin'
password = '{manoj@1234}'
driver= '{ODBC Driver 17 for SQL Server}'
# params=pymysql.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# params = urllib.parse.quote_plus(r"Driver={ODBC Driver 13 for SQL Server};Server=tcp:simplydo-db.database.windows.net,1433;Database=simplydodb;Uid=simplydoadmin;Pwd={manoj@1234};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
params = urllib.parse.quote_plus(r"DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:simplydo-db.database.windows.net;DATABASE=simplydodb;UID=simplydoadmin;PWD=manoj@1234")





app.secret_key = 'manoj1234manu'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)



class set_up:
    def __init__(self):
        @app.route('/')
        @app.route('/login', methods =['GET', 'POST'])
        def login():
            if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
                self.username = request.form['email']
                self.password = request.form['password']
                all_details=user.query.all()
                verify_deatils=user.query.filter_by(user_mail=self.username).all()
                if len(verify_deatils)==0:
                    new_user=user(self.username,self.password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for('main_page'))

                else:
                    for i in verify_deatils:
                        if i.user_password==self.password:
                            return redirect(url_for('main_page'))
                        else:
                            return redirect(url_for('login'))
            return render_template('login.html')

        @app.route('/main_page',methods=['GET','POST'])
        def main_page():
            if request.method == 'POST' and 'event-name' in request.form:
                schedule_name=request.form['event-name']
                schedule_time=request.form['date_time']
                schedule_num=len(schedules_details.query.all())+1
                new_schedule=schedules_details(schedule_name,schedule_time,self.username,schedule_num)
                print(schedule_num)
                print(new_schedule.user_mail)
                print(new_schedule.schedules_status)
                print(new_schedule.schedules_number)
                db.session.add(new_schedule)
                db.session.commit()

            elif request.method=='POST':
                but_id=request.get_data()
                get_row=schedules_details.query.get(but_id)
                if get_row.schedules_status:
                    get_row.schedules_status=False
                else:
                    get_row.schedules_status=True
                db.session.commit()
            today = datetime.today()
            t ='%'+str(today.strftime("%m/%d/%Y"))+'%'
            y = '%'+str((today - timedelta(days = 1)).strftime("%m/%d/%Y"))+'%'
            to ='%'+str((today + timedelta(days = 1)).strftime("%m/%d/%Y"))+'%'
            user_yesterday_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.like(y)).all()
            user_today_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.like(t)).all()
            user_tommorow_schedules=schedules_details.query.filter_by(user_mail=self.username).filter(schedules_details.schedules_dt.like(to)).all()

            y_event_time={}
            t_event_time={}
            to_event_time={}
            for i in user_yesterday_schedules:
                y_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            for i in user_today_schedules:
                t_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            for i in user_tommorow_schedules:
                to_event_time[i.schedules_name]=[str(i.schedules_dt)[-8::1],i.schedules_status,i.schedules_number]
            leng=[len(list(y_event_time.keys())),len(list(t_event_time.keys())),len(list(to_event_time.keys()))]
            return render_template('index.html',yet=y_event_time,tet=t_event_time,toet=to_event_time,l=leng)

class user(db.Model):

    __tablename__='user_info'
    user_mail=db.Column(db.VARCHAR(45),primary_key=True,unique=True)
    user_password=db.Column(db.VARCHAR(10))

    def __init__(self,user_mail,user_password):
        self.user_mail=user_mail
        self.user_password=user_password
class schedules_details(db.Model):

    __tablename__='schedules_info'
    schedules_number=db.Column(db.Integer,primary_key=True,nullable=False,autoincrement=True)
    schedules_name=db.Column(db.VARCHAR(45))
    schedules_status=db.Column(db.Boolean,default=False)
    schedules_dt=db.Column(db.VARCHAR(20))
    user_mail=db.Column(db.VARCHAR(45))

    def __init__(self,name,dt,mail,num):
        self.user_mail=mail
        self.schedules_dt=dt
        self.schedules_name=name
        self.schedules_status=False
        self.schedules_number=num

set_up()
app.run()
