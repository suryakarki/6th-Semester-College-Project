import cx_Oracle

class ClosedAcc:
    def __init__(self):
        pass
    def closed(self):
        db = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = db.cursor()
        # printing closed account history
        print("\n\n\t\tClosed Accounts History\n\n")
        try:
            cur.execute("select S_ACCOUNT_NO,CLOSED_ON from SAVINGS_ACCOUNT_DETAILS where status='CLOSED'")
            a = cur.fetchall()
            if a[0][0]!= None:
                print("\tClosed Savings Accounts:")
                print("\tClosed Account Number\tClosed On")
                for i in range(0,cur.rowcount):
                    print("\t\t  ",a[i][0],"\t\t\t ",a[i][1])
        except:
            print("\tNo Savings Account Have been closed")
        try:
            cur.execute("select C_ACCOUNT_NO,CLOSED_ON from CURRENT_ACCOUNT_DETAILS where status='CLOSED'")
            cad = cur.fetchall()
            if cad[0][0] != None:
                print("\tClosed Current Accounts:\n")
                print("\tClosed Account Number\tClosed On")
                for i in range(0, cur.rowcount):
                    print("\t\t  ",cad[i][0],"\t\t\t ",cad[i][1])
        except:
            print("\tNo Current Account Have been closed")
#ca=ClosedAcc()
#ca.closed()