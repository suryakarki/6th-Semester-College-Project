import cx_Oracle

class Transfer:
    def __init__(self):
        pass
    def transfer(self):
        con = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = con.cursor()
        # Transfer Money
        print('\n\n\t\tTransfer Money Into Another Account')
        atype = input('\tEnter account type(savings/current): ')
        if atype == 'savings':
                acc = input('Enter Your Account Number: ')
                try:
                    cur.execute("select S_ACCOUNT_NO,BALANCE,STATUS from savings_account_details where S_ACCOUNT_NO=:1",(acc,))
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        f = 1
                        while f == 1:
                            tra = input('Transfer Amount: Rs.')
                            if float(tra) <= 0:
                                print("\tTransfer Amount cannot be equal to or less than Rs.0.\nPlease enter correct amount.")
                            elif float(tra) > bal:
                                print("\tTransfer Amount cannot be greater than available account balance.\nPlease enter correct amount.")
                            else:
                                break
                        bacc = input("Enter Beneficiary Account Number: ")
                        try:
                            cur.execute("select ACCOUNT_NO from account_details where ACCOUNT_NO=:a",{'a': bacc})
                            bad = cur.fetchall()
                            ban = bad[0][0]
                            if ban == int(bacc):
                                try:
                                    cur.execute("select S_ACCOUNT_NO,BALANCE,STATUS from savings_account_details where S_ACCOUNT_NO=:a",
                                                {'a': bacc})
                                    bsad = cur.fetchall()
                                    bsan = bsad[0][0]
                                    bsst = bsad[0][2]
                                    if bsan == int(bacc) and bsst == 'OPEN':
                                        bbal = bsad[0][1]
                                        bbal = bbal + float(tra)
                                        bal = bal - float(tra)
                                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",
                                                    (bal,acc,))
                                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",
                                                    (bbal,bacc,))
                                        con.commit()
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                                    (bacc,tra,bbal,))
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                                    (acc,tra,bal,))
                                        con.commit()
                                        print('\tTransfer Successful\n\tSavings Account Balance: Rs.',bal)
                                    else:
                                        print("\tBeneficiary account is blocked")
                                except Exception as e:
                                    print("Error Savings Beneficiary Account Section: ",e)
                                try:
                                    cur.execute("select C_ACCOUNT_NO,BALANCE,STATUS from current_account_details where C_ACCOUNT_NO=:a",
                                                {'a': acc})
                                    bcad = cur.fetchall()
                                    bcan = bcad[0][0]
                                    bcst = bcad[0][2]
                                    if bcan == int(bacc) and bcst == 'OPEN':
                                        bbal = bcad[0][1]
                                        bbal = bbal + float(tra)
                                        bal = bal - float(tra)
                                        cur.execute("UPDATE current_account_details SET BALANCE=:1 WHERE C_ACCOUNT_NO=:2",
                                                    (bal,acc,))
                                        cur.execute("UPDATE savings_account_details SET BALANCE=:b WHERE C_ACCOUNT_NO=:a",
                                                    (bbal,bacc,))
                                        con.commit()
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                                    (bacc, tra, bbal,))
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                                    (acc, tra, bal,))
                                        con.commit()
                                        print('\n\tTransfer Successful\n\tCurrent Account Balance: Rs.',bal)
                                except Exception as e:
                                    print("Error Current Beneficiary Account Section: ",e)
                        except Exception as e:
                            print("Error Beneficiary Account Section: ",e)
                            print("\n\tInvalid Beneficiary Account Number.\n\tTransfer Unsuccessful.Please try again!!")
                except Exception as e:
                    print("Error Savings Account Section: ",e)
                    print("\tAccount doesn't exit")
                    print('\n\tCannot Transfer given amount!!\n\tTry again!!')
        elif (atype == 'current'):
                acc = input('Enter Your Account Number: ')
                try:
                    cur.execute("select C_ACCOUNT_NO,BALANCE,STATUS from current_account_details where C_ACCOUNT_NO=:a",
                                {'a': acc})
                    ad = cur.fetchall()
                    an = ad[0][0]
                    st = ad[0][2]
                    if an == int(acc) and st == 'OPEN':
                        bal = ad[0][1]
                        f = 1
                        while f != 0:
                            tra = input('Transfer Amount: Rs.')
                            if float(tra) <= 0:
                                print("\tTransfer Amount cannot be equal to or less than Rs.0.\nPlease enter correct amount.")
                            elif float(tra) > bal:
                                print("\tTrandfer Amount cannot be greater than available account balance.\nPlease enter correct amount.")
                            elif bal - float(tra) < 5000:
                                print("\tCurrent Account Balance will become less than Rs.5000.\nPlease enter correct amount.")
                            else:
                                f = 0
                        bacc = input("Enter Beneficiary Account Number: ")
                        try:
                            cur.execute("select ACCOUNT_NO from account_details where ACCOUNT_NO=:a",{'a': bacc})
                            bad = cur.fetchall()
                            ban = bad[0][0]
                            if ban == int(bacc):
                                try:
                                    cur.execute("select S_ACCOUNT_NO,BALANCE,STATUS from savings_account_details where S_ACCOUNT_NO=:a",
                                                {'a': bacc})
                                    bsad = cur.fetchall()
                                    bsan = bsad[0][0]
                                    bsst = bsad[0][2]
                                    if bsan == int(bacc) and bsst == 'OPEN':
                                        bbal = bsad[0][1]
                                        bbal = bbal + float(tra)
                                        bal = bal - float(tra)
                                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",
                                            (bal, acc,))
                                        cur.execute("UPDATE savings_account_details SET BALANCE=:1 WHERE S_ACCOUNT_NO=:2",
                                            (bbal, bacc,))
                                        con.commit()
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                            (bacc, tra, bbal,))
                                        cur.execute("INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                            (acc, tra, bal,))
                                        con.commit()
                                        print('\n\tTransfer Successful\n\tSavings Account Balance: Rs.', bal)
                                except Exception as e:
                                    pass
                                    '''print("Error Savings Beneficiary Account Section: ", e)'''
                                try:
                                    cur.execute("select C_ACCOUNT_NO,BALANCE,STATUS from current_account_details where C_ACCOUNT_NO=:a",
                                        {'a': bacc})
                                    bcad = cur.fetchall()
                                    bcan = bcad[0][0]
                                    bcst = bcad[0][2]
                                    if bcan == int(bacc) and bcst == 'OPEN':
                                        bbal = bcad[0][1]
                                        bbal = bbal + float(tra)
                                        bal = bal - float(tra)
                                        cur.execute(
                                            "UPDATE current_account_details SET BALANCE=:1 WHERE C_ACCOUNT_NO=:2",
                                            (bal, acc,))
                                        cur.execute(
                                            "UPDATE savings_account_details SET BALANCE=:1 WHERE C_ACCOUNT_NO=:2",
                                            (bbal, bacc,))
                                        con.commit()
                                        cur.execute(
                                            "INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,:2,0,:3,SYSDATE)",
                                            (bacc, tra, bbal,))
                                        cur.execute(
                                            "INSERT INTO transaction_details (TRANSACTION_ID,ACCOUNT_NO,CREDIT,DEBIT,CUR_BALANCE,TRAN_DATE) VALUES(transac_seq.NEXTVAL,:1,0,:2,:3,SYSDATE)",
                                            (acc, tra, bal,))
                                        con.commit()
                                        print('\tTransfer Successful\n\tCurrent Account Balance: Rs.', bal)
                                    else:
                                        print("Beneficiary account is closed/blocked")
                                except:
                                    pass
                                    '''print("Error Current Beneficiary Account Section: ", e)'''
                        except:
                            '''print("Error Beneficiary Account Section: ", e)'''
                            print("\tInvalid Beneficiary Account Number.\n\tTransfer Unsuccessful.Please try again!!")
                except:
                    #print("Error Current Account Section: ", e)
                    print("\tAccount doesn't exit")
                    print('\tCannot Transfer given amount!!\n\tTry again!!')
        con.close()
#t=Transfer()
#t.transfer()