from flask import Flask, render_template, request,session,redirect,url_for
app = Flask(__name__)
app.secret_key=b'1234'

import mysql 
import mysql.connector

dbconfig={'host':'localhost','user':'root','password':'','database':'guestbook_db'}
conn=mysql.connector.connect(**dbconfig)
cursor=conn.cursor()

@app.route('/')
def home()->'html':
    SQL="SELECT *FROM guestbook_t"
    cursor.execute(SQL)
    data=cursor.fetchall()
    return render_template("index.html",data=data)

@app.route('/login/')
def gesipan_login()->'html':
    return render_template("login.html")

@app.route('/logout/')
def hp_logout():
        #session에서 user_id 삭제
        session.pop('user_id',None)
        
        return render_template("logout.html")

@app.route('/login_db/', methods=['POST'])
def gesipan_login_db()->'html':
    user_id=request.form["id"]
    user_pw=request.form["pw"]
    SQL="SELECT *FROM member WHERE user_id=%s AND user_pw=%s"
    cursor.execute(SQL,(user_id,user_pw))

    data= cursor.fetchall() #검색된결과를 모두가져와서 변수에저장
    if len(data)==0:
            print("id나 pw가 정확하지 않습니다.")
            return redirect("http://127.0.0.1:5000/login")
    else:
            session.clear()
            session["user_id"]=user_id
            print(session)
            return redirect("http://127.0.0.1:5000/")

@app.route('/g_write/')
def write()->'html':
    return render_template("g_write.html")

@app.route('/g_write_db/',methods=['POST'])
def writedb()->'html':
    title=request.form["title"]
    author=request.form["author"]
    desc=request.form["desc"]

    SQL="INSERT INTO guestbook_t (c_title,c_body,c_writer) VALUES (%s, %s, %s) "
    cursor.execute(SQL,(title,author,desc))
    conn.commit()
    return render_template("g_write_result.html")


app.run(debug=True)
