from flask import Flask,render_template,request,redirect,session,g,url_for
from sqlite3 import connect
import os
from pytz import timezone
from datetime import datetime
from random import choice
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.config['UPLOAD_FOLDER']='static/uploads'
app.secret_key=os.urandom(24)
dresses=os.listdir('static/dress')
kurtas=os.listdir('static/kurta')
dresses_data=[]
ADMIN_USERNAME="admin123@admin.admin"
ADMIN_PASSWORD="9877061%AK-47"
count=1
for i in dresses:
    dresses_data.append([i,f"Dress {count}",str(choice([150,250,300,560,375,180,550,900]))+' Rs.'])
    count+=1
kurtas_data=[]
count=1
for i in kurtas:
    kurtas_data.append([i,f"Kurta {count}",str(choice([150,250,300,560,375,180,550,900]))+' Rs.'])
    count+=1

@app.route("/",methods=["GET","POST"])
def index():
    if g.user:
        return redirect('/auth')
    if request.method=="POST":
        session.pop('user',None)
        conn=connect('users.db')
        data = conn.execute(f"select Id,pass from USERS where email='{request.form.get('email')}'")
        result=data.fetchall()
        conn.close()
        if request.form.get("email")==ADMIN_USERNAME and request.form.get("pass")==ADMIN_PASSWORD:
            session['user']='admin'
            return render_template("admin.html")
        
        elif result!=[]:
            if request.form.get("pass")==result[0][1]:
                session['user']=result[0][0]
                return redirect('/auth')
            else:
                return render_template("login.html")
        else:
            print("No data found")
    return render_template("index.html")

@app.route("/signup",methods=["GET","POST"])
def signUpPage():
    if request.method=="POST":
        conn=connect('users.db')
        conn.execute(f"insert into Users(fname,lname,email,pass) values('{request.form.get('fname')}','{request.form.get('lname')}','{request.form.get('email')}','{request.form.get('pass')}')")
        conn.commit()
        conn.close()
        print("Succesfully Added Data")
        return render_template("index.html")
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def loginPage():
    return render_template("login.html")

@app.route("/auth",methods=["GET","POST"])
def authenticate():
    if g.user:
        if g.user=='admin':
            return render_template("admin.html")
        return render_template("profile.html",user=session['user'])
    return redirect('/')

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']


@app.route('/designs',methods=["GET","POST"])
def selectDesigns():
    if request.method=="POST":
        dress_type=request.form['dress_type']
        if dress_type=="dress":
            return render_template("designs.html",dress_type='dress',design_data=dresses_data)
        elif dress_type=="kurta":
            return render_template("designs.html",dress_type='kurta',design_data=kurtas_data)
    return redirect('/auth')

@app.route('/order',methods=["GET","POST"])
def orderNow():
    if request.method=="POST":
        img_path='static/'+request.form['imgPath']
        india_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        curr_date=india_time[:10]
        curr_time=india_time[11:]
        conn=connect('users.db')
        conn.execute(f"insert into orders(userid,type_of_order,img_path,date,time,payment_status) values('{session['user']}','{img_path.split('/')[0]}','{img_path}','{curr_date}','{curr_time}','pending')")
        conn.commit()
        print("Order Placed Successfully")
        conn.close()
        return render_template("profile.html",user=session['user'])    
    return redirect('/auth')

@app.route('/myOrders',methods=["GET","POST"])
def getUserOrders():
    if request.method=="POST":
        conn=connect('users.db')
        user_orders=conn.execute(f"select * from orders where userid='{session['user']}'").fetchall()
        conn.close()
        return render_template("myorders.html",orders=user_orders)
    return redirect('/auth')

@app.route('/receivedOrders',methods=["GET","POST"])
def getReceivedOrders():
    if request.method=="POST":
        conn=connect('users.db')
        order_result = conn.execute("select * from orders").fetchall()
        usernames=[]
        # print(order_result)
        for order in order_result:
            rs=conn.execute(f"select fname,lname from users where id={order[1]}").fetchall()
            name=rs[0][0]+" "+rs[0][1]
            usernames.append(name)
        conn.close()
        return render_template("admin_orders.html",orders=order_result,user_names=usernames,no_of_orders=len(order_result))
    return redirect('/auth')



@app.route('/cancelOrder',methods=["GET","POST"])
def cancelOrder():
    if request.method=="POST":
        order_id=request.form['order_id']
        conn=connect('users.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM orders WHERE order_id=?', (order_id,))
        conn.commit()
        print("Order Canceled")
        conn.close()
        return redirect(request.url)
    return redirect('/auth')

@app.route('/deliveryDate',methods=['GET','POST'])
def setDeliveryDate():
    if request.method=="POST":
        order_id=request.form['order_id']
        conn=connect('users.db')
        conn.execute(f"UPDATE orders set delivery_date = ? where ORDER_ID = ?",(request.form['delivery_date'],order_id))
        conn.commit()
        print("Updated Delivery Date")
        order_result = conn.execute("select * from orders").fetchall()
        usernames=[]
        for order in order_result:
            rs=conn.execute(f"select fname,lname from users where id={order[1]}").fetchall()
            name=rs[0][0]+" "+rs[0][1]
            usernames.append(name)
        conn.close()
        return render_template("admin_orders.html",orders=order_result,user_names=usernames,no_of_orders=len(order_result))
    return redirect('/auth')

@app.route('/custom_design',methods=['GET','POST'])
def customDesignPage():
    if request.method=="POST":
        return render_template("custom_design.html")
    return redirect('/auth')

@app.route('/upload_design',methods=['GET','POST'])
def uploadDesign():
    if request.method=="POST":
        f=request.files['upload_file']
        photo_id=len(os.listdir(app.config['UPLOAD_FOLDER']))+1
        img_path=os.path.join(app.config['UPLOAD_FOLDER'],f"{g.user}_{photo_id}_"+secure_filename(f.filename))
        f.save(img_path)
        india_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
        curr_date=india_time[:10]
        curr_time=india_time[11:]
        conn=connect('users.db')
        conn.execute(f"insert into orders(userid,type_of_order,img_path,date,time,payment_status) values('{session['user']}','{request.form['type_of_order']}','{img_path}','{curr_date}','{curr_time}','pending')")
        conn.commit()
        print("Order Placed Successfully")
        conn.close()
        return """<h1>Uploaded Successfully<h1>
        <form action='/auth' method='POST'>
            <input type="submit" value="Go to Profile">
        </form>"""
    return redirect('/auth')

@app.route('/dropsession',methods=['GET','POST'])
def drop_session():
    if request.method=="POST":
        session.pop('user',None)
        return render_template("index.html")
    return redirect('/auth')


if __name__=="__main__":
    app.run(debug=True)