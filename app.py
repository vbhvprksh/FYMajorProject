from django.shortcuts import render
from app import app
from flask import render_template,request,redirect
import sqlite3
import os


#Routes

#Home

# Route to home page
@app.route("/")
def index():
    return render_template('index.html')





#Login Routes BEGIN

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login",methods=["POST"])
def checklogin():
    UN=request.form['username']
    PD=request.form['password']
    currentlocation= os.path.dirname(os.path.abspath(__file__))
    sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
    cursor=sqlconnection.cursor()
    query1="SELECT Username,Password from Users WHERE Username= '{un}' AND Password= '{pw}' ".format(un=UN,pw=PD)
    rows = cursor.execute(query1)
    rows=rows.fetchall()
    if len(rows) ==1:
        return render_template("loggedin.html")
    else:
        return redirect("/register")


#Login Routes End

#Register Routes Begin


@app.route("/register",methods=["GET","POST"])

def registerpage():
    if request.method == "POST":
        print("In the post method")
        DUN=request.form['DUsername']
        DPD=request.form['pwd']
        Uemail=request.form['EmailUser']
        print(DUN)
        print(DPD)
        print(Uemail)
        currentlocation= os.path.dirname(os.path.abspath(__file__))
        sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
        cursor=sqlconnection.cursor()
        query1="INSERT INTO Users VALUES('{u}','{p}','{e}')".format(u=DUN,p=DPD,e=Uemail)
        cursor.execute(query1)
        print("Data is inserted Successfully")
        sqlconnection.commit()
        return redirect("/")
    else:
        print("In the render Page")
        return render_template("Register.html")

#Register Routes End here




#Loggedin Routes Starts here
@app.route("/loggedin",methods=["GET","POST"])

def logged():
    if request.method == "POST":
        print("In the post method")
        Fname=request.form['fname']
        Lname=request.form['lname']
        Lemail=request.form['lemail']
        mobile=request.form['mobile']
        date=request.form['date']
        
        print(Fname)
        print(Lname)
        print(Lemail)
        print(mobile)
        print(date)
        currentlocation= os.path.dirname(os.path.abspath(__file__))
        sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
        cursor=sqlconnection.cursor()
        query1="INSERT INTO Loggedin VALUES('{fn}','{ln}','{le}','{mob}','{dt}')".format(fn=Fname,ln=Lname,le=Lemail,mob=mobile,dt=date)
        cursor.execute(query1)
        print("Data is inserted Successfully")
        sqlconnection.commit()
        return redirect("/doc")
    else:
        print("In the render Page")
        return render_template("loggedin.html")




#Loggedin Route Ends here


#Doc Uploading


@app.route("/doc")
def doc():
    return render_template("doc.html")




#Thank you Route Starts here

@app.route("/thank")
def thankyou():
    return render_template("thankyou.html")

@app.route("/blogs")
def blogs():
    return render_template("blogs.html")





#EmailOtp Validation Starts here


#EmailOtp Validation Ends here


#Pan Verification




if __name__ == '__main__':
    app.run()