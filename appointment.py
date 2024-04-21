# import modules
from tkinter import *
import sqlite3
import tkinter.messagebox

# connect to the databse.
conn = sqlite3.connect('database.db')
# cursor to move around the databse
c = conn.cursor()

# empty list to later append the ids from the database
ids = []

# tkinter window
class Application:
    def __init__(self, master):
        self.master = master

        # creating the frames in the master
        self.left = Frame(master, width=800, height=720, bg='grey')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=400, height=720, bg='darkblue')
        self.right.pack(side=RIGHT)

        # labels for the window
        self.heading = Label(self.left, text="Due Date Reminder", font=('arial 40 bold'), fg='black', bg='grey')
        self.heading.place(x=50, y=0)


        # age
        self.age = Label(self.left, text="Amount", font=('arial 18 bold'), fg='black', bg='grey')
        self.age.place(x=50, y=140)

        # gender
        self.gender = Label(self.left, text="Description", font=('arial 18 bold'), fg='black', bg='grey')
        self.gender.place(x=50, y=180)

        # location
        self.location = Label(self.left, text="Date", font=('arial 18 bold'), fg='black', bg='grey')
        self.location.place(x=50, y=220)

        # appointment time
        self.time = Label(self.left, text="    Time", font=('arial 18 bold'), fg='black', bg='grey')
        self.time.place(x=20, y=260)



        # Entries for all labels============================================================


        self.age_ent = Entry(self.left, width=30)
        self.age_ent.place(x=250, y=150)
    
        self.gender_ent = Entry(self.left, width=30)
        self.gender_ent.place(x=250, y=190)

        self.location_ent = Entry(self.left, width=30)
        self.location_ent.place(x=250, y=230)

        self.time_ent = Entry(self.left, width=30)
        self.time_ent.place(x=250, y=270)


        # button to perform a command
        self.submit = Button(self.left, text="Add Reminder", width=20, height=2, bg='skyblue', command=self.add_appointment)
        self.submit.place(x=250, y=360)
    
        # getting the number of appointments fixed to view in the log
        sql2 = "SELECT ID FROM appointments "
        self.result = c.execute(sql2)
        for self.row in self.result:
            self.id = self.row[0]
            ids.append(self.id)
        
        # ordering the ids
        self.new = sorted(ids)
        self.final_id = self.new[len(ids)-1]
        # displaying the logs in our right frame
        self.logs = Label(self.right, text="Logs", font=('arial 32 bold'), fg='white', bg='darkblue')
        self.logs.place(x=0, y=0)

        self.box = Text(self.right, width=50, height=40)
        self.box.place(x=20, y=60)
        self.box.insert(END, "Total Reminders till now :  " + str(self.final_id))
    # funtion to call when the submit button is clicked
    def add_appointment(self):
        # getting the user inputs
        self.val1 = self.name_ent.get()
        self.val2 = self.age_ent.get()
        self.val3 = self.gender_ent.get()
        self.val4 = self.location_ent.get()
        self.val5 = self.time_ent.get()
        self.val6 = self.phone_ent.get()

        # checking if the user input is empty
        if self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
            tkinter.messagebox.showinfo("Warning", "Please Fill Up All Boxes")
        else:
            # now we add to the database
            sql = "INSERT INTO 'appointments' (name, age, gender, location, scheduled_time, phone) VALUES(?, ?, ?, ?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5, self.val6))
            conn.commit()
            tkinter.messagebox.showinfo("Success", "Appointment for " +str(self.val1) + " has been created" )
            

            self.box.insert(END, 'Appointment fixed for ' + str(self.val1) + ' at ' + str(self.val5))

# creating the object
root = Tk()
b = Application(root)

# resolution of the window
root.geometry("1200x720+0+0")

# preventing the resize feature
root.resizable(False, False)

# end the loop
root.mainloop()