from flask import redirect,request,render_template,session
import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="sahil@13^19", database="sportshope")

def adminlogin():
    if request.method=="GET":
        return render_template("adminlogin.html")
    else:
        username = request.form.get("username")
        pwd = request.form.get("pwd")
        sql = "select count(*) from admin where username=%s and password=%s"
        val = (username,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        
        if count[0]==0:
            return redirect("/adminlogin")
        else:
            session["username"]=username
            return render_template("Dashboard.html")

def dashboard():
    if "username" in session:
        return render_template("Dashboard.html")
    else:
        return redirect("/adminlogin")
    
def logout():
    session.clear()
    return redirect("/adminlogin")