import cx_Oracle

class Withdrawal:
    def __init__(self):
        pass
    def withdrawal(self):
        con = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = con.cursor()
        print('\n\n\t\tMoney Withdrawal')
        type = input('\n\tEnter account type(savings/current): ')
        if type == 'savings':
                acc = input('Enter Account Number: ')
                try:
                    cur.execute("select S_ACCOUNT_NO,BALANCE,STATUS from savings_account_details where S_ACCOUNT_NO=:a",
                                {'a': acc})
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        f = 1
                        while f != 0:
                            wit = input('Withdrawal Amount: Rs.')
                            if float(wit) <= 0:
                                print(
                                    "\tWithdrawal Amount cannot be equal to or less than Rs.0.\nPlease enter correct amount.")
                            elif float(wit) > bal:
                                print(
                                    "\tWithdrawal Amount cannot be greater than available account balance.\nPlease enter correct amount.")
                            else:
                                f = 0
                        bal = bal - float(wit)
                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",(bal, acc,))
                        con.commit()
                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                    (an,wit,bal,))
                        con.commit()
                        print("\tWithdrawal Successful")
                        print('\n\tSavings Account Balance: Rs.',bal)
                except Exception as e:
                    pass
                    '''print("Error Savings Account Section: ", e)
                    print("\tAccount doesn't exit")
                    print('\n\tCannot Withdraw given amount!!\n\tTry again!!')'''
        elif type == 'current':
                acc = input('Enter Account Number: ')
                try:
                    cur.execute("select C_ACCOUNT_NO,BALANCE,STATUS from current_account_details where C_ACCOUNT_NO=:a",{'a': acc})
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        f = 1
                        while f != 0:
                            wit = input('Withdrawal Amount: Rs.')
                            if (float(wit) <= 0):
                                print("\tWithdrawal Amount cannot be equal to or less than Rs.0.\nPlease enter correct amount.")
                            elif (float(wit) > bal):
                                print("\tWithdrawal Amount cannot be greater than available account balance.\nPlease enter correct amount.")
                            elif (bal - float(wit) < 5000):
                                print("\tCurrent Account Balance will become less than Rs.5000.\nPlease enter correct amount.")
                            else:
                                f = 0
                        bal = bal - float(wit)
                        cur.execute("UPDATE current_account_details SET BALANCE=:1 WHERE C_ACCOUNT_NO=:2",(bal,acc,))
                        con.commit()
                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                    (an,wit,bal,))
                        con.commit()
                        print('\tCurrent Account Balance: Rs.', bal)
                except Exception as e:
                    pass
                    '''print("Error Current Account Section: ", e)
                    print("\tAccount doesn't exit")
                    print('\tCannot Withdraw given amount!!\n\tTry again!!')'''
        con.close()
#w=Withdrawal()
#w.withdrawal()

