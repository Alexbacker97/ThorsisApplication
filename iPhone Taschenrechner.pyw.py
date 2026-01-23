import customtkinter as ctk
import re
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

fenster = ctk.CTk()
fenster.title("Taschenrechner")
fenster.geometry("322x699")
fenster.config(bg="#000000")
from PIL import Image, ImageTk

# PNG oder ICO laden
icon_path = r"C:\Users\Jonathan\Desktop\Programs VSCode\Python\GUI_endziel_BMI_Rechner\calc_icon.ico"
pil_image = Image.open(icon_path)

# In Tkinter PhotoImage konvertieren
icon_image = ImageTk.PhotoImage(pil_image)

# Icon setzen
fenster.iconphoto(True, icon_image)




Rechner = ctk.CTkFrame(fenster, fg_color="#000000")
Verlauf = ctk.CTkFrame(fenster, fg_color="#000000", bg_color="#000000")

VerlaufListe = []

def VerlaufÖffnen():
    if Verlauf.winfo_ismapped():
        Verlauf.place_forget()
    else:
        Verlauf.place(x=10, y=50)

        for widget in Verlauf.winfo_children():
            widget.destroy()

        for i, eintrag in enumerate(VerlaufListe[-10:]):
            label = ctk.CTkLabel(Verlauf, text=eintrag, fg_color="#000000", text_color="white")
            label.place(x=10, y=10 + i*30)


verlaufB = ctk.CTkButton(
    fenster,
    width=25,   
    height=25,
    text="◴",
    command=VerlaufÖffnen,
    fg_color="#000000",
    bg_color="#000000",      
    hover_color="#000000",       
    text_color="white",                      
)
verlaufB.place(x=10, y=10)





def button_click(zeichen):
    global Ausdruck

    if zeichen == "=":
        try:
            temp = Ausdruck.replace("x", "*").replace("÷", "/")
            ergebnis = eval(temp)
            Ausdruck = str(ergebnis)
            VerlaufListe.append(Ausdruck)
        except:
            Ausdruck = "Error"
    else:
        Ausdruck = Ausdruck + zeichen

    Ausgabe.configure(text=Ausdruck)
    

def berechnen():
    global Ausdruck
    try:
        temp = Ausdruck.replace("x","*").replace("÷","/")
        ergebnis = str(eval(temp))
        Ausdruck = ergebnis
        Ausgabe.configure(text=Ausdruck)
    except:
        Ausdruck = ""
        Ausgabe.configure(text="Error")

def delete():
    global Ausdruck
    Ausdruck = Ausdruck[:-1]
    Ausgabe.configure(text=Ausdruck)


def switch_sign():
    global Ausdruck
    if Ausdruck:
        match = re.search(r'(\d+\.?\d*)$', Ausdruck)
        if match:
            num = match.group(1)
            start = match.start(1)

            if num.startswith('-'):
                num = num[1:]
            else:
                num = '-' + num
            Ausdruck = Ausdruck[:start] + num
            Ausgabe.configure(text=Ausdruck)

def percent():
    global Ausdruck
    match = re.search(r'(\d+\.?\d*)$', Ausdruck)
    if match:
        num = match.group(1)
        start = match.start(1)
        num = str(float(num)/100)
        Ausdruck = Ausdruck[:start] + num
        Ausgabe.configure(text=Ausdruck)





size = 40  
B1 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="±",
    command=switch_sign,
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B1.place(x=10, y=620)

B2 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="0",
    command=lambda: button_click("0"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B2.place(x=88, y=620)

B3 = ctk.CTkButton(
    fenster,
    width=55,
    height=size,
    text=".",
    command=lambda: button_click("."),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B3.place(x=166, y=620)

B4 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="=",
    command=lambda: (button_click("="), berechnen()),
    fg_color="#FF9500",
    bg_color="#000000",
    hover_color="#FF9500",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B4.place(x=244, y=620)

B5 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="1",
    command=lambda: button_click("1"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B5.place(x=10, y=570)

B6 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="2",
    command=lambda: button_click("2"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B6.place(x=88, y=570)

B7 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="3",
    command=lambda: button_click("3"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B7.place(x=166, y=570)

B8 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="+",
    command=lambda: button_click("+"),
    fg_color="#FF9500",
    bg_color="#000000",
    hover_color="#FF9500",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B8.place(x=244, y=570)

B9 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="4",
    command=lambda: button_click("4"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B9.place(x=10, y=520)

B10 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="5",
    command=lambda: button_click("5"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B10.place(x=88, y=520)

B11 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="6",
    command=lambda: button_click("6"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B11.place(x=166, y=520)

B12 = ctk.CTkButton(
    fenster,
    width=55,
    height=size,
    text="-",
    command=lambda: button_click("-"),
    fg_color="#FF9500",
    bg_color="#000000",
    hover_color="#FF9500",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B12.place(x=244, y=520)

B13 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="7",
    command=lambda: button_click("7"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B13.place(x=10, y=470)

B14 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="8",
    command=lambda: button_click("8"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B14.place(x=88, y=470)

B15 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="9",
    command=lambda: button_click("9"),
    fg_color="#505050",
    bg_color="#000000",
    hover_color="#636363",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B15.place(x=166, y=470)

B16 = ctk.CTkButton(
    fenster,
    width=53,
    height=size,
    text="x",
    command=lambda: button_click("x"),
    fg_color="#FF9500",
    bg_color="#000000",
    hover_color="#FF9500",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B16.place(x=244, y=470)

B17 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="⌫",
    command=delete,
    fg_color="#979797",
    bg_color="#000000",
    hover_color="#979797",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B17.place(x=10, y=420)

def clear():
    global Ausdruck
    Ausdruck = ""
    Ausgabe.configure(text="")

B18 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="C",
    fg_color="#979797",
    bg_color="#000000",
    hover_color="#979797",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2,
    command=lambda: clear()
)
B18.place(x=88, y=420)

B19 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="%",
    command=percent,
    fg_color="#979797",
    bg_color="#000000",
    hover_color="#979797",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B19.place(x=166, y=420)

B20 = ctk.CTkButton(
    fenster,
    width=size,
    height=size,
    text="÷",
    command=lambda: button_click("÷"),
    fg_color="#FF9500",
    bg_color="#000000",
    hover_color="#FF9500",
    text_color="white",
    font=("Helvetica", 24),
    corner_radius=size // 2
)
B20.place(x=244, y=420)


Ausgabe = ctk.CTkLabel(
    fenster,
    text="",
    width= 302,
    height= 60,
    font= ("Helvetica", 24),
    fg_color="#000000",
    text_color="white",
)
Ausgabe.place(x=10, y=300)

Ausdruck = ""



fenster.mainloop()
