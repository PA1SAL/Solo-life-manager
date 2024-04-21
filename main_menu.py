from tkinter import *
from PIL import Image, ImageTk
import subprocess

class MenuPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Menu Page")
        self.master.geometry("1024x492")

        # Load background image using Pillow
        self.bg_image = Image.open("background_image.jpeg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = Label(self.master, text="Welcome to the Menu Page", font=("Arial", 20))
        self.label.pack(pady=20)

        self.button_module1 = Button(self.master, text="Due Date Reminder", command=self.open_module1)
        self.button_module1.pack(pady=10)

        self.button_module2 = Button(self.master, text="Expense Tracker", command=self.open_module2)
        self.button_module2.pack(pady=10)

        self.button_module3 = Button(self.master, text="Meal Suggestions", command=self.open_module3)
        self.button_module3.pack(pady=10)

        self.button_module4 = Button(self.master, text="Log Out", command=self.open_module4)
        self.button_module4.pack(pady=10)

    def open_module1(self):
        subprocess.Popen(["python", "appointment.py"])

    def open_module2(self):
        subprocess.Popen(["python", "expense.py"])

    def open_module3(self):
        subprocess.Popen(["python", "cluster.py"])

    def open_module4(self):
        subprocess.Popen(["python", "module4.py"])

def main():
    root = Tk()
    menu_page = MenuPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
