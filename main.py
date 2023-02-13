import mysql.connector
from sshtunnel import SSHTunnelForwarder

#credentials
host_='acadmysqldb001p.uta.edu'
user_='pxc686'
password_='Yogapandu12345'
db_='pxc6866'


#method to create an ssh tunnel from local system to remote server @UTAOmega
def sshTunnel():
    tunnel = SSHTunnelForwarder(
        ('Omega.uta.edu', 22),
        ssh_username = 'pxc6866',
        ssh_password = 'Yoga#12345',
        remote_bind_address = ('127.0.0.1', 3306),
    )
    tunnel.start()
#creating connection with mysql server on uta Omega
cnx = mysql.connector.connect(host=host_,
                                            user=user_,
                                            password=password_,
                                            database=db_)

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
        for i in mycurse:
            ov=i[0]
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
def createaccount(cssn,accno,typ):
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

def loans():
    mycurse.execute("select * from players")
    for i in mycurse:
        print(i)

cnx.close()

loans()