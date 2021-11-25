import tkinter as tk
from tkinter import filedialog
import sf2_loader as sf
import pygame

'''
sf2_loader:
https://pypi.org/project/sf2-loader/
https://github.com/Rainbow-Dreamer/sf2_loader
     print(loader)
     print(loader.file)
     print(loader.sfid_list)


Input box:
https://python-course.eu/tkinter_entry_widgets.php
https://www.tutorialspoint.com/python/tk_entry.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm
'''
    

def get_file_path():
    '''
    Opens the file explorer, and returns the
    file path of the chosen file.
    '''
    root = tk.Tk()    #create the frame
    root.withdraw()   #display the frame
    return filedialog.askopenfilename()   #file path of chosen file

def play_MIDI(midi_path, sound_path):
    print('Loading the soundfont...')
    loader = sf.sf2_loader(sound_path)
    print('Loading the song...')
    loader.play_midi_file(midi_path)
    print('Playing the song')
    
def new_song():
    global currentSong, songs, midi
    try:
        newSongPath = get_file_path()
        master = tk.Tk()
        tk.Label(master, text='Song Name:').grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
        tk.mainloop()
        newSong = e1.get()
        master.destroy()
        songs.append(newSong)
        midi[f'{newSong}'] = f'{newSongPath}'
        currentSong = len(songs) - 1
    except:
        return 'Error'

def new_instrument():
    global currentInstrument, instruments, sounds
    try:
        newSoundPath = get_file_path()
        master = tk.Tk()
        tk.Label(master, text='Instrument Name:').grid(row=0)
        e1 = tk.Entry(master)
        e1.grid(row=0, column=1)
        tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
        tk.mainloop()
        newSound = e1.get()
        master.destroy()
        instruments.append(newSound)
        sounds[f'{newSound}'] = f'{newSoundPath}'
        currentInstrument = len(instruments) - 1
    except:
        return 'Error'


def main_scene():
    global songs, midi, currentSong, instruments, sounds, currentInstrument
    pygame.init()
    surfaceSize = (1440, 910)
    
    clock = pygame.time.Clock()
    
    mainSurface = pygame.display.set_mode(surfaceSize)

    
    #------------Intiialize Variables---------------

    #load the images:
    playButton = pygame.image.load('Play_Button.png')
    playButton = pygame.transform.smoothscale(playButton, (0.1*playButton.get_width(),0.1*playButton.get_height()))
    musicNote = pygame.image.load('Music_Note.png')
    musicNote = pygame.transform.smoothscale(musicNote, (0.25*musicNote.get_width(),0.25*musicNote.get_height()))
    plusButton = pygame.image.load('Plus_Button.png')
    plusButton = pygame.transform.smoothscale(plusButton, (0.1*plusButton.get_width(),0.1*plusButton.get_height()))

    #load the fonts:
    font = pygame.font.SysFont('Arial', 80)
    font2 = pygame.font.SysFont('Arial', 50)

    songs = ['Canon In D (0)']
    instruments = ['Full Grand (0)']
    
    currentSong = 0
    currentInstrument = 0
    

    sounds={
        'Full Grand (0)' : 'Full_Grand.SF2'
        }
    
    midi={
        'Canon In D (0)' : 'Canon_In_D.mid'
        }

    #-----------Main Game Loop--------------
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            if x >= 0 and x <= 49 and y >= 0 and y <= 47:
                play_MIDI(midi[songs[currentSong]], sounds[instruments[currentInstrument]])
            elif x >= 0 and x <= 57 and y >= 53 and y <= 100:
                new_song()
            elif x >= 0 and x <= 54 and y >= 100 and y <= 157:
                new_instrument()
            elif x >= 556 and x <= 897 and y >= 68 and y <= 132:
                if currentSong != len(songs) - 1:
                    currentSong += 1
                else:
                    currentSong = 0
            elif x >= 564 and x <= 881 and y >= 180 and y <= 228:
                if currentInstrument != len(instruments) - 1:
                    currentInstrument += 1
                else:
                    currentInstrument = 0
        
        mainSurface.fill(0)

        #pygame.draw.rect(mainSurface, (255, 0, 0), (100, 100, 200, 100))
     
        #draw the play button: 
        mainSurface.blit(playButton, (0, 0)) 
     
        #draw the add song button:
        mainSurface.blit(musicNote, (0, 50))
     
        #draw the add instrument button:
        mainSurface.blit(plusButton, (0, 100))

     
        #draw the song name:
        text = songs[currentSong]
        renderedText = font.render(text, 0, (200, 200, 200))
        text_rect = renderedText.get_rect(center=((1440/2), (100)))
        mainSurface.blit(renderedText, text_rect)
          
        #draw the instrument name  
        text = instruments[currentInstrument]
        renderedText = font2.render(text, 0, (200, 200, 200))
        text_rect = renderedText.get_rect(center=((1440/2), (200)))
        mainSurface.blit(renderedText, text_rect)
     
        pygame.display.flip()
        
        clock.tick(60)
        
    pygame.quit()

    
    
    
    

