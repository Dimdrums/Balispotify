import tkinter as tk
from PIL import Image, ImageTk
import os
import json

import requests
import re
import html

################ DATA ###############

appdata_dir = os.getenv('APPDATA')    #les données sont sauvegardées dans le appdata
data_path = os.path.join(appdata_dir, 'BaliSpotify', 'data.json')

with open(data_path, 'r') as f:
        data = json.load(f)

lienSpotify = data["lien"]
Bluetooth_init = data["Bluetooth"]

#####################################

class FloatingTooltip:
    def __init__(self, widget, delay=300):
        self.widget = widget
        self.tooltip = None
        self.delay = delay
        self.after_id = None

        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.hide_tooltip)
        self.widget.bind("<Motion>", self.move_tooltip)

    def schedule_show(self, event=None):
        self.after_id = self.widget.after(self.delay, lambda: self.show_tooltip(event))

    def show_tooltip(self, event=None):
        if self.tooltip or not self.widget.get():
            return

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.attributes("-topmost", True)

        label = tk.Label(
            self.tooltip,
            text=self.widget.get(),
            font=(Police,10),fg=couleur3,bg=couleur1,
            relief="solid",
            borderwidth=1,
        )
        label.pack()

        self.move_tooltip(event)

    def move_tooltip(self, event):
        if self.tooltip:
            x = event.x_root + 15
            y = event.y_root + 10
            self.tooltip.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

def get_playlist_name(url):
    headers = {
        "User-Agent": "Mozilla/5.0", #C'est juste le nom du header, c'est indépendant des navigateurs installés
        "Range": "bytes=0-4096"
    }

    r = requests.get(url, headers=headers)
    text = r.text

    start = text.find("<title>")
    end = text.find("</title>")

    if start != -1 and end != -1:
        title = text[start+7:end]
        return html.unescape(title.split(" - ")[0])

    return None

def toggle(toggle_button):
    
    with open(data_path, 'r') as f:
        data = json.load(f)

    if toggle_button.config('relief')[-1] == 'sunken':
        toggle_button.config(relief='raised',background=couleur1)
        texte="                                                                                                                                                                            "
        new_state=0
    else:
        toggle_button.config(relief='sunken',background=couleur2)
        texte="*Si votre enceinte est pairé avec votre ordinateur, elle se connectera automatiquement."
        new_state=1

    disclaimer = tk.Label(bottom_band, text=texte,font=(Police,8,"bold"),fg=couleur1,bg=couleur4, anchor="e") 
    disclaimer.grid(row=0, column=0, padx=10, pady=10, sticky="e")  

    data["Bluetooth"] = new_state
        
    with open(data_path, 'w') as f:
        json.dump(data, f, indent=4)

###################################

def page2 (lien):#mode,nom,mail,pathExosL,pathCours):

    with open(data_path, 'r') as f:
        data = json.load(f)
    
    nom_playlist = data["nom_playlist"]

    Valider=tk.Button(grille,text="Valider",font=(Police,12),fg=couleur2,bg=couleur1,command = lambda : Verif(EntreeLien))
    
    Label=tk.Label(grille,text="Configuration",font=(Police,12),fg=couleur3,bg=couleur1)

    espace1=tk.Label(grille,text="                      ",font=(Police,12),fg=couleur2,bg=couleur1)
    espace2=tk.Label(grille,text="                              ",font=(Police,12),fg=couleur2,bg=couleur1)
    espace3=tk.Label(grille,text="                                                         ",font=(Police,8),fg=couleur2,bg=couleur1)

    if nom_playlist == "clic droit > Partager > Copier le lien...":
        texte = nom_playlist
        color = couleur2
    else:
        texte = f"'{nom_playlist}'"
        color = couleur3

    Label1=tk.Label(grille,text="Lien de la playlist :",font=(Police,12),fg=couleur2,bg=couleur1)
    Label2=tk.Label(grille,text="Bluetooth automatique* :",font=(Police,12),fg=couleur2,bg=couleur1)
    Label3=tk.Label(grille,text=texte,font=(Police,8),fg=color,bg=couleur1)
    EntreeLien=tk.Entry(grille,width=30)
    EntreeLien.insert(0,lien)
    FloatingTooltip(EntreeLien)
    
    Bluetooth=tk.Button(grille,image=imageBluetooth,fg=couleur2,bg=couleur1, command = lambda : toggle(Bluetooth), width=30, height=30)

    
    Label.grid(row=0,column=0, columnspan=20,pady=50)

    Label1.grid(row=1,column=2,padx=10,pady=5, sticky="e")
    EntreeLien.grid(row=1,column=4,padx=10,pady=5, sticky="w")
    Label3.grid(row=1, column=6, padx=10, pady=5)

    espace2.grid(row=2, column=2, padx=10, pady=5, sticky="w")
    espace1.grid(row=2, column=6, padx=10, pady=5, sticky="w")

    Label2.grid(row=3,column=2,padx=10,pady=10, sticky="e")
    Bluetooth.grid(row=3, column=4, padx=10, pady=5, sticky="w")
    espace3.grid(row=3, column=6, padx=10, pady=5, sticky="w")
    
    Valider.grid(row=100,column=6,padx=10,pady=20)
    interface.bind('<Return>', lambda event: Valider.invoke())

    if Bluetooth_init:
        toggle(Bluetooth)


def Verif (entry):

    Label1=tk.Label(grille,text="🛜",font=(Police,12),fg=couleur2,bg=couleur1)
    Label1.grid(row=100,column=4,pady=20, sticky="e")
    interface.update()

    lien_entre = entry.get()
    try:
        key = lien_entre.split("playlist/")[1].split("?")[0] #peut échouer

        if len(key) != 22 or "open.spotify.com" not in lien_entre:
            texte="Le lien renseigné n'est pas valide"

        else:
            texte="                                                       "

            try :
                nom_playlist=get_playlist_name(lien_entre) #peut échouer

                if nom_playlist=="Spotify" or nom_playlist=="Page not available":
                    nom_playlist="OK 👍"
                else:
                    nom_playlist=f"'{nom_playlist}'"

                Label3=tk.Label(grille,text="                                                         ",font=(Police,8),fg=couleur3,bg=couleur1)
                Label3.grid(row=1, column=6, padx=10, pady=5, sticky="w")
                interface.update()
                Label3=tk.Label(grille,text=nom_playlist,font=(Police,8),fg=couleur3,bg=couleur1)
                Label3.grid(row=1, column=6, padx=10, pady=5)

                with open(data_path, 'r') as f:
                    data = json.load(f)

                data["lien"] = lien_entre
                data["key"] = key
                data["nom_playlist"] = nom_playlist
                    
                with open(data_path, 'w') as f:
                    json.dump(data, f, indent=4) 
            except:
                texte="Le lien renseigné n'est pas valide"
    except:
        texte="Le lien renseigné n'est pas valide"

       

    ErrorLabel=tk.Label(grille,text=texte,font=(Police,8),fg=couleur5,bg=couleur1)
    ErrorLabel.grid(row=2,column=4,padx=6,pady=5, sticky="e")

    Label1=tk.Label(grille,text="     ",font=(Police,12),fg=couleur2,bg=couleur1)
    Label1.grid(row=100,column=4,pady=20, sticky="e")
    interface.update()


###########################################################
couleur1="#E5F9F1"
couleur2="#009465"
couleur3="#30bf7c"
couleur4="#133127"
couleur5="#933535"
Police="Open Sans"



interface=tk.Tk()
interface.title("BaliSpotify")
# interface.configure(bg=couleur1)

# icon=tk.PhotoImage(file="webex+.png")
# interface.iconphoto(True,icon)
imageBluetooth=ImageTk.PhotoImage(Image.open("bt_logo.png").resize((25, 25)))




largeur_ecran = interface.winfo_screenwidth()
hauteur_ecran = interface.winfo_screenheight()


l = 600
h = 400

x = (largeur_ecran-l)//2
y = (hauteur_ecran-h)//2


interface.geometry(f'{l}x{h}+{x}+{y-100}')


frame_special = tk.Frame(interface, width=2*l, height=2*h,bg=couleur1)
frame_special.place(relx=0.5, rely=0.5, anchor="center") 

grille = tk.Frame(interface,bg=couleur1)
grille.place(relx=0.5, rely=0.5, anchor="center")  


top_band = tk.Frame(interface, bg=couleur4, relief="raised", height=80)
top_band.grid(row=0, column=0, sticky="nsew")

bottom_band = tk.Frame(interface, bg=couleur4, relief="raised", height=20)
bottom_band.grid(row=2, column=0, sticky="nsew")

espace = tk.Label(top_band, text="    ",bg=couleur4)
espace.grid(row=0, column=0, padx=10, pady=3)  
webex = tk.Label(top_band, text="BaliSpotify",font=(Police,25,"bold"),fg=couleur1,bg=couleur4)  #titre
webex.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')  

disclaimer = tk.Label(bottom_band, text="     ",font=(Police,8,"bold"),fg=couleur1,bg=couleur4, anchor="e") 
disclaimer.grid(row=0, column=0, padx=10, pady=10, sticky="e")  


bottom_band.grid_columnconfigure(0, weight=1)
interface.grid_columnconfigure(0, weight=1)
interface.grid_rowconfigure(1, weight=1)  

page2(lienSpotify)

interface.mainloop()