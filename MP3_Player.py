from tkinter import *
import pygame
from tkinter import filedialog
from PIL import ImageTk, Image
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
# import cv2

global n

n=0

#file
f=open("songs.txt","r")
s=f.read().split('\n')
length=len(s)
f.close()
#file

#Creating a dialog box and adding song to playlist
def add_song(no):
    global n
    n=no
    song=filedialog.askopenfilename(initialdir='\songs',title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    psong=list(playlist.get(0,playlist.size()))
    for s in range(len(psong)):
        psong[s]=psong[s]
        song=song.split('/')
        song = song[len(song)-1]
        song = song.replace(".mp3","")
        if song in psong:
            continue
        if song!='':
            #print(song)
            n+=1
            playlist.insert(END,song)
    song = song.replace(".mp3","")
    n=n+1
    playlist.insert(END,song)
    
 #Adding many songs at a same time   
def add_many_song(no):

    songs=filedialog.askopenfilenames(title="Choose A Song", filetypes=(("mp3 Files","*.mp3"),))
    global n
    n=no
  
    psong=list(playlist.get(0,playlist.size()))
    for s in range(len(psong)):
        psong[s]=psong[s]
    print(psong)
    for song in songs:
        song=song.split('/')
        song = song[len(song)-1]
        song = song.replace(".mp3","")
        if song in psong:
            continue
        if song!='':
            #print(song)
            n+=1
            playlist.insert(END,song)

global temp
temp = False

#Play song function
def Play():
    global stopped
    stopped=False
    global temp
    temp = False
    song=playlist.get(ACTIVE)
    song = song + ".mp3"

    #Update the to slide position
    slider.config(value=0)
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # Calls the play_time function at time of playing
    play_time()
    
    
global stopped
stopped = False

#Stop song function
def Stop():
    
    global stopped
    stopped=True
    #Reset Slider
    status_bar.config(text='')
    slider_lable.config(text='')
    slider.config(value=0)
    
    pygame.mixer.music.stop()
    playlist.selection_clear(ACTIVE)
    
    #Clear Status bar
    status_bar.config(text='')
    stopped=True
    
global paused
paused=False

#Pausing the song
def Pause(is_paused):
    global paused
    paused=is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused=False
    else:
        pygame.mixer.music.pause()
        paused=True

#Play the next song in the playlist
def next_song():
    #Update the to slide position
    slider.config(value=0)
    #Get the current song tuple no
    next_one=playlist.curselection()
    #Add one to the current song no
    next_one=(next_one[0] + 1)%n
    #Grab song title from playlist
    song = playlist.get(next_one)
    #add directory structure and .mp3 to song title
    song=song + ".mp3"
    #playing the next song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist 
    playlist.selection_clear(0,END)
    #Move the active bar to next song
    playlist.activate(next_one)
    #Set active bar to next song
    playlist.selection_set(next_one)  
    global stopped
    stopped=False

    

    
#Play the previous song in the playlist
def previous_song():
    #Update the to slide position
    slider.config(value=0)
    #Get the current song tuple no
    previous_one=playlist.curselection()
    #Substract one to the current song no
    previous_one=(previous_one[0] - 1)%n
    #Grab song title from playlist
    song = playlist.get(previous_one)
    #add directory structure and .mp3 to song title
    song= song + ".mp3"
    #playing the previous song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist 
    playlist.selection_clear(0,END)
    #Move the active bar to previous song
    playlist.activate(previous_one)
    #Set active bar to previous song
    playlist.selection_set(previous_one)
    global stopped
    stopped=False

    

#Delete the selected song
def delete_song(no):
    Stop()
    global n
    n=no
    playlist.delete(ANCHOR)
    n=n-1
    #Stop music if its playing
    pygame.mixer.music.stop()
    
#Delete all the selected songs
def delete_all_song(no):
    Stop()
    global n
    n=0
    playlist.delete(0,END)
    #Stop music if its playing
    pygame.mixer.music.stop()


#Get the song length info
def play_time():
    if stopped:
        return
    #Grab the current song elapsed times
    global temp
    current_time=round(pygame.mixer.music.get_pos()/1000)
    
    if temp:
        current_time = round(slider.get())
    

    
    #Converting to time format
    converted_current_time=time.strftime('%M:%S',time.gmtime(int(current_time)))
    
    #Get the current song
    
    song = playlist.get(ACTIVE)
    #add directory structure and .mp3 to song title
    song= song + ".mp3"
    
    #Load the song with mutagen
    song_mut = MP3(song) 
    
    #Get the length of current song with mutagen
    global song_length
    song_length=song_mut.info.length
    
    #Converting to time format
    global converted_song_length
    converted_song_length=time.strftime('%M:%S',time.gmtime(int(song_length)))
      
    
    if int(slider.get())==int(song_length):
        # status_bar.config(text=f'Time Elapsed :  {converted_song_length} of  {converted_song_length}   ')
        slider_lable.config(text=" " + str(converted_song_length) +  "\t\t\t\t\t\t        " +  str(converted_song_length))
        next_song()
        
    elif paused :
        #If paused do nothing
        pass
    elif int((slider.get()))==int(current_time):
        
        #Slider hasnt moved

        slider_position=int(song_length)
        slider.config(to=slider_position,value=int(current_time))
        
        #Converting to time format
        converted_current_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))
        

        # Update slider value to current song position
        slider_lable.config(text=" " + str(converted_current_time) +  "\t\t\t\t\t\t        " +  str(converted_song_length))

        
        #Update slider value to next value
        next_time = slider.get() + 1
        slider.config(value=next_time)
        
    else:
        #Slider has been moved

        slider_position=song_length
        slider.config(to=slider_position,value=round(slider.get()))
        
        temp=True
        
        #Converting to time format
        converted_current_time=time.strftime('%M:%S',time.gmtime(int(slider.get())))


        # Update slider value to current song position
        slider_lable.config(text=" " + str(converted_current_time) +  "\t\t\t\t\t\t        " +  str(converted_song_length))
        
        
        #Update slider value to next value
        next_time = slider.get() + 1
        slider.config(value=next_time)
    
    
    #Update time after every sec
    status_bar.after(1000,play_time)

def slide(x):
    song=playlist.get(ACTIVE)
    song = song + ".mp3"
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0,start=round(slider.get()))

#Main interface
root = Tk() 
root.title('MP3 Player')
root.geometry("500x500")

#Initializing pygame.mixer
pygame.mixer.init()


#Frame containing playlist and scrollbar
playlist_frame=Frame(root)
playlist_frame.pack(pady=10,ipady=10,ipadx=10)

#Scrollbar
sb=Scrollbar(playlist_frame,width=12)
sb.pack(side=RIGHT,fill=Y)

#playlist
playlist = Listbox(playlist_frame,bg="black",fg="white",width=60,selectbackground="lightgreen",selectforeground="black",yscrollcommand=sb.set)
playlist.pack(pady=20)

#Loading images for buttons
back_btn_img = ImageTk.PhotoImage((Image.open("backward2.jpg")).resize((50,50),Image.ANTIALIAS))
forward_btn_img = ImageTk.PhotoImage((Image.open("forward2.png")).resize((50,50),Image.ANTIALIAS))
play_btn_img = ImageTk.PhotoImage((Image.open("play2.png")).resize((50,50),Image.ANTIALIAS))
pause_btn_img = ImageTk.PhotoImage((Image.open("pause2.png")).resize((50,50),Image.ANTIALIAS))
stop_btn_img= ImageTk.PhotoImage((Image.open("stop2.png")).resize((50,50),Image.ANTIALIAS)) 


#Main frame
controls_frame=Frame(root)
controls_frame.pack()

#Buttons
back_button=Button(controls_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_button=Button(controls_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_button=Button(controls_frame,image=play_btn_img,borderwidth=0,command=Play)
pause_button=Button(controls_frame,image=pause_btn_img,borderwidth=0,command=lambda: Pause(paused))
stop_button=Button(controls_frame,image=stop_btn_img,borderwidth=0,command=Stop)

#Arranging Buttons
back_button.grid(row=0,column=0,padx=10,pady=25)
forward_button.grid(row=0,column=1,padx=10,pady=25)
play_button.grid(row=0,column=2,padx=10,pady=25)
pause_button.grid(row=0,column=3,padx=10,pady=25)
stop_button.grid(row=0,column=4,padx=10,pady=25)

#songs add
for i in range(len(s)):
    playlist.insert(END,s[i]) 
 #songs add

n=n+len(s)

#Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Adding options
add_song_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add one song to playlist",command=lambda: add_song(n))
add_song_menu.add_command(label="Add multiple song to playlist",command=lambda: add_many_song(n))

#Deleting options
delete_song_menu = Menu(my_menu,tearoff=False)
my_menu.add_cascade(label="Delete Songs", menu=delete_song_menu)
delete_song_menu.add_command(label="Delete a song from playlist",command=lambda: delete_song(n))
delete_song_menu.add_command(label="Delete all songs from playlist",command=lambda: delete_all_song(n))

# #Status bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
# status_bar.pack(fill=X, side =BOTTOM,ipady=2)

#Slider
slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,command=slide,length=340)
slider.pack(pady=20)

#Slider label
slider_lable=Label(root,text='')
slider_lable.pack(anchor="w",padx=80)

root.mainloop()

