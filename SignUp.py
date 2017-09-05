import cx_Oracle
import re

class Signup:
    def __init__(self):
        self.fname = ''
        self.lname = ''
        self.gen = ''
        self.mob = 0
        self.eml = ''
        self.al1 = ''
        self.al2 = ''
        self.addr = ''
        self.city = ''
        self.state = ''
        self.pin = 0
        self.atype = ''
        self.bal = 0
        self.password = ''
    def enterDetails(self):
        print("\n\t\tEnter your details")
        self.fname=input('First name: ')
        self.lname=input('Last name: ')
        self.gen=input('Gender: ')
        self.mob=input('Mobile Number: ')
        self.eml=input('E-mail: ')
        self.al1=input('Address Line 1: ')
        self.al2=input('Address Line 2: ')
        self.addr=self.al1+' '+self.al2
        self.city=input('City: ')
        self.state=input('State: ')
        f=1
        while(f != 0):
            self.pin=input('Pincode: ')
            temp=self.pin
            if(len(str(temp)) != 6):
                print("Pincode should be of 6 digits.")
            else:
                f=0
        self.atype=input('Account Type(savings/current): ')
        f=1
        while(f != 0):
            self.bal=input('Starting balance to be deposited: Rs.')
            tbal=self.bal
            if self.atype == 'savings' and int(self.bal) < 0:
                print('Entered balance cannot be less than 0.\nPlease enter correct amount.')
            elif self.atype == 'current' and int(self.bal) < 5000:
                print('Minimum balance in a current account should be 5000.\nPlease enter correct amount.')
            else:
                f=0
        #print('working before database connection')
        try:
            con = cx_Oracle.connect('surya/peace@localhost/xe')
            cur = con.cursor()
            cur.execute(
                'INSERT INTO customer_details (CUSTOMER_ID,FIRST_NAME,LAST_NAME,GENDER,MOBILE,EMAIL,ADDRESS,CITY,STATE,PINCODE,CREATED_ON) VALUES(customer_seq.nextval,:1,:2,:3,:4,:5,:6,:7,:8,:9,SYSDATE)',
                (self.fname, self.lname, self.gen, self.mob, self.eml, self.addr, self.city, self.state, self.pin,))
            cur.execute(
                'INSERT INTO account_details (ACCOUNT_NO,CUSTOMER_ID) VALUES(customer_seq.currval,customer_seq.currval)')
            if (self.atype == 'savings'):
                cur.execute(
                    "INSERT INTO savings_account_details (S_ACCOUNT_NO,CUSTOMER_ID,BALANCE,CREATED_ON,LAST_ACCESSED) VALUES(customer_seq.currval,customer_seq.currval,:1,SYSDATE,SYSDATE)",
                    (self.bal,))
            if (self.atype == 'current'):
                cur.execute(
                    "INSERT INTO current_account_details (C_ACCOUNT_NO,CUSTOMER_ID,BALANCE,CREATED_ON,LAST_ACCESSED) VALUES(customer_seq.currval,customer_seq.currval,:1,SYSDATE,SYSDATE)",
                    (self.bal,))
            print("\tYour Account has been created Successfully.")
            cur.execute(
                "INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,customer_seq.currval,:1,0,:2,SYSDATE)",
                (self.bal, self.bal))
            cur.execute('select customer_seq.currval from dual')
            custid = cur.fetchall()
            print("\tCustomer Id: ", custid[0][0])
            print("\tAccount Number: ", custid[0][0])
            f = 1
            while (f != 0):
                self.password = input("\n\n\tEnter password: ")
                if (len(str(self.password)) >= 8 and re.match('[a-zA-Z0-9]+', str(self.password))):
                    f = 0
                else:
                    print("\n\tPassword should be minimum of 8 characters (Alphabets or Number only).")
            con.commit()
            f = 1
            while (f != 0):
                cpassword = input("\tConfirm password: ")
                if (cpassword == self.password):
                    cur.execute("UPDATE customer_details SET PASSWORD=:1 WHERE CUSTOMER_ID=:2",
                                (cpassword, custid[0][0],))
                    f = 0
                else:
                    print("\tPassword should be minimum of 8 characters (Alphabets or Number only).")
            con.commit()
            cur.close()
            con.close()
            print("\tYour account password has been created.\n\n\tSelect Sign In for logging into your account.")
        except:
            print("Enter unique and correct details. Try Again!!")
#s=Signup()
#s.enterDetails()