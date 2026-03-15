from flask import redirect,request,render_template,session,url_for
import mysql.connector
from datetime import date
from flask import flash


con = mysql.connector.connect(host="localhost", user="root", password="sahil@13^19", database="sportshope")


# def login_requerd(fun):
#     def wrapper():
#         if 'uname' in session:
#             fun()
#         else:
#             return redirect("/Login")
        
#     return wrapper

def homepage():
    print("Home")
    sql = "select * from product_w "
    cursor=con.cursor()
    cursor.execute(sql)
    pro = cursor.fetchall()

    ##Categories
    sql = "select * from Category"
    cursor.execute(sql)
    cat = cursor.fetchall()
    return render_template("homepage.html",pro=pro,cat=cat)


def viewproduct(cid):
    sql = "select * from product_w where cid=%s"
    val = (cid,)
    cursor=con.cursor()
    cursor.execute(sql,val)
    pro = cursor.fetchall()

    ##Categories
    sql = "select * from Category"
    cursor=con.cursor()
    cursor.execute(sql)
    cat = cursor.fetchall()
    return render_template("homepage.html",pro=pro,cat=cat)


def viewdetails(pid):
    if request.method=="GET":
        sql = "select * from product_w where pid=%s"
        val = (pid,)
        cursor=con.cursor()
        cursor.execute(sql,val)
        pro = cursor.fetchone()

        ##Categories
        sql = "select * from Category"
        cursor.execute(sql)
        cat = cursor.fetchall()
        return render_template("viewditails.html",pro=pro,cat=cat)
    else:
        session["pid"]= request.form.get("pid")
        session["qty"] = request.form.get("qty")
        return redirect("/addtocart")
    
def addtocart():
    if "uname" in session:
        sql = "select count(*) from mycart where pid=%s and username=%s and order_id is null"
        val = (session["pid"],session["uname"])
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0] == 1:
            return redirect("/showcart")
        else:
            sql = "insert into mycart (pid,username,qty,status) values(%s,%s,%s,%s)"
            val = (session["pid"],session["uname"],session["qty"],0)
            cursor.execute(sql,val)
            con.commit()
            return redirect("/showcart")
        
    else:
        return redirect("/login")

def login():
    if request.method == "GET":
        if "massage" in request.args:
            massage = request.args.get("massage")
        else:
            massage = ""
        return render_template("login.html", massage=massage)

    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        sql = "select count(*) from userlogin where uname=%s and pwd=%s"
        val = (uname,pwd)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        
        if count[0]==1:
            session["uname"]=uname
            return redirect("/")
        else:
            massage = "Invaild user"
        return redirect(url_for("login",massage=massage))
            

def Regester():
    if request.method == "GET":
        if "massage" in request.args:
            massage = request.args.get("massage")
        else:
            massage = ""
        return render_template("regester.html", massage=massage)
    else:
        uname = request.form.get("uname")
        pwd = request.form.get("pwd")
        phone = request.form.get("phone")
        Addrest = request.form.get("Add")
        sql = "select count(*) from userlogin where uname=%s "
        val = (uname,)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        
        if count[0]==1:
            massage = "user already exit"
            return redirect(url_for("Regester",massage=massage))
        else:
            sql = "insert into userlogin values (%s,%s,%s,%s)"
            val = (uname,pwd,phone,Addrest)
            cursor=con.cursor()
            cursor.execute(sql,val)
            con.commit()
            return redirect("/login")


def search():
    data = request.form.get("searchData")
    data=data[0:3]
    sql = "select * from product where pname like %s"
    val = ("%"+ data + "%",)
    cursor = con.cursor()
    cursor.execute(sql,val)
    pro = cursor.fetchall()
    sql = "select * from Category"
    cursor=con.cursor()
    cursor.execute(sql)
    cat = cursor.fetchall()
    return render_template("homepage.html",pro=pro,cat=cat)

def showcart():
    if "uname" in session:
        if request.method == 'GET':
            sql = "select * from cart_v where username=%s and order_id is null"
            val = (session["uname"],)
            cursor = con.cursor()
            cursor.execute(sql,val)
            iteam = cursor.fetchall()
            sql = "select * from Category"
            cursor=con.cursor()
            cursor.execute(sql)
            cat = cursor.fetchall()
            sql = "select sum(total) from cart_v where username=%s and order_id is null"
            val = (session["uname"],)
            cursor = con.cursor()
            cursor.execute(sql,val)
            total = cursor.fetchone()[0]
            session["total"]=total
            return render_template("showcart.html",iteam=iteam,cat=cat,total=total)
        else:
            action = request.form.get('action')
            card_id = request.form.get('card_id')
            qty = request.form.get('qty')
            cursor = con.cursor()
            if action == "delete":
                sql = "delete from mycart where id=%s"
                val = (card_id,)
                cursor.execute(sql,val)
                con.commit()
            else:
                sql = "update mycart set qty=%s where id=%s"
                val = (qty,card_id)
                cursor.execute(sql,val)
                con.commit()
            return redirect('/showcart')
    else:
        return redirect("/")

def Makepayment():
    if request.method=="GET":
        return render_template("makepayment.html")
    else:
        cardno = request.form.get("cardno")
        cvv = request.form.get("cvv")
        expiry = request.form.get("expiry")
        sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
        val = (cardno,cvv,expiry)
        cursor = con.cursor()
        cursor.execute(sql,val)
        count = cursor.fetchone()
        if count[0]==1:
            # byer update
            sql = "update payment set balance = balance-%s where cardno=%s and cvv=%s and expiry=%s"
            val = (session["total"],cardno,cvv,expiry)
            cursor.execute(sql,val)
            ## seller update
            sql = "update payment set balance = balance+%s where cardno=%s and cvv=%s and expiry=%s"
            val = (session["total"],'222','222','12/2040')
            cursor.execute(sql,val)
            con.commit()
            sql = "insert into order_master (date_of_order,amount) values (%s,%s)"
            val = (datetime.now(),session["total"])
            cursor.execute(sql,val)
            con.commit()
            sql = "select order_id from order_master where date_of_order=%s and amount=%s"
            val = (datetime.now().date(),session["total"])
            cursor.execute(sql,val)
            order_id = cursor.fetchone()[0]
            #print(order_id)
            sql = "update mycart set order_id=%s,status=1 where username=%s and order_id is null"
            val = (order_id,session["uname"])
            cursor.execute(sql,val)
            con.commit()
            session.pop("total")
            
            return redirect("/")

        else:
            return redirect("/makepayment")
        

def MyOrder():
    sql = "select distinct(order_id),date_of_order,amount from order_view where username=%s"
    val = (session['uname'],)
    cursor = con.cursor()
    cursor.execute(sql,val)
    order_details = cursor.fetchall()

    sql = "select pname,price,description,image_url,qty,total,order_id from order_view where username=%s"
    val = (session['uname'],)
    cursor = con.cursor()
    cursor.execute(sql,val)
    product_details = cursor.fetchall()

    final_data = {}

    for order in order_details:
        final_data[order] = []
        for product in product_details:
            if product[6] == order[0]:
                final_data[order].append(product)

    return render_template("myorder.html", final_data=final_data)

def Feedback():
    if "uname" in session:
        if request.method=="GET":
            return render_template("feedback.html")
        else:
            name = request.form.get("uname")
            email = request.form.get("email")
            phone = request.form.get("phone")
            rating = request.form.get("rating")
            feedback = request.form.get("feedback")
            sql = """INSERT INTO feedback
            (customer_name,email,phone_number,rating,message,feedback_date)
            VALUES (%s,%s,%s,%s,%s,%s)"""
            val = (name,email,phone,rating,feedback,date.today())
            cursor = con.cursor()
            cursor.execute(sql,val)
            con.commit()

            flash("Thank you for your feedback!")
            return redirect("/")
    else:
        return redirect("/login")
    
def Logout():
    if "uname" in session:
        session.clear()
        return redirect("/")
    
