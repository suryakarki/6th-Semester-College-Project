import cx_Oracle
import Deposit
import Withdrawal
import Transfer

class Signin:
    def __init__(self):
        self.cid = 0
        self.al1 = ''
        self.al2 = ''
        self.addr =''
        self.city = ''
        self.state = ''
        self.pin=0
    def checkDetails(self):
        con = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = con.cursor()
        i = 0
        d = 1
        count = 0
        print("\n\n\t\tSign In To Your Account\n")
        while (i != 1):
            cust = input("Enter Customer Id: ")
            try:
                cur.execute("select CUSTOMER_ID,STATUS from CUSTOMER_DETAILS where CUSTOMER_ID=:1", (cust,))
                user1 = cur.fetchall()
                self.cid = user1[0][0]
                '''print(cid)'''
                if (self.cid == int(cust)):
                    cst = user1[0][1]
                    if (cst == 'OPEN'):
                        break
                    else:
                        print("Your Account is Blocked/Closed.")
                        d = 0
                    break
            except:
                print("Invalid customer id.Please Enter again!")
        while (d != 0):
            pwd = input("Enter password:")
            try:
                cur.execute("select password from CUSTOMER_DETAILS where password=:m and CUSTOMER_ID=:1",
                            (pwd,self.cid,))
                u = cur.fetchall()
                p = u[0][0]
                if (p == pwd):
                    print("\n\tSuccessfully Logged In!")
                    count = 0
                    ach = 0
                    while (ach != 7):
                        print('\n\t\tUser Menu')
                        print('\n\t1.Address Change')
                        print('\n\t2.Money Deposit')
                        print('\n\t3.Money Withdrawal')
                        print('\n\t4.Print Statement')
                        print('\n\t5.Transfer Money')
                        print('\n\t6.Account Closure')
                        print('\n\t7.Customer Logout')
                        adch = input("\n\nSelect Option: ")
                        if adch == '1':
                            print('\n\n\t\tEnter New Address Details')
                            self.al1 = input('Address Line 1: ')
                            self.al2 = input('Address Line 2: ')
                            self.addr = self.al1 + ' ' + self.al2
                            self.city = input('City: ')
                            self.state = input('State: ')
                            f = 1
                            while(f != 0):
                                 self.pin=input('Pincode: ')
                                 tmp=self.pin
                                 if(len(str(tmp)) != 6):
                                     print("Pincode should be of 6 digits.")
                                 else:
                                     f=0
                            try:
                                cur.execute("UPDATE customer_details SET ADDRESS=:1,CITY=:2,STATE=:3,PINCODE=:4 WHERE CUSTOMER_ID=:5",
                                            (self.addr, self.city, self.state, self.pin, self.cid,))
                                con.commit()
                                print('\tAddress has been successfully updated')
                            except Exception as e:
                                print(e)
                                print("\tAddress Update Failed!! Try again")
                        elif adch == '2':
                            try:
                                dep=Deposit.Deposit()
                                dep.deposit()
                            except Exception as e:
                                print("Error: ",e)
                        elif adch == '3':
                            try:
                                w = Withdrawal.Withdrawal()
                                w.withdrawal()
                            except Exception as e:
                                print("Error: ", e)
                        elif adch == '4':
                            print('\n\n\t\tPrint Statement')
                            acc = input('Enter Account Number: ')
                            try:
                                cur.execute("select ACCOUNT_NO from account_details where ACCOUNT_NO=:a AND CUSTOMER_ID=:c",
                                            {'a': acc,'c':self.cid})
                                user = cur.fetchall()
                                ac = user[0][0]
                                if ac == int(acc):
                                    tag = 1
                                    '''while (tag != 0):
                                        dateto = input("Enter Date To(mm/dd/yyyy): ")
                                        datefr = input("Enter Date From(mm/dd/yyyy): ")
                                        import time
                                        dt = time.strptime(dateto, "%m/%d/%Y")
                                        df = time.strptime(datefr, "%m/%d/%Y")
                                        if (dt > df):
                                            tag = 0
                                        else:
                                            print("\tDate To should be greater than Date From.\n\tEnter correct dates.")'''
                                    try:
                                        cur.execute("select TRAN_DATE,CREDIT,DEBIT,CUR_BALANCE,ACCOUNT_NO from transaction_details where ACCOUNT_NO=:a",
                                                    {'a': acc,})
                                        ad = cur.fetchall()
                                        an = ad[0][4]
                                        if an == int(acc):
                                            print("\t   Transaction DATE\t\tTRANSACTION TYPE\tAMOUNT\tBALANCE")
                                            for i in range(0,cur.rowcount):
                                                if ad[i][1] == 0:
                                                    print("\t",ad[i][0],"\t\tDebit\t\t   ",ad[i][2]," ",ad[i][3])
                                                else:
                                                    print("\t",ad[i][0],"\t\tCredit\t\t   ",ad[i][1]," ",ad[i][3])
                                    except Exception as e:
                                        print(e)
                                        print("\tNo Transaction Record Found. Customer has not performed any transactions.")
                            except Exception as e:
                                print(e)
                                print('\tInvalid Account Number!!\n\tTry again!!')
                        elif adch == '5':
                            try:
                                tra = Transfer.Transfer()
                                tra.transfer()
                            except:
                                pass
                                #print("Error: ", e)
                        elif adch == '6':
                            print('\n\n\t\tAccount Closure')
                            acc= input('Enter Account Number: ')
                            try:
                                cur.execute("select ACCOUNT_NO from account_details where ACCOUNT_NO=:a AND CUSTOMER_ID=:c",
                                            {'a': acc,'c':self.cid})
                                user = cur.fetchall()
                                ac = user[0][0]
                                if ac == int(acc):
                                    try:
                                        cur.execute("select S_ACCOUNT_NO,BALANCE from savings_account_details where S_ACCOUNT_NO=:1",
                                                    (acc,))
                                        ad = cur.fetchall()
                                        an = ad[0][0]
                                        if an == int(acc):
                                            b = ad[0][1]
                                            if b >= 2000:
                                                b = b - 2000
                                            cur.execute("UPDATE savings_account_details SET STATUS='CLOSED',BALANCE=:1 WHERE S_ACCOUNT_NO=:2",
                                                        (b,acc,))
                                            cur.execute("UPDATE customer_details SET STATUS='CLOSED' WHERE CUSTOMER_ID=:1",
                                                        (self.cid,))
                                            con.commit()
                                            print("\tYour Savings Account ",an," has been closed successfully.")
                                            print("\tAn amount of Rs.",b," will be send to your address.")
                                            print("\tRs.2000 has been reduced from your account as account closure fee.")
                                    except Exception as e:
                                        print(e)
                                    try:
                                        cur.execute("select C_ACCOUNT_NO,BALANCE from current_account_details where C_ACCOUNT_NO=:1",
                                                    (acc,))
                                        ad = cur.fetchall()
                                        an = ad[0][0]
                                        if an == int(acc):
                                            b = ad[0][1]
                                            if b >= 2000:
                                                b = b - 2000
                                            cur.execute("UPDATE current_account_details SET STATUS='CLOSED',BALANCE=::1 WHERE C_ACCOUNT_NO=:2",
                                                        (acc,))
                                            cur.execute("UPDATE customer_details SET STATUS='CLOSED' WHERE CUSTOMER_ID=:1",
                                                        (self.cid,))
                                            con.commit()
                                            print("\tYour Current Account ",acc,"has been closed successfully.")
                                            print("\tAn amount of Rs.",b," will be send to your address.")
                                            print("Rs.2000 has been reduced from your account as account closure fee.")
                                    except Exception as e:
                                        print("ERROR: ",e)
                            except Exception as e:
                                print(e)
                                print("Account doesn't belong to your customer id")
                        elif adch == '7':
                            ach = 7
                        else:
                            print("Wrong Choice Entered. Please Enter Correct Choice")
                    break
            except:
                print("Invalid password.Please Enter again")
                count = count + 1
                if (count == 3):
                    print("\n\n\tSorry! You have made 3 unsuccessful attempts!Your account is Bloced!")
                    cur.execute("UPDATE customer_details SET STATUS='BLOCKED' WHERE CUSTOMER_ID=:1", (self.cid,))
                    con.commit()
                    break
        con.close()
#s=Signin()
#s.checkDetails()