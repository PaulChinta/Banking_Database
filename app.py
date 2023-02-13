from flask import Flask,redirect,url_for,render_template,request,session
import mysql.connector
import test
 

cnx = mysql.connector.connect(host='localhost',user='root', password='root',database='project3')
mycurse=cnx.cursor()
app = Flask(__name__)
app.secret_key="hey"


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        ssn=request.form['ssn']
        return redirect(url_for('create',name=ssn))
    else:
        return render_template("login.html")

@app.route("/create/<name>",methods=['GET','POST'])
def create(name):
    if(request.method=='POST'):
        essn=name
        #check if ssn already exist
        cssn=request.form['ssn']
        name=request.form['name']
        st=request.form['street']
        city=request.form['City']
        #check if acc exist
        an=request.form['acc_no']
        t=request.form['acc_type']
       
        test.createaccount(essn,cssn,name,st,city,an,t)
        return redirect(url_for('summary',name=an))
    else:
        return render_template("create.html",name=name)


@app.route("/stats/<name>",methods=['GET','POST'])
def summary(name):
    acc_no=name
    
    if(request.method=='POST'):
        amount=request.form['Amount']
        t=request.form['type']
        test.transact(acc_no,t,int(amount))
        trans=test.trans(acc_no)
        stat=test.stat(acc_no)
        return render_template("stats.html",lis=trans,stat=stat)
        
    else:
        trans=test.trans(acc_no)
        stat=test.stat(acc_no)
        return render_template("stats.html",lis=trans,stat=stat)


@app.route("/emp",methods=['GET','POST'])
def po():
    return render_template("employee.html")

@app.route('/banks')
def payment():
    b_list=test.banks()
    e_list=test.employee()
    c_list=test.customers()
    return render_template('results.html',b_list=b_list,e_list=e_list,c_list=c_list)

if(__name__=="__main__"):
    app.run(debug=True)