import ClosedAccount

class Adminmenu:
    def menu(self):
        ach=0
        while( ach != 2):
            print ('\n\t\tAdmin Menu')
            print ('\n\t1.Print Closed Account History')
            print ('\n\t2.Admin Logout')
            adch=input("\n\nSelect Option: ")
            if adch == '1':
                try:
                    ca=ClosedAccount.ClosedAcc()
                    ca.closed()
                except:
                    print("Error in Closed Account")
            elif adch == '2':
                ach=2
            else:
                print("Wrong Choice Entered. Please Enter Correct Choice.")
    def __init__(self):
        pass
#am=Adminmenu()
#am.menu()