from main import app
import category as cat
import product as pro
import adminlogin as ad
import user

app.add_url_rule('/addcategory',view_func=cat.addcategory,methods=["GET","POST"])
app.add_url_rule('/showcategory',view_func=cat.showcategory)
app.add_url_rule('/deletecategory/<cid>',view_func=cat.deletecategory,methods=["GET","POST"])
app.add_url_rule('/editcategory/<cid>',view_func=cat.editcategory,methods=["GET","POST"])
app.add_url_rule('/searchcategory',view_func=cat.searchcategory,methods=["GET","POST"])

app.add_url_rule('/addproduct',view_func=pro.addproduct,methods=["GET","POST"])
app.add_url_rule('/showproduct',view_func=pro.showall)
app.add_url_rule('/deleteproduct/<pid>',view_func=pro.deleteproduct,methods=["GET","POST"])
app.add_url_rule('/editproduct/<pid>',view_func=pro.editproduct,methods=["GET","POST"])
app.add_url_rule('/adminlogin',view_func=ad.adminlogin,methods=["GET","POST"])
app.add_url_rule('/dashboard',view_func=ad.dashboard)
app.add_url_rule('/logout',view_func=ad.logout)

app.add_url_rule("/",view_func=user.homepage)
app.add_url_rule("/viewproduct/<cid>",view_func=user.viewproduct)
app.add_url_rule("/viewdetails/<pid>",view_func=user.viewdetails,methods=["GET","POST"])
app.add_url_rule('/login',view_func=user.login,methods=["GET","POST"])
app.add_url_rule('/regester',view_func=user.Regester,methods=["GET","POST"])
app.add_url_rule('/search',view_func=user.search,methods=["GET","POST"])
app.add_url_rule('/Logout',view_func=user.Logout,methods=["GET","POST"])
app.add_url_rule('/addtocart',view_func=user.addtocart,methods=["GET","POST"])
app.add_url_rule('/showcart',view_func=user.showcart,methods=["GET","POST"])
app.add_url_rule('/makepayment',view_func=user.Makepayment,methods=["GET","POST"])
app.add_url_rule('/myorder',view_func=user.MyOrder)
app.add_url_rule("/feedback",view_func=user.Feedback,methods=["GET","POST"])