#All Imports


from cgitb import html
from pydoc import doc
from site import setquit
from unittest import result
from colorama import Cursor
from django.shortcuts import render
from sqlalchemy import func
from app import app
from flask import render_template,request,redirect,request
import sqlite3
import os
import json
from flask_mail import Mail,Message
from random import *
from flask import session
import cv2
from PIL import Image
from skimage.metrics import structural_similarity
import imutils

#Routes






# Route to home page
@app.route("/")
def index():
    return render_template('index.html')

#Route to Login Page

@app.route("/login")
def login():
    return render_template("login.html")

#Last Page
@app.route("/thankyou")
def thank():
    return render_template("thankyou.html")


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






#Login Routes BEGIN

@app.route("/login",methods=["POST"])
def checklogin():
    UN =request.form['username']
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



#Loggedin Routes Starts here
@app.route("/loggedin",methods=["GET","POST"])
def logged():
    if request.method == "POST":
        print("In the post method")
        Fname=request.form['fname']
        Lname=request.form['lname']
        mobile=request.form['mobile']
        date=request.form['date']
        
        print(Fname)
        print(Lname)
        print(mobile)
        print(date)
        currentlocation= os.path.dirname(os.path.abspath(__file__))
        sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
        cursor=sqlconnection.cursor()
        query1="INSERT INTO Loggedin VALUES('{fn}','{ln}','{mob}','{dt}')".format(fn=Fname,ln=Lname,mob=mobile,dt=date)
        cursor.execute(query1)
        print("Data is inserted Successfully")
        sqlconnection.commit()
        return redirect("/loggedin#step2")
    else:
        print("In the render Page")
        return render_template("loggedin.html")




#Loggedin Route Ends here





#EmailOtp Validation Starts here

with open('config.json','r') as f:
    params=json.load(f)['param']


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)

otp=randint(000000,999999)

@app.route("/verify",methods=['POST','GET'])
def verify():
    if request.method=="POST":
        accessemail=request.form["accessemail"]
        print(accessemail)
        #Sql Query
        currentlocation= os.path.dirname(os.path.abspath(__file__))
        sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
        cursor=sqlconnection.cursor()
        query1="INSERT INTO Store VALUES('{e}')".format(e=accessemail)
        cursor.execute(query1)
        print("Data is inserted Successfully")
        sqlconnection.commit()
        # Python code to create a file
        file = open('test.txt','w')
        file.write (accessemail)
        file.close()

        #Flask_Mail
        msg = Message("OTP Verification",sender="vbhvprksh@gmail.com",recipients=[accessemail])
        msg.body=("Welcome to Automated Document Verification Portal.Your Otp for Verification is" +" " + str(otp) + " " +"It is valid for next 5 mins.")
        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/otp.png") as fp:
            msg.attach("doc_verificaion.png","image/png",fp.read())
        mail.send(msg)
    return redirect("/loggedin#step2")


#Email Validation Starts Here

@app.route("/validate",methods=['POST','GET'])
def validate():
    userotp=request.form["eotp"]
    if otp== int(userotp):
        return redirect("/loggedin#step3")
    return render_template("retry.html")


#EmailOtp Validation Ends here







# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original/'
app.config['EXISTNG_FILE_bandana'] = 'app/static/original/bandana'
app.config['EXISTNG_FILE_rahul'] = 'app/static/original/rahul'
app.config['EXISTNG_FILE_vaibhav'] = 'app/static/original/vaibhav'
app.config['EXISTNG_FILE_ved'] = 'app/static/original/ved'
app.config['EXISTNG_FILE_vivek'] = 'app/static/original/vivek'
app.config['GENERATED_FILE'] = 'app/static/generated'


with open('config.json','r') as f:
    params=json.load(f)['param']


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)












#PAN card

@app.route("/pan", methods=["GET", "POST"])
def pan():
    	# Execute if request is get
	if request.method == "GET":   
            return redirect("/loggedin#step3")

            
	

	# Execute if reuqest is post
	if request.method == "POST": 
            options=request.form["plan"]
            if options=="bandana":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'

                # Python code to illustrate read() mode
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                print(pan_variable)
                if (pred>"90%"):
                        pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                        pan_msg.body=str("Dear"+ " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred  )
                        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                            pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                        mail.send(pan_msg)

                    
                if (pred<"90%"):
                    pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    pan_msg.body=str("Dear" " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(pan_msg) 

            if options=="rahul":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_rahul'], 'rahul.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_rahul'], 'rahul.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_rahul'], 'rahul.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'

                # Python code to illustrate read() mode
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                print(pan_variable)
                if (pred>"90%"):
                        pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                        pan_msg.body=str("Dear"+ " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred  )
                        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                            pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                        mail.send(pan_msg)

                    
                if (pred<"90%"):
                    pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    pan_msg.body=str("Dear" " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(pan_msg) 

            if options=="vaibhav":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_vaibhav'], 'vaibhav.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_vaibhav'], 'vaibhav.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_vaibhav'], 'vaibhav.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'

                # Python code to illustrate read() mode
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                print(pan_variable)
                if (pred>"90%"):
                        pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                        pan_msg.body=str("Dear"+ "" + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred  + ".")
                        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                            pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                        mail.send(pan_msg)

                    
                if (pred<"90%"):
                    pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    pan_msg.body=str("Dear" " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(pan_msg) 

            if options=="ved":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_ved'], 'ved.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_ved'], 'ved.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_ved'], 'ved.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'

                # Python code to illustrate read() mode
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                print(pan_variable)
                if (pred>"90%"):
                        pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                        pan_msg.body=str("Dear"+ " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred  )
                        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                            pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                        mail.send(pan_msg)

                    
                if (pred<"90%"):
                    pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    pan_msg.body=str("Dear" " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(pan_msg) 

            if options=="vivek":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_vivek'], 'vivek.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_vivek'], 'vivek.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_vivek'], 'vivek.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'

                # Python code to illustrate read() mode
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                print(pan_variable)
                if (pred>"90%"):
                        pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                        pan_msg.body=str("Dear"+ " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred  )
                        with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                            pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                        mail.send(pan_msg)

                    
                if (pred<"90%"):
                    pan_msg = Message("Pan Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    pan_msg.body=str("Dear" " " + options+",Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + pred )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        pan_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(pan_msg) 





            #place of last returning
            return redirect("/loggedin#step4")


#Aadhar Card SSIM

@app.route("/aadhar", methods=["GET", "POST"])
def aadhar():

        # Execute if request is get
        if request.method == "GET":
            return redirect("/loggedinin.html#step4")

        # Execute if reuqest is post
        if request.method == "POST":

                    # Get uploaded image
                file_upload = request.files['file_uploadd']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'aadhar.jpg'))

                    # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE'], 'aadhar.jpg')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'aadhar.jpg'))

                    # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'aadhar.jpg'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'aadhar.jpg'))

                    # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

                    # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                    # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                    
                    # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                predd=str(round(score*100,2)) + '%' + ' correct'
                file = open("test.txt", "r")
                pan_variable=(str(file.read()))
                    
                print(pan_variable)
                    
                    #TEST
                if (predd>"95%"):
                    aadhar_msg = Message("Aadhar Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    aadhar_msg.body=str("Dear User,Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + predd  )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        aadhar_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(aadhar_msg)

                    
                if (predd<"95%"):
                    aadhar_msg = Message("Aadhar Doc Verification",sender="vbhvprksh@gmail.com",recipients=[pan_variable])
                    aadhar_msg.body=str("Dear User,Congratulation Your Document has been Submitted sucessfully.As per our records your document has the accuracy of" + predd )
                    with app.open_resource("C:/Users/Vaibhav Prakash/Desktop/main/app/static/email/poster.png") as fp:
                        aadhar_msg.attach("doc_verificaion.png","image/png",fp.read())
                    mail.send(aadhar_msg) 



                    return render_template("/thankyou.html")

###Testing new thing

@app.route("/try")
def tryy():
    return render_template("try.html")



currentlocation= os.path.dirname(os.path.abspath(__file__))
sqlconnection=sqlite3.connect(currentlocation + "\Login.db")
cursor=sqlconnection.cursor()
sql="select Username from Users"
cursor.execute(sql)
results=[]
results=cursor.fetchall()
strip1 = str(results[0]).lstrip("('").rstrip("',)")
strip2 = str(results[1]).lstrip("('").rstrip("',)")
strip3 = str(results[2]).lstrip("('").rstrip("',)")
strip4 = str(results[3]).lstrip("('").rstrip("',)")
strip5 = str(results[4]).lstrip("('").rstrip("',)")
    




@app.route("/test1", methods=["GET", "POST"])
def test1():

	# Execute if request is get
	if request.method == "GET":   
            return redirect("/loggedin#step3")

            
	

	# Execute if reuqest is post
	if request.method == "POST": 
            options=request.form["plan"]
            if options=="bandana":
                file_upload = request.files['panfile']
                filename = file_upload.filename
                
                # Resize and save the uploaded image
                uploaded_image = Image.open(file_upload).resize((250,160))
                uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                
                # Resize and save the original image to ensure both uploaded and original matches in size
                original_image = Image.open(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png')).resize((250,160))
                original_image.save(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png'))
                # Read uploaded and original image as array
                original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE_bandana'], 'bandana.png'))
                uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'pan.png'))
                # Convert image into grayscale
                original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
                uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)
                # Calculate structural similarity
                (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
                diff = (diff * 255).astype("uint8")

                # Calculate threshold and contours
                thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                
                # Draw contours on image
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Save all output images (if required)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
                cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
                pred=str(round(score*100,2)) + '%' + ' correct'
                return (pred)


    #Testing Database






if __name__ == '__main__':
    app.run(port=2000)