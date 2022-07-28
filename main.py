import tkinter as tk
from tkinter.colorchooser import askcolor
import playsound
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from pytube import YouTube
from pytube import Playlist
from playsound import playsound
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
import os
from tkinter import messagebox
import shutil


def callback():
    if row >= 1:
        if messagebox.askokcancel("Beenden", "Möchtest du es wirklich beenden ? "):
            shutil.rmtree("./TempImages")
            root.destroy()
    else: 
        if messagebox.askokcancel("Beenden", "Möchtest du es wirklich beenden ? "):
            root.destroy()

def Notification():
    window = Toplevel()
    window.title("Fertig")
    window.resizable(width=False, height=False)
    Label(window, text="Fertig",font="Arial 32",background="Green").pack(side="top")
    os.chdir("..")
    playsound(".assets/Sound.mp3")





def browseFiles():
    global filename
    filename = filedialog.askdirectory(initialdir="/")
    Label(root, text=filename,).place(x=790, y=453)



def Yt_Playlist():
    parent_dir = "./"
    directory = "TempImages"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    plurl = entry2.get()
    p = Playlist(plurl)
    size = 150,150
    vids = p.video_urls
    finalurls = vids.__str__().split(", ")
    os.chdir("./TempImages")
    for x in finalurls:
        video = YouTube(x)
        print(x)
        u = urlopen(video.thumbnail_url)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        im.thumbnail(size=size)
        im.save(video.video_id + ".jpg")
        ima = Image.open(video.video_id + ".jpg")
        image = ImageTk.PhotoImage(ima,size=size)
        Label3 = Label(scrollable_frame,image=image,borderwidth=0)
        Label3.grid()
        Label3.photo = image
        Label4 = Label(scrollable_frame,text=video.title, foreground="white",background="gray5", font="Arial 9 bold", wraplength=200)
        Label4.grid(column=1, row=row)
        variable()
    if audio1var.get() == 0:
        for video in p.videos:
            video.streams.get_highest_resolution().download(filename)

        Notification()




    if audio1var.get() == 1:
        for video in p.videos:
            video.streams.filter(resolution="720p")
            heruntergeladen = video.streams.get_audio_only().download(filename)
            base, ext = os.path.splitext(heruntergeladen)
            new_file = base + '.mp3'
            os.rename(heruntergeladen, new_file)
        Notification()
row = 0


def variable():
    global row
    row += 1

def Yt_video():
    parent_dir = "./"
    directory = "TempImages"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    url = entry1.get()
    video = YouTube(url)
    size = 150,150
    u = urlopen(video.thumbnail_url)
    raw_data = u.read()
    u.close()
    im = Image.open(BytesIO(raw_data))
    im.thumbnail(size=size)
    os.chdir("./TempImages")
    im.save(video.video_id + ".jpg")
    ima = Image.open(video.video_id + ".jpg")
    image = ImageTk.PhotoImage(ima, size=size)
    Label3 = Label(scrollable_frame, image=image, borderwidth=0)
    Label3.grid()
    Label3.photo = image
    Label4 = Label(scrollable_frame,text=video.title, foreground="white",background="gray5", font="Arial 9 bold", wraplength=200)
    Label4.grid(column=1, row=row)
    variable()
    if audio1var.get() == 0:
        video.streams.get_highest_resolution().download(filename)

        Notification()




    if audio1var.get() == 1:
        heruntergeladen = video.streams.get_audio_only().download(filename)
        base, ext = os.path.splitext(heruntergeladen)
        new_file = base + '.mp3'
        os.rename(heruntergeladen, new_file)

        Notification()



root = tk.Tk()
root.title("Youtube Downloader and Converter")
root.geometry("1280x720")
root.resizable(width=False, height=False)
photo = tk.PhotoImage(file=".assets/python.png")

image_label = tk.Label(root, image=photo )
image_label.place(x=0,y=0,width=1280,height=720)

entry1 = Entry(root, width=70)
entry1.place(x=600, y=300, anchor="sw")

entry2 = Entry(root, width=70)
entry2.place(x=600, y=200, anchor="sw")

audio1 = tk.Checkbutton(root, text='nur Audio')
audio1var = tk.BooleanVar()
audio1["variable"] = audio1var
audio1.place(x=830 , y=350)

button1 = Button(root, text= "Download Einzeln" , command=Yt_video)
button1.place(x=715 , y=350)

button2 = Button(root, text= "Ziel" , command=browseFiles)
button2.place(x=920 , y=350)

button3 = Button(root, text= "Download Playlist" , command=Yt_Playlist)
button3.place(x=600 , y=350)


Label1 = Label(root, text="Playlist : ", font="arial 15")
Label1.place(x=500, y=200, anchor="sw")

Label2 = Label(root, text="Einzeln : ", font="arial 15")
Label2.place(x=500, y=300, anchor="sw")


container = ttk.Frame(root,borderwidth=0)
canvas = Canvas(container, background="gray5", borderwidth=0)

scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas, background="gray5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

container.place(x=50, y=50, width=400, height=600)
canvas.pack(side="left", fill="both",expand=True)
scrollbar.pack(side="right", fill="y")

row = 0

root.protocol("WM_DELETE_WINDOW", callback)

root.mainloop()