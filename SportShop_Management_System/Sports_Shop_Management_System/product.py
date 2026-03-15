from flask import redirect,render_template,request
import mysql.connector
from werkzeug.utils import secure_filename

con = mysql.connector.connect(host="localhost",user="root",password="sahil@13^19",database="sportshope")
def addproduct():
    if request.method=="GET":
        sql = "select * from Category"
        cursor = con.cursor()
        cursor.execute(sql,)
        cats = cursor.fetchall()
        return render_template("addproduct.html",cats=cats)
    else:
        product_name = request.form.get("product_name")
        price = request.form.get("price")
        description = request.form.get("description")
        cid = request.form.get("cid")

        image = request.files['image_url']  #user give the file name
        filename = secure_filename(image.filename) # conect the file to secure file
        filename = "static/Images/"+image.filename  ## strong file address

        image.save(filename)  # save file 
        filename = "Images/"+secure_filename(image.filename) 

        sql = "insert into product(pname,price,description,image_url,cid) values (%s,%s,%s,%s,%s)"
        val = (product_name,price,description,filename,cid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
        return redirect("/showproduct")
    


def showall():
    sql = "select * from product_w"
    cursor = con.cursor()
    cursor.execute(sql)
    pro = cursor.fetchall()
    return render_template("showallprodeuct.html",pro=pro)

def deleteproduct(pid):
    if request.method=="GET":
        return render_template("confir.html")
    else:
        action = request.form.get("action")
        if action == "Yes":
            sql = "delete from product where pid=%s"
            val = (pid,)
            cursor=con.cursor()
            cursor.execute(sql,val)
            con.commit()
        return redirect("/showproduct")
    

def editproduct(pid):
    if request.method=="GET":
        sql = "select * from product where pid=%s"
        val = (pid,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        ets = cursor.fetchone()
        return render_template("editproduct.html",ets=ets)
    else:
        product_name = request.form.get("product_name")
        price = request.form.get("price")
        description = request.form.get("description")
        cid = request.form.get("cid")

        image = request.files['image_url']  #user give the file name
        filename = secure_filename(image.filename) # conect the file to secure file
        filename = "static/Images/"+image.filename  ## strong file address

        image.save(filename)  # save file 
        filename = "Images/"+secure_filename(image.filename) 

        sql = "update product set pname=%s,price=%s,description=%s,image_url=%s,cid=%s where pid=%s"
        val = (product_name,price,description,filename,cid,pid)
        cursor=con.cursor()
        cursor.execute(sql,val)
        con.commit()
    return redirect("/showproduct")
    
    
