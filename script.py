
import mysql.connector
cnx = mysql.connector.connect(host='localhost',user='root', password='root',database='project4')
mycurse=cnx.cursor()
fb = open("banks.csv", "r")
fe = open("employee.csv", "r")
fc = open("customers.csv", "r")

def insert(fil,tname):
    for i in fil:
        mycurse.execute("Insert into "+tname+" values("+i+");")
    cnx.commit()
    print("success")

 
def select(dbname):
    mycurse.execute('select * from '+dbname+';')
    for i in mycurse:
        print(i)
    print("success")

def create(fe,fb,fc):
      mycurse.execute("CREATE TABLE EMPLOYEE(EMP_SSN INTEGER,NAME VARCHAR(100),TELEPHONE INTEGER UNIQUE,DEPENDANT VARCHAR(100),START_DATE DATE,DURATION INTEGER,BANK_NAME VARCHAR(100),PRIMARY KEY(EMP_SSN));")
      cnx.commit()
      insert(fe,"employee")
      mycurse.execute("CREATE TABLE BANKS(BANK_NAME VARCHAR(100), CITY VARCHAR(100) UNIQUE,MANAGER_SSN INTEGER,PRIMARY KEY(BANK_NAME),FOREIGN KEY(MANAGER_SSN) REFERENCES EMPLOYEE(EMP_SSN));")
      cnx.commit()
      insert(fb,"banks")
      mycurse.execute("ALTER TABLE EMPLOYEE ADD FOREIGN KEY(BANK_NAME) REFERENCES BANKS(BANK_NAME);")
      cnx.commit()
# alternative 
      mycurse.execute("CREATE TABLE CUSTOMERS(CUS_SSN INTEGER,CNAME VARCHAR(100),STREET VARCHAR(100),CITY VARCHAR(100),EMP_SSN INTEGER,PRIMARY KEY(CUS_SSN),FOREIGN KEY(EMP_SSN) REFERENCES EMPLOYEE(EMP_SSN));")
      cnx.commit()
      insert(fc,"customers")
create(fe,fb,fc)
print('done')
cnx.close()