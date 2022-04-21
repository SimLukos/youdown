from io import BytesIO
from urllib.request import urlopen # URL paveiksliukui gauti
from tkinter import *
from tkinter.font import BOLD
from pytube import YouTube
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.font import Font


class Langas:

    def __init__(self, langas):
        self.langas = langas

        self.fonas = PhotoImage(file='fonas.png') #ikeliami paveiksliukai
        self.refresh = PhotoImage(file='refresh1.png')
        self.clear = PhotoImage(file='clear1.png')
        self.audio = PhotoImage(file='audio.png')
        self.video = PhotoImage(file='download.png')
        self.search = PhotoImage(file='folder.png')

        #sureguliuojam font
        font1 = Font(family='Iosevka Extended',
                    size=16,
                    weight='bold')

        font2 = Font(family='Iosevka Extended',
                    size=12)

        self.canvas = Canvas(langas, width=800, height=500) #kuriamas canvas
        self.canvas.pack(fill='both', expand=True)

        self.canvas.create_image(0, 0, image=self.fonas, anchor='nw') #koordinates, paveiksliukas, vieta(puse)

        self.canvas.create_text(40, 40, text='URL:', anchor='nw', font=font1) #tekstas
        self.canvas.create_text(40, 130, text='Video information:', anchor='nw', font=font1)
        self.canvas.create_text(40, 420, text='Download to:', anchor='nw', font=font1)

        self.canvas.create_text(40, 160, text='Title:', anchor='nw', font=font2)
        self.title = self.canvas.create_text(100, 160, text='', anchor='nw', font=font2)

        self.canvas.create_text(40, 190, text='Views:', anchor='nw', font=font2)
        self.views = self.canvas.create_text(100, 190, text='', anchor='nw', font=font2)

        self.canvas.create_text(40, 220, text='Author:', anchor='nw', font=font2)
        self.author = self.canvas.create_text(100, 220, text='', anchor='nw', font=font2)


        naujinti_myg = Button(langas, image=self.refresh, command=self.naujinti, borderwidth=0) #kuriami mygtukai
        valyti_myg = Button(langas, image=self.clear, command=self.trinti, borderwidth=0)
        audio_myg = Button(langas, image=self.audio, borderwidth=0)
        video_myg = Button(langas, image=self.video, command=self.video_Parsiuntimas, borderwidth=0)
        search_myg = Button(langas, image=self.search, command=self.katalogas, borderwidth=0)

        self.url_entry = Entry(langas, width=50, bg='white', fg='black', highlightthickness=0) #kuriami entry laukai
        self.directory_entry = Entry(langas, width=42, bg='white', fg='black', highlightthickness=0)

        self.naujinti_myg_canvas = self.canvas.create_window(40, 80, 
                                            anchor='nw', 
                                            window=naujinti_myg) #mygtukas iterpiamas i Canvas
        self.valyti_myg_canvas = self.canvas.create_window(100, 80,
                                            anchor='nw',
                                            window=valyti_myg)
        self.audio_myg_canvas = self.canvas.create_window(610, 415,
                                            anchor='nw',
                                            window=audio_myg)
        self.video_myg_canvas = self.canvas.create_window(670, 415,
                                            anchor='nw',
                                            window=video_myg)
        self.directory_myg_canvas = self.canvas.create_window(550, 415,
                                            anchor='nw',
                                            window=search_myg)

        self.url_entry_canvas = self.canvas.create_window(80, 38,
                                            anchor='nw',
                                            window=self.url_entry) #entry laukas iterpiamas i Canvas
        self.directory_entry_canvas = self.canvas.create_window(145, 420,
                                            anchor='nw',
                                            window=self.directory_entry)
                                            
    def naujinti(self):
        try:
            self.canvas.itemconfig(self.title, text='')
            self.canvas.itemconfig(self.views, text='')
            self.canvas.itemconfig(self.author, text='')

            link = self.url_entry.get()
            video = YouTube(link)
            self.pavadinimas = video.title
            self.perziuros = video.views
            self.autorius = video.author

            self.canvas.itemconfig(self.title, text=self.pavadinimas) #i canvas laukus ivedame video duomenis
            self.canvas.itemconfig(self.views, text=self.perziuros)
            self.canvas.itemconfig(self.author, text=self.autorius)

            self.video_photo_url = video.thumbnail_url #video paveikslelio url adresas
            self.url_image = urlopen(self.video_photo_url) #url atidarymas
            self.image_data = self.url_image.read() #url nuskaitymas ir priskirimas kintamajam
            self.image = Image.open(BytesIO(self.image_data)) #paveiksliuko atidarymas bitais
            self.image_dydis = self.image.resize((220,160)) #paveiksliuko dydzio korekcija
            self.photo = ImageTk.PhotoImage(self.image_dydis) #paveiksliuko atidarymas
            self.photo_canvas = self.canvas.create_image(40, 250, image=self.photo, anchor='nw') #paveiksliuko ikelimas i canvas langa
        except:
            pass
    
    def trinti(self):
        self.canvas.itemconfig(self.title, text='')
        self.canvas.itemconfig(self.views, text='')
        self.canvas.itemconfig(self.author, text='')
        self.canvas.delete(self.photo_canvas)

    def katalogas(self): #funkcija leidzianti pasirinkti folderi ir ji pavaizduoti entry lauke
        self.vieta = filedialog.askdirectory()
        self.directory_entry.insert(0, str(self.vieta))
    
    def video_Parsiuntimas(self):
        link = self.url_entry.get()
        video = YouTube(link)
        video = video.streams.get_highest_resolution() #gauname didziausios raiskos video
        video.download(self.directory_entry.get()) #pradedame siuntima i nurodyta kataloga

#langas.overrideredirect(True) #Nuimam nuo lango remus
langas = Tk()
app = Langas(langas)
langas.geometry('800x500')
langas.title('YOU--DOWN')
langas.mainloop()