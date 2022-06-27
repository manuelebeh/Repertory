import tkinter
from tkinter import*
from tkinter.messagebox import askokcancel, askyesno, askquestion
from tkinter import ttk
import sqlite3

#création de fenêtre
window = Tk()
window.title("Repertory")
window.state('zoomed')

"""
tree_frame = Frame(window)
tree_frame.pack(pady=20)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()
tree_scroll.config(command=my_tree.yview)
"""

my_tree = ttk.Treeview()

#Style Treeview
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background = "silver",
                foreground = "black",
                rowheight = 25,
                fieldbackground = "silver"
)

style.map("Treeview",
          background = [("selected", "#F38D11")])
my_tree = ttk.Treeview(window)

#window.resizable(height = FALSE, width = FALSE)
#window.minsize(8,100)


#CREATION OF THE DATABASE
conn = sqlite3.connect("Rep.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS INFORMATIONS
        (id integer PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        age INT,
        gender TEXT,
        nationality TEXT,
        address TEXT,
        phone INT,
        mail TEXT)''')
conn.commit()
cur.close()
conn.close()


temp_label=Label(window, text="")
temp_label.pack

#CREATION OF THE VALIDATE FUNCTION
def submit_record():
    submit = askyesno("CONFIRMATION",\
                     "Voulez vous sauvegarder ?")
    if submit:
        first_name = str(fname_zone.get())
        last_name = str(lname_zone.get())
        age = int(age_zone.get())
        gender = str(gender_zone.get())
        nationality = str(nat_zone.get())
        address = str(adr_zone.get())
        phone = int(phone_zone.get())
        mail = str(mail_zone.get())
        data=(first_name,last_name,age,gender,nationality,address,phone,mail)
        conn=sqlite3.connect("Rep.db")
        cur=conn.cursor()

        cur.execute("INSERT INTO INFORMATIONS(first_name,last_name,age,gender,nationality,address,phone,mail) "
                    "VALUES(?,?,?,?,?,?,?,?)",data)
            
        conn.commit()
        cur.close()
        conn.close()

#CREATION OF THE FUNCTION TO CLOSE THE WINDOWS
def close_window():
    destr = askyesno("CLOSE WINDOWS",\
                    "Do you want to close the windows?")
    if destr:
        window.destroy()

#CREATION OF THE FUNCTION TO SELECT A RECORD
def select_record():
    fname_zone.delete(0, END)
    lname_zone.delete(0, END)
    age_zone.delete(0, END)
    gender_zone.delete(0, END)
    nat_zone.delete(0, END)
    adr_zone.delete(0, END)
    phone_zone.delete(0, END)
    mail_zone.delete(0, END)
    selected = my_tree.focus()
    values = my_tree.item()
    values = tree.item(selected, 'values')
    #temp_label.config(text = values[0])
    fname_zone.insert(0, values[0])
    lname_zone.insert(0, values[1])
    age_zone.insert(0, values[2])
    gender_zone.insert(0, values[3])
    nat_zone.insert(0, values[4])
    adr_zone.insert(0, values[5])
    phone_zone.insert(0, values[6])
    mail_zone.insert(0, values[7])

#CREATION OF THE FUNCTION TO UPDATE A RECORD
def update_record():
    selected = my_tree.focus()
    values = my_tree.item(selected, "values")
    temp_label.config()
    my_tree.item(selected, text = "", values = (fname_zone.get(), lname_zone.get(), age_zone.get(), gender_zone.get(), nat_zone.get(), adr_zone.get(), phone_zone.get(), mail_zone.get()))
    fname_zone.delete(0, END)
    lname_zone.delete(0, END)
    age_zone.delete(0, END)
    gender_zone.delete(0, END)
    nat_zone.delete(0, END)
    adr_zone.delete(0, END)
    phone_zone.delete(0, END)
    mail_zone.delete(0, END)


    """"""
    cur.execute("""UPDATE INFORMATIONS SET
    nom = :surname;
    prenom = :name;
    age = :age;
    sexe = :gender;
    nat = :nat;
    adr = :adr;
    tel = :tel;
    mail = :mail;
    
    WHERE oid = :oid""",
    {
        "surname": fname_zone.get(),
        "name": lname_zone.get(),
        "age": age_zone.get(),
        "gender": gender_zone.get(),
        "nat": nat_zone.get(),
        "adr": adr_zone.get(),
        "tel": phone_zone.get(),
        "mail": mail_zone.get(),
    })
""""""

#CREATION OF THE FUNCTION TO DELETE MANY RECORDS
def delete_many_record():
    response = tkinter.messagebox.askyesno("CONFIRMATION","Do you really want to delete this information?")
    if response == 1:
        x = my_tree.selection()
        ids_to_delete = []

        for record in x:
            ids_to_delete.append(my_tree.item())

        for record in x:
            my_tree.delete(record)

        conn = sqlite3.connect("Rep.db")
        cur = conn.cursor()

        cur.executemany("DELETE from INFORMATIONS WHERE id = ?", ids_to_delete )
        conn.commit()
        cur.close()
        conn.close()
        clear_entries()
#CREATION OF THE FUNCTION TO DELETE A RECORD
def delete_record():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    conn = sqlite3.connect("Rep.db")
    cur = conn.cursor()

    cur.execute("DELETE from INFORMATIONS WHERE oid ="+id.get())
    conn.commit()
    cur.close()
    conn.close()


#Creation of the title entry
label_title = Label(window, text = "Information Repertory", font = "arial" "bold")
label_title.grid(row = 0, column = 1)

#Creation of the First Name entry
fname_title = Label(window, text = "Name :", height = 5)
fname_title.grid(row = 1, column = 0)

fname_zone = Entry(window, width = 60)
#fname_zone.insert(1, "What is your first name ?    ")
fname_zone.grid(row = 1, column = 1)

#Creation of the Last Name entry
lname_title = Label(window, text = "Surname :", height = 5)
lname_title.grid(row = 2, column = 0)

lname_zone = Entry(window, width = 60)
#lname_zone.insert(1, "What is your name ?     ")
lname_zone.grid(row = 2, column = 1)

#Creation of the age entry
age_title = Label(window, text = "Age :", height = 5)
age_title.grid(row = 3, column = 0)

age_zone = Entry(window, width = 60)
#age_zone.insert(1, "How old are you ?     ")
age_zone.grid(row = 3, column = 1)

#Creation of the gender entry
gender_title = Label(window, text = "Gender :", height = 5)
gender_title.grid(row = 4, column = 0)

gender_zone = Entry(window, width = 60)
#gender_zone.insert(1, "Male or Female ?     ")
gender_zone.grid(row = 4, column = 1)

#Creation of the nationality entry
nat_title = Label(window, text = "Nationality :", height = 5)
nat_title.grid(row = 5, column = 0)

nat_zone = Entry(window, width = 60)
#nat_zone.insert(1, "Where are you from ?     ")
nat_zone.grid(row = 5, column = 1)

#Creation of the address entry
adr_title = Label(window, text = "Address : ", height = 5)
adr_title.grid(row = 6, column = 0)

adr_zone = Entry(window, width = 60)
#adr_zone.insert(1, "What is your address ?     ")
adr_zone.grid(row = 6, column = 1)

#Creation of the phone entry
phone_title = Label(window, text = "Phone : ", height = 5)
phone_title.grid(row = 7, column = 0)

phone_zone = Entry(window, width = 60)
#phone_zone.insert(1, "What is your cell number ?     ")
phone_zone.grid(row = 7, column = 1)
phone_zone.grid(row = 7, column = 1)

#Creation of the mail entry
mail_title = Label(window, text = "Mail : ", height = 5)
mail_title.grid(row = 8, column = 0)

mail_zone = Entry(window, width = 60)
#mail_zone.insert(1, "What is your email address ?     ")
mail_zone.grid(row = 8, column = 1)


#Button création
submit_button = Button(window, text = "ADD RECORD", command = submit_record)
submit_button.grid(row = 9, column = 0)
select_button = Button(window, text = "SELECT RECORD", command = select_record)
select_button.grid(row = 9, column = 3)
update_button = Button(window, text = "UPDATE RECORD", command = update_record)
update_button.grid(row = 9, column = 4)
delete_button = Button(window, text = "DELETE RECORD", command = delete_record)
delete_button.grid(row = 9, column = 5)
close_button = Button(window, text = "CLOSE WINDOWS", command = close_window)
close_button.grid(row = 9, column = 2)


#Création de data tk
tree = ttk.Treeview(window, column = (1,2,3,4,5,6,7,8,9), height = 5, show = "headings")
tree.place(x = 465, width = 1050, height = 600)

tree.heading(1, text = "ID")
tree.heading(2, text = "NAME")
tree.heading(3, text = "SURNAME")
tree.heading(4, text = "AGE")
tree.heading(5, text = "GENDER")
tree.heading(6, text = "NATIONALITY")
tree.heading(7, text = "ADDRESS")
tree.heading(8, text = "PHONE")
tree.heading(9, text = "MAIL")

tree.column(1, width = 20)
tree.column(2, width = 80)
tree.column(3, width = 30)
tree.column(4, width = 10)
tree.column(5, width = 50)
tree.column(6, width = 80)
tree.column(7, width = 90)
tree.column(8, width = 90)
tree.column(9,width = 100)

#Base tk
conn = sqlite3.connect("Rep.db")
cur = conn.cursor()
select = cur.execute("select*from INFORMATIONS")
for row in select:
    tree.insert('',END, value = row)

conn.close()
window.mainloop()