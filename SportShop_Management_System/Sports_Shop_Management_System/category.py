from flask import Flask,render_template,redirect,request
import mysql.connector


try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sahil@13^19",
        database="sportshope"
    )
    print("DB connected")
except Exception as e:
    print("DB error:", e)

def addcategory():
    if request.method=="GET":
        return render_template("addcategory.html")
    else:
        cname = request.form.get("cname")
        sql = """insert into category(cname) values(%s)"""
        val=(cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showcategory")
    
    
def editcategory(cid):
    if request.method=="GET":
        sql = "select * from category where cid=%s"
        val = (cid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        cat = cursor.fetchone()
        return render_template("edit.html",cat=cat)
    else:
        cname = request.form.get("cname")
        sql = """update category set cname=%s where cid=%s"""
        val = (cname,cid)
        cursor = con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showcategory")

    
 
def deletecategory(cid):
    if request.method=="GET":
        return render_template("confirmation.html")
    else:
        action = request.form.get("action")
        if action == "Yes":
            sql = "delete from category where cid=%s"
            val = (cid,)
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showcategory")

   
def showcategory():
    sql = "select * from category"
    cursor = con.cursor()
    cursor.execute(sql)
    cats = cursor.fetchall()
    return render_template("showAllCategories.html",cats=cats)

def searchcategory():
    if request.method=="GET":
        return render_template("search.html")
    else:
        cname = request.form.get("cname")
        sql = "select * from category where cname = %s"
        val = (cname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        res = cursor.fetchall()
        return render_template("result.html",res=res)
    


