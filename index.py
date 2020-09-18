from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import sqlite3
import os
from datetime import datetime
from PyQt5.uic import loadUiType

# coursesUi,course_iu = loadUiType('courses.ui')
loginUi, onboarding = loadUiType('Login.ui')
ui,_ = loadUiType('Main.ui')
con = sqlite3.connect("database.db")
cur = con.cursor()




class MainApp(QMainWindow, loginUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.LoginButton.clicked.connect(self.Login)
        # self.pushButton_2.clicked.connect(self.Exit_Button)
        self.show()

    def Login(self):
        email = self.EmailInput.text()
        password = self.PasswordInput.text()

        if(email == 'admin@admin.com' and password == 'admin'):
            self.display = Home()
            self.display.show()
            self.close()
            print("Match")
        else:
            print('not found')

        print(email)
        print(password)

    def Start_Button(self):
        self.display = Home()
        self.display.show()
        self.close()

    def Exit_Button(self):
        self.close()


class Home(_, ui,):
    def __init__(self):
        _.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.setWindowTitle("Nigerian Defence Academy Attendance System")
        self.show()
        # self.getCourses()
        # self.handle_UI_Changes()


    def Handle_Buttons(self):
        self.AddCrimeButton.clicked.connect(self.Add_A_Crime_Tab)
        self.pushButton_4.clicked.connect(self.Add_A_New_User_Tab)
        self.pushButton_7.clicked.connect(self.Add_New_User_Button)
        self.pushButton_8.clicked.connect(self.Add_Crime_Button)
        self.pushButton_3.clicked.connect(self.Search_User)

    def Add_A_Crime_Tab(self):
        self.tabWidget.setCurrentIndex(2)
        # print(self.listWidget.count ())     
        pass

    def Add_A_New_User_Tab(self):
        global searched_id
        cursorr = con.cursor()
        cursorr.execute("SELECT ndaNumber FROM cardets")
        result = cursorr.fetchall()
        cursorr.close()
        cardetquery = self.lineEdit_4.text().upper()
        searched_id = cardetquery
        print(type(cardetquery))
        search_list = [index for (index, a_tuple) in enumerate(result) if a_tuple[0]==cardetquery]
        print(search_list)
        if search_list == []:
            self.tabWidget.setCurrentIndex(3)
            print("Cardet not found")
        else:
            self.tabWidget.setCurrentIndex(4)
            print("Create a new user")
    
    def Add_New_User_Button(self):
        cursorr = con.cursor()
        cursorrs = con.cursor()
        name=self.fullname.text()
        ndaNumber=self.ndanumber.text().upper()
        department=self.department.text()
        state=self.state.text()
        crimeDescription=self.description.text()
        query ="INSERT INTO cardets (name, ndaNumber, department, state, crimeDescription) VALUES(?,?,?,?,?)"
        query2 ="INSERT INTO crime (ndaNumber, description, date) VALUES(?,?,?)"
        cursorr.execute(query,(name,ndaNumber,department,state,crimeDescription))
        cursorrs.execute(query2,(ndaNumber,crimeDescription, datetime.now()))
        con.commit()
        cursorr.close()
        cursorrs.close()
        self.tabWidget.setCurrentIndex(0)
        QMessageBox.information(self,"Success","Student has been added")

    def Add_Crime_Button(self):
        global searched_id
        cursorr = con.cursor()
        description = self.textEdit.toPlainText()
        query ="INSERT INTO crime (ndaNumber, description, date) VALUES(?,?,?)"
        cursorr.execute(query,(searched_id,description, datetime.now()))
        con.commit()
        cursorr.close()
        self.tabWidget.setCurrentIndex(0)
        QMessageBox.information(self,"Success","Crime have been registered successfully")
    
    def Search_User(self):
        searchQuery = self.lineEdit_2.text().upper()
        cursorr = con.cursor()
        cursorr.execute("SELECT ndaNumber FROM cardets")
        result = cursorr.fetchall()
        cursorr.close()

        search_list = [index for (index, a_tuple) in enumerate(result) if a_tuple[0]==searchQuery]
        print(search_list)
        if search_list == []:
            QMessageBox.information(self,"Not Found!!","Cardet has no crime history")
            print("Cardet not found")
        else:
            fetcher = con.cursor()
            query=("SELECT * FROM crime WHERE ndaNumber=?")
            crimes = fetcher.execute(query, (searchQuery,)).fetchall()
            # fetcher.close()

            # fetcher2 = con.cursor()
            query2=("SELECT * FROM cardets WHERE ndaNumber=?")
            fulldata = fetcher.execute(query2, (searchQuery,)).fetchall()
            print(fulldata)
            
            print(crimes)
            print('There are '+str(len(crimes))+' records on the list')


            veebox = QVBoxLayout()
            self.groupBox_7.setLayout(veebox)
            
            mylabel = QLabel()
            mylabel.setText("Fullname: "+str(fulldata[0][1]))
            mylabel.setObjectName('mylabel')
            mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')

            mylabel2 = QLabel()
            mylabel2.setText("NDA Number: "+str(fulldata[0][2]))
            mylabel2.setObjectName('mylabel22')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')
            
            mylabel3 = QLabel()
            mylabel3.setText("Department: "+str(fulldata[0][3]))
            mylabel3.setObjectName('Department')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')
            
            mylabel4 = QLabel()
            mylabel4.setText("State: "+str(fulldata[0][4]))
            mylabel4.setObjectName('State')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')
            
            mylabel5 = QLabel()
            mylabel5.setText("Date of birth: "+str(fulldata[0][5]))
            mylabel5.setObjectName('DOB')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')

            mylabel6 = QLabel()
            mylabel6.setText("Sex: "+str(fulldata[0][6]))
            mylabel6.setObjectName('Sex')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')

            mylabel7 = QLabel()
            mylabel7.setText("Battalion: "+str(fulldata[0][7]))
            mylabel7.setObjectName('Battalion')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')

            # mylabel6 = QLabel()
            # mylabel6.setText("Crime: "+str(fulldata[0][8]))
            # mylabel6.setObjectName('Sex')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')
            
            # mylabel = QLabel()
            # mylabel.setText("Gender: "+str(fulldata[0][6]))
            # mylabel.setObjectName('Gender')
            # mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')

            veebox.addWidget(mylabel)
            veebox.addWidget(mylabel2)
            veebox.addWidget(mylabel3)
            veebox.addWidget(mylabel4)
            veebox.addWidget(mylabel5)
            veebox.addWidget(mylabel6)
            veebox.addWidget(mylabel7)
            
            

            
            dynamicVars = []
            dynamicVar2= []
            vbox = QVBoxLayout()
            self.groupBox_8.setLayout(vbox)
            for index in range(len(crimes)):
                dynamicVars.append('var'+str(index))
                dynamicVar2.append('vars'+str(index))
                print ('Current record :' + str(crimes[index][2]))
                print(dynamicVars)

                qgroupbox = QGroupBox()
                dynamicVars[index] = QGroupBox()
                mylabel = QLabel()
                mylabel.setText(str(crimes[index][2]))
                mylabel.setObjectName('mylabel'+str(index))
                mylabel.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent; font-size:18px; max-width:360px }')
                
                mylabel2 = QLabel()
                mylabel2.setText(str(crimes[index][3]))
                mylabel2.setObjectName('mylabel'+str(index))
                mylabel2.setStyleSheet('QLabel#mylabel { color:blue; background-color:transparent;}')            

                dynamicVar2[index] = QVBoxLayout()
                dynamicVar2[index].addWidget(mylabel)
                dynamicVar2[index].addWidget(mylabel2)
                dynamicVars[index].setLayout(dynamicVar2[index])
                dynamicVars[index].setStyleSheet('QGroupBox { background-color: #cccccc; border-radius:15px; max-height: 100px; max-width:400px;}')

                # qgroupbox.setLayout(vbox2)
                # qgroupbox.setStyleSheet('QGroupBox { background-color: red; border-radius:15px; max-height: 100px; max-width:400px}')

                # vbox.addWidget(qgroupbox)
                vbox.addWidget(dynamicVars[index])
                self.tabWidget.setCurrentIndex(1)
                print("See cardet's Info")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    # attendance.StartClass().show
    app.exec_()

if __name__ == '__main__':
    main()
