
import mysql.connector
from sshtunnel import SSHTunnelForwarder


cnx = mysql.connector.connect(host='localhost',user='root', password='root',database='project3')
mycurse=cnx.cursor()



def transact(accno,typ,amount):
    s=str(accno)+','+typ+','+str(amount)
    mycurse.execute("select acc_type from accounts where acc_no="+str(accno))
    for i in mycurse:
        at=i[0]

    if(typ=="'withdraw'"):
        mycurse.execute("select balance from accounts where acc_no="+str(accno))
        for i in mycurse:
            balance=i[0]
        newamount=int(balance)-amount
        if(newamount<0):
            print("not enough balance: money overdraft")
            mycurse.execute('update accounts set balance='+str(newamount)+' ,last_access_date=now(),overdraft='+str(amount)+' where acc_no='+str(accno))
            cnx.commit()
            mycurse.execute('insert into transactions values('+s+',now());')
            cnx.commit()

        else:
            mycurse.execute('update accounts set balance='+str(newamount)+' ,last_access_date=now() where acc_no='+str(accno))
            cnx.commit()
            mycurse.execute('insert into transactions values('+s+',now());')
            cnx.commit()

    elif(typ=="'deposit'"):
        
        mycurse.execute("select overdraft from accounts where acc_no="+str(accno))
        if(mycurse.fetchall()[0][0]!=None):
            mycurse.execute("select overdraft from accounts where acc_no="+str(accno))
            for i in mycurse:
                ov=i[0]
        else:
            ov=0
        mycurse.execute("select balance from accounts where acc_no="+str(accno))
        for i in mycurse:
            balance=i[0]
        newamount=int(balance)+amount-ov
        mycurse.execute('update accounts set balance='+str(newamount)+' ,last_access_date=now(),overdraft=0 where acc_no='+str(accno))
        cnx.commit()
        mycurse.execute('insert into transactions values('+s+',now());')
        cnx.commit()

def loan_payment(loanid,payid,amount):
    s=str(loanid)+','+str(payid)+','+str(amount)
    mycurse.execute("select owe from loans where loan_id="+str(loanid)+";")
    for i in mycurse:
          balance=i[0]
    if (int(balance>=0)):
        newamount=int(balance)-amount
        mycurse.execute('update loans set owe='+str(newamount)+' where loan_id='+str(loanid))
        cnx.commit()
        mycurse.execute('insert into payments values('+s+',now());')
        cnx.commit()
    else:
        print('loan has been paid')

# permit with personel banker
def createaccount(essn,cssn,name,street,city,accno,typ):
    mycurse.execute("select * from  customers where cus_ssn="+str(cssn))
    if (len(mycurse.fetchall())==0):
        mycurse.execute("insert into customers values("+str(cssn)+",'"+str(name)+"','"+str(street)+"','"+str(city)+"',"+str(essn)+");")
        cnx.commit()
    s2=str(cssn)+','+str(accno)
    if(typ=="'checking'"):
        s=str(accno)+',0,now(),'+str(typ)+',0,NULL,NULL,NULL,NULL'
        mycurse.execute('insert into accounts values('+s+');')
        cnx.commit()
        mycurse.execute('insert into maintains values('+s2+');')
        cnx.commit()

    elif(typ=="'savings'"):
        s=str(accno)+',0,now(),'+str(typ)+',NULL,3,NULL,NULL,NULL'
        mycurse.execute('insert into accounts values('+s+');')
        cnx.commit()
        mycurse.execute('insert into maintains values('+s2+');')
        cnx.commit()

    elif(typ=="'cd'"):
        s=str(accno)+',0,now(),'+str(typ)+',NULL,NULL,NULL,NULL,NULL'
        mycurse.execute('insert into accounts values('+s+');')
        cnx.commit()
        mycurse.execute('insert into maintains values('+s2+');')
        cnx.commit()
        
    elif(typ=="'credit'"):
        limit=str(5000)
        s=str(accno)+',0,now(),'+str(typ)+',NULL,NULL,'+limit+',15,0'
        mycurse.execute('insert into accounts values('+s+');')
        cnx.commit()
        mycurse.execute('insert into maintains values('+s2+');')
        cnx.commit()
           
def createloan(cssn,loanid,amount):
    s=str(loanid)+','+str(amount)+','+str(amount)
    s2=str(cssn)+','+str(loanid)
    mycurse.execute('insert into loans values('+s+');')
    cnx.commit()
    mycurse.execute('insert into takes values('+s2+');')
    cnx.commit()

def checkbalance(cssn,acc_no):
    mycurse.execute("select balance from accounts where acc_no="+str(acc_no))
    # c=input('enter ssn')
    for i in mycurse:
        print(i[0])

def trans(acc_no):
    mycurse.execute("select * from transactions where acc_no="+str(acc_no))
    trans=mycurse.fetchall() 
    return trans

def stat(acc_no):
    mycurse.execute("select * from accounts where acc_no="+str(acc_no))
    stat=mycurse.fetchall()[0] 
    return stat

def loandata(lid):
    mycurse.execute("select * from loans where loan_id="+str(lid))
    
    for i in mycurse:
        print(i)
# results
def banks():
    mycurse.execute("select * from banks")
    b_list=mycurse.fetchall()
   
    return b_list
def employee():
    mycurse.execute("select * from employee")
    b_list=mycurse.fetchall()
  
    return b_list
def customers():
    mycurse.execute("select * from customers")
    c_list=mycurse.fetchall()

    return c_list

def addbranch(bname,city,manager_ssn):
    mycurse.execute("insert into banks values('"+str(bname)+"','"+str(city)+"',"+str(manager_ssn)+");")
    cnx.commit()
    print("added branch succesfully")

def checkloans(cssn):
    mycurse.execute("select * from loans where loan_id in (select loan_id from takes where cus_ssn="+str(cssn)+");")
    for i in mycurse:
        print(i)
def createemp(essn,name,telephone,dependant,startdate,bank_name):
    mycurse.execute("insert into employee values("+str(essn)+",'"+str(name)+"',"+str(telephone)+",'"+str(dependant)+"','"+str(startdate)+"',0,'"+str(bank_name)+"');")
    cnx.commit()
    mycurse.execute("update employee set duration=2023-YEAR(start_date) WHERE EMP_SSN="+str(essn))
    cnx.commit()

def branchloans(branch):
    mycurse.execute("select SUM(OWE) from loans where loan_id in(select loan_id from takes where cus_ssn IN(SELECT CUS_SSN FROM CUSTOMERS WHERE EMP_SSN  IN(select EMP_SSN from employee WHERE EMP_SSN IN (SELECT EMP_SSN FROM EMPLOYEE WHERE BANK_NAME='"+str(branch)+"'))))")
    for i in mycurse:
        owe=i[0]
        print("Total Loan amount still owed $"+str(i[0]))
    mycurse.execute("select SUM(loan_amount) from loans where loan_id in(select loan_id from takes where cus_ssn IN(SELECT CUS_SSN FROM CUSTOMERS WHERE EMP_SSN  IN(select EMP_SSN from employee WHERE EMP_SSN IN (SELECT EMP_SSN FROM EMPLOYEE WHERE BANK_NAME='"+str(branch)+"'))))")
    for i in mycurse:
        print("Total AMOUNT loaned $"+str(i[0]))
        tot=i[0]
    print("Total Loan Amount Payed by Customers:"+str(tot-owe))
    print("\nAll accounts at "+branch)
    mycurse.execute("select a.acc_no as Account_Number,c.cus_ssn as customer_ssn,c.cname as Name ,a.balance as Balance ,a.acc_type as Account_Type,c.emp_ssn as personal_banker,e.bank_name from accounts a join maintains m on a.acc_no=m.acc_no join customers c on c.cus_ssn=m.cus_ssn join employee e on e.emp_ssn=c.emp_ssn where e.bank_name='"+str(branch)+"';")
    for i in mycurse:
        print(i)
    print("\nAll loans taken at "+branch)
    mycurse.execute("select l.loan_id as LOAN_NO,c.cus_ssn as SSN_NO ,c.cname AS BORROWER ,c.emp_ssn As SANCTIONED_BY,l.loan_amount LOAN_AMOUNT,l.owe as LOAN_PAID,e.Bank_name as Branch from customers c join takes t on c.cus_ssn=t.cus_ssn join loans l on t.loan_id=l.loan_id join employee e on c.emp_ssn=e.emp_ssn where e.bank_name='"+str(branch)+"';")
    for i in mycurse:
        print(i)

       
    


# 4.1
# createaccount(105,902,"","","",526,"'checking'")
# 4.2
# createloan(902,302,10000)
# createloan(902,303,50000)
# checkloans(902)
# 4.3
# createemp(112,'Sai Reddy Bovvila',682445990,'meg','1995-02-18','CHASE_400')
# 4.4
# loan_payment(302,402,5000)
# 4.5
# createaccount(105,902,"","","",528,"'savings'")
# 4.6
# addbranch('CHASE-750','Mallapuram',105)

# 5
# branchloans('CHASE_305')

# pay loan
# loandata(302)
# loan_payment(302,123,5000)
# loandata(302)