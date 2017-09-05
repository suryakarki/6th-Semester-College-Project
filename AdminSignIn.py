import cx_Oracle
import AdminMenu

class Adminsignin:
    def checkDetails(self):
        db = cx_Oracle.connect('surya/peace@localhost/xe')
        cur = db.cursor()
        i = 1
        self.count = 0
        print("\n\n\t\tAdmin Sign In\n")
        while (i != 0):
            self.name = input("Enter Admin Username: ")
            try:
                cur.execute("select user_name from users where user_name=:n", {'n': self.name})
                self.user = cur.fetchall()
                self.admin = self.user[0][0]
                if (self.admin == self.name):
                    i = 0

            except:
                print("Invalid username.Please Enter again!")
                i = 1
        i = 1
        while (i != 0):
            self.pwd = input("Enter password:")
            try:
                cur.execute("select password from users where password=:m and user_name=:n",
                            {'m': self.pwd, 'n': self.name})
                self.u = cur.fetchall()
                self.p = self.u[0][0]
                if (self.p == self.pwd):
                    print("\n\tSuccessfully logged in as Admin")
                    self.count = 0
                    try:
                        a = AdminMenu.Adminmenu()
                        a.menu()
                    except Exception as e:
                        print('Error in Admin Menu: ',e)
                    i = 0
            except:
                print("Invalid password.Please Enter again")
                self.count = self.count + 1
                i = 1
                if (self.count == 3):
                    print("\n\n\tSorry! You have made 3 unsuccessful attempts!You are Bloced!")
                    break

    def __init__(self):
        pass
#asi=Adminsignin()
#asi.checkDetails()