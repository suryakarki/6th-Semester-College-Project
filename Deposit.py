import cx_Oracle

class Deposit:
    def __init__(self):
        pass
    def deposit(self):
        con = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = con.cursor()
        print('\n\n\t\tMoney Deposit')
        f = 1
        while (f != 0):
            dep = input('Deposit Amount: Rs.')
            if float(dep) <= 0:
                print("\tDeposit Amount cannot be equal to or less than Rs.0.\nPlease enter correct amount.")
            else:
                f = 0
        acc = input('Enter Account Number: ')
        try:
            cur.execute("select ACCOUNT_NO from account_details where ACCOUNT_NO=:a",{'a': acc})
            user = cur.fetchall()
            ac = user[0][0]
            if ac == int(acc):
                try:
                    cur.execute("select S_ACCOUNT_NO,BALANCE,STATUS from savings_account_details where S_ACCOUNT_NO=:a",{'a': acc})
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        bal = bal + float(dep)
                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",(bal,acc,))
                        con.commit()
                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                    (an,dep,bal,))
                        con.commit()
                        print('\tDeposit Successful in Savings Account')
                        print('\tSavings Account Balance: Rs.',bal)
                except Exception as e:
                    print("Error Savings Account Section: ", e)
                try:
                    cur.execute("select C_ACCOUNT_NO,BALANCE,STATUS from current_account_details where C_ACCOUNT_NO=:a",{'a': acc})
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        bal = bal + float(dep)
                        cur.execute("UPDATE current_account_details SET BALANCE=:1 WHERE C_ACCOUNT_NO=:2",(bal,acc,))
                        con.commit()
                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                    (an,dep,bal,))
                        con.commit()
                        print('\tCurrent Account Balance: Rs.',bal)
                except Exception as e:
                    print("Error Current Account Section: ",e)
        except Exception as e:
            print("ERROR Account Section:",e)
            print("\tAccount doesn't exit")
            print('\tDeposit Failed!!\n\tTry again!!')
        con.close()
#d=Deposit()
#d.deposit()