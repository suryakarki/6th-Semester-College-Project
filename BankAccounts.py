import SignUp
import SignIn
import AdminSignIn

class Bankaccount:
    def __init__(self):
        pass
    def mainmenu(self):
        ch=0
        while( ch != 4 ):
            print ('\n\n\t\tMAIN MENU\n')
            print ('\t1. Sign Up(New Customer)')
            print ('\t2. Sign In(Existing Customer)')
            print ('\t3. Admin Sign In')
            print ('\t4. Quit')
            choice=input("\n\nSelect Option: ")
            if( choice == '1' ):
                su=SignUp.Signup()
                su.enterDetails()
            elif( choice == '2' ):
                si=SignIn.Signin()
                si.checkDetails()
            elif( choice == '3' ):
                asi=AdminSignIn.Adminsignin()
                asi.checkDetails()
            elif( choice == '4' ):
                print('\n\n\n\t\t~!~Thanks For Visiting Our Bank~!~')
                ch=4
            else:
                print("Wrong Choice Entered. Please Enter Correct Choice")
bankobj=Bankaccount()
bankobj.mainmenu()