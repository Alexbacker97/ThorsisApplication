import customtkinter as ctk
from PIL import Image
from datetime import datetime

bmi = None

#theme_path = r"C:\Users\Jonathan\Desktop\Programs VSCode\Python\GUI_endziel_BMI_Rechner\my_theme.json"

ctk.set_appearance_mode("Dark")
#ctk.set_default_color_theme("theme_path")

fenster = ctk.CTk()
fenster.title("BMI Rechner")
fenster.geometry("1080x720")
fenster.configure(bg="#4149D1")

StartSeite = ctk.CTkFrame(fenster, fg_color="#4149D1")
StartSeite.pack(fill="both", expand=True)

Rechner = ctk.CTkFrame(fenster, fg_color="#A3B1FF")

Verlauf = ctk.CTkFrame(fenster, fg_color="#37417A")

def BMIBx2():
    BMIBerechnen()
    VerlaufSpeichern()


def ButtonClick():
    StartSeite.pack_forget()
    Rechner.pack(fill="both", expand=True)    

def BMIBerechnen():
    global bmi
    
    if EntryGewicht.get() == "" or EntryGröße.get() == "":
        LabelError.configure(text="Das Feld darf nicht leer sein!")
        return
    
    try:
        wert2 = float(EntryGewicht.get())
        wert1 = float(EntryGröße.get())
    except ValueError:
        LabelError.configure(text="Gib eine Zahl ein!")
        return
    
    bmi = wert2 / wert1 ** 2
    LabelError.configure(text=f"Dein BMI beträgt: {bmi:.2f}")

    grafik_path = r"C:\Users\Jonathan\Desktop\Programs VSCode\Python\GUI_endziel_BMI_Rechner\BMIGrafik.png"
    pil_image = Image.open(grafik_path)     

    ctk_image = ctk.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=(500, 400)
        )
    
    image_label = ctk.CTkLabel(
    Rechner,
    image=ctk_image,
    text=""
)
    image_label.place(x=500, y=200)



def VerlaufÖffnen():
    if bmi is None:
        return
    Rechner.pack_forget()
    Verlauf.pack(fill="both", expand=True)


def VerlaufSchließen():
    Verlauf.pack_forget()
    Rechner.pack(fill="both", expand=True)

BMI_VERLAUF = []

def VerlaufSpeichern():
    BMI_VERLAUF.append((datum, round(bmi, 2)))

    LabelVerlaufBMI = ctk.CTkLabel(
        Verlauf,
        text=f"BMI: {bmi:.2f}",
        text_color="#A3B1FF",
        font=("Helvetica", 14, "bold"),
        pady=20
    )
    LabelVerlaufBMI.pack(padx=25, pady=10)

    LabelVerlaufDatum = ctk.CTkLabel(
        Verlauf,
        text=f"↑ Datum: {datum}",
        text_color="#A3B1FF",
        font=("Helvetica", 14, "bold"),
        pady=20
    )
    LabelVerlaufDatum.pack(padx=25, pady=10)


datum = datetime.now().strftime("%d.%m.%Y")
print(datum)


image_path = r"C:\Users\Jonathan\Desktop\Programs VSCode\Python\GUI_endziel_BMI_Rechner\startseite.png"
pil_image = Image.open(image_path)

ctk_image = ctk.CTkImage(
    light_image=pil_image,
    dark_image=pil_image,
    size=(1080, 620),
    
)

LabelError = ctk.CTkLabel(
    Rechner,
    text="",
    text_color="#1D237E",
    pady=10,
    font=("Helvetica", 14, "bold")
)
LabelError.place(x=30, y=490)

image_label = ctk.CTkLabel(
    StartSeite,
    image=ctk_image,
    text=""
)
image_label.place(x=0, y=0)


StartenB = ctk.CTkButton(
    StartSeite,
    text="Starte den BMI-Rechner",
    width= 120,
    height= 40,
    fg_color="#A3B1FF",
    text_color="#1D237E",
    hover_color="#606791",
    command= ButtonClick,
    corner_radius=20,
    font=("Helvetica", 14, "bold")
)
StartenB.pack(side="bottom", pady=20)
StartenB.lift()

Label1 = ctk.CTkLabel(
    Rechner,
    text="Berechne deinen BMI.",
    text_color="#1D237E",
    pady=10,
    justify="left",
    font=("Helvetica", 24, "bold")
)

Label1.place(x=10, y=10)

Label2 = ctk.CTkLabel(
    Rechner,
    text="Der Body Mass Index (BMI) ist eine einfache Maßzahl,\num das Verhältnis von Körpergewicht zu Körpergröße einzuschätzen.",
    text_color="#1D237E",
    pady=10,
    justify="left",
    font=("Helvetica", 14, "bold")
)
Label2.place(x=10, y=60)

Label3 = ctk.CTkLabel(
    Rechner,
    text="Er wird berechnet nach der Formel:",
    text_color="#1D237E",
    pady=10,
    font=("Helveticy", 14, "bold"),
    justify="left"
)
Label3.place(x=10, y=100)

Label4 = ctk.CTkLabel(
    Rechner,
    text="\n\n\n BMI =",
    text_color="#1D237E",
    pady=10,
    font=("Helvetica", 18, "italic")
)
Label4.place(x=10, y=100)

Label5 = ctk.CTkLabel(
    Rechner,
    text="\n(Gewicht in kg) \n ⸻⸻⸻ \n  (Größe in m)²",
    text_color="#1D237E",
    pady=10,
    font=("Helvetica", 14, "italic")
)
Label5.place(x=70, y=136)

Label6 = ctk.CTkLabel(
    Rechner,
    text="Gib dein Gewicht ein (in kg und . statt ,).",
    text_color="#1D237E",
    pady=10,
    font=("Helvetica", 14, "bold")
)
Label6. place(x=30, y=220)

EntryGewicht = ctk.CTkEntry(
    Rechner,
    width=120,
    height=30,
    fg_color="#4149D1",
    corner_radius=15
)
EntryGewicht.place(x=30, y=260)

Label7 = ctk.CTkLabel(
    Rechner,
    text="Gib dein Größe ein (in m und . statt ,).",
    text_color="#1D237E",
    pady=10,
    font=("Helvetica", 14, "bold")
)
Label7. place(x=30, y=320)

EntryGröße = ctk.CTkEntry(
    Rechner,
    width=120,
    height=30,
    fg_color="#4149D1",
    corner_radius=15
)
EntryGröße.place(x=30, y=360)

BMIB = ctk.CTkButton(
    Rechner,
    text="BMI berechnen",
    width= 120,
    height= 40,
    fg_color="#4149D1",
    text_color="#1D237E",
    hover_color="#606791",
    command= BMIBx2,
    corner_radius=20,
    font=("Helvetica", 14, "bold")
)
BMIB.place(x=30, y=410)

VerlaufB = ctk.CTkButton(
    Rechner,
    text="◴",
    width= 30,
    height= 20,
    fg_color="#A3B1FF",
    text_color="#1D237E",
    hover_color="#A3B1FF",
    command= VerlaufÖffnen,
    font=("Helvetica", 24, "bold")
)
VerlaufB.place(x=1000, y=30)

VerlaufSch = ctk.CTkButton(
    Verlauf,
    text="🗙",
    width= 30,
    height= 30,
    fg_color="#37417A",
    text_color="#A3B1FF",
    hover_color="#37417A",
    command= VerlaufSchließen,
    font=("Arial", 20, "bold")
    )
VerlaufSch.place(x=1000, y=30)

Label1Verlauf = ctk.CTkLabel(
    Verlauf,
    text="Dein Verlauf:",
    fg_color="#37417A",
    text_color="#A3B1FF",
    font=("Helvetica", 24, "bold")
)
Label1Verlauf.place(x=50, y=50)
fenster.mainloop()