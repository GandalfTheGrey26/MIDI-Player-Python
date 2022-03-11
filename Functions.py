import tkinter as tk
from tkinter import filedialog
import sf2_loader as sf
import pygame, time
from mido import MidiFile

'''
sf2_loader:
https://pypi.org/project/sf2-loader/
https://github.com/Rainbow-Dreamer/sf2_loader
     print(loader)
     print(loader.file)
     print(loader.sfid_list)

filedialog:
https://docs.python.org/3/library/dialog.html
https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/

Input box:
https://python-course.eu/tkinter_entry_widgets.php
https://www.tutorialspoint.com/python/tk_entry.htm
https://www.tutorialspoint.com/python/python_gui_programming.htm

Midi Progam:
https://www.noterepeat.com/articles/how-to/213-midi-basics-common-terms-explained#H
'''

#dict_name = {'key' : 'value'}
#x = dictionary.keys()
#x = dictionary.values()

auto_name = True

def get_file_paths(file_type):
    root = tk.Tk()
    root.withdraw()
    if file_type == 'MIDI':
        return filedialog.askopenfilenames(title='Add Songs', filetypes=[("MIDI Sequence", '.mid')])
    elif file_type == 'Soundfont':
        return filedialog.askopenfilenames(title='Add Instruments', filetypes=[("Sound Font", ".sf2")])   #file path of chosen file
    
def getName(file_path):
    slash = 0
    path = (file_path.split('/'))[-1]
    path = path.split('.')[0]
    return path

def play_MIDI(midi_path, sound_path, mainSurface, null):
    font3 = pygame.font.SysFont('Arial', 35)
    print('Loading the soundfont...')
    loader = sf.sf2_loader(sound_path)
    print('Loading the song...')
    if not null:
        text = 'Loading...'
        renderedText = font3.render(text, 0, (255, 255, 255))
        text_rect = renderedText.get_rect(center=(720, 780)) 
        mainSurface.blit(renderedText, text_rect)
        pygame.display.flip()
    loader.play_midi_file(midi_path)
    print('Playing the song')
    
def new_songs():
    global currentSong, songs, midi, duration
    try:
        newSongPaths = get_file_paths('MIDI')
        for i in range(0, len(newSongPaths)):
            if not auto_name:
                master = tk.Tk()
                tk.Label(master, text=f'{newSongPaths[i]}/Song Name:').grid(row=0)
                e1 = tk.Entry(master)
                e1.grid(row=0, column=1)
                tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
                tk.Button(master, text='Skip', command=master.quit).grid(row=0, column=3, sticky=tk.W, pady=4)
                tk.mainloop()
                newSong = e1.get()
                master.destroy()
            else:
                newSong = getName(str(newSongPaths[i]))
            if newSong != '':
                duration[f'{newSong}'] = round(MidiFile(newSongPaths[i]).length)
                songs.append(newSong)
                midi[f'{newSong}'] = f'{newSongPaths[i]}'
                currentSong = len(songs) - 1
    except:
        return 'Error'
    
def new_instruments():
    global currentInstrument, instruments, sounds
    try:
        newSoundPaths = get_file_paths('Soundfont')
        for i in range(0, len(newSoundPaths)):
            if not auto_name:
                master = tk.Tk()
                tk.Label(master, text=f'{newSoundPaths[i]}/Instrument Name:').grid(row=0)
                e1 = tk.Entry(master)
                e1.grid(row=0, column=1)
                tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
                tk.Button(master, text='Skip', command=master.quit).grid(row=0, column=3, sticky=tk.W, pady=4)
                tk.mainloop()
                newSound = e1.get()
                master.destroy()
            else:
                newSound = getName(str(newSoundPaths[i]))
            if newSound != '':
                instruments.append(newSound)
                sounds[f'{newSound}'] = f'{newSoundPaths[i]}'
                currentInstrument = len(sounds) - 1
    except:
        return 'Error'

def main_scene():
    global songs, midi, currentSong, instruments, sounds, currentInstrument, duration, auto_name
    pygame.init()
    surfaceSize = (1440, 910)
    
    clock = pygame.time.Clock()
    
    mainSurface = pygame.display.set_mode(surfaceSize)
    
    #------------Initialize Variables---------------
    #https://pypi.org/project/sf2-loader/

    #load the images:
    playButton = pygame.image.load('Play_Button.png')
    playButton = pygame.transform.smoothscale(playButton, (0.1*playButton.get_width(),0.1*playButton.get_height()))
    musicNote = pygame.image.load('Music_Note.png')
    musicNote = pygame.transform.smoothscale(musicNote, (0.25*musicNote.get_width(),0.25*musicNote.get_height()))
    plusButton = pygame.image.load('Plus_Button.png')
    plusButton = pygame.transform.smoothscale(plusButton, (0.1*plusButton.get_width(),0.1*plusButton.get_height()))
    pauseButton = pygame.image.load('Pause_Button.png')
    pauseButton = pygame.transform.smoothscale(pauseButton, (0.08*pauseButton.get_width(),0.08*pauseButton.get_height()))
    
    #load the fonts:
    font = pygame.font.SysFont('Arial', 80)
    font2 = pygame.font.SysFont('Arial', 50)
    font3 = pygame.font.SysFont('Arial', 35)
    font4 = pygame.font.SysFont('Arial', 23)

    songs = ['Canon In D', 'Piano Piece #1 (In D Minor)', 'Piece #1 (In C Minor)']
    instruments = ['Full Grand']
    
    currentSong = 0
    currentInstrument = 0

    duration={
        'Canon In D' : round(MidiFile('Canon_In_D.mid').length),
        'Piano Piece #1 (In D Minor)' : round(MidiFile('Piano Piece #1 (In D Minor).mid').length),
        'Piece #1 (In C Minor)' : round(MidiFile('Piece #1 (In C Minor).mid').length)
        }
    
    sounds={
        'Full Grand' : 'Full_Grand.SF2'
        }
    
    midi={
        'Canon In D' : 'Canon_In_D.mid',
        'Piano Piece #1 (In D Minor)' : 'Piano Piece #1 (In D Minor).mid',
        'Piece #1 (In C Minor)' : 'Piece #1 (In C Minor).mid'
        }
    
    playing = False
    startTime = time.time()
    song = currentSong
            
    #-----------Main Game Loop--------------
    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            if x >= 0 and x <= 49 and y >= 0 and y <= 47:
                play_MIDI(midi[songs[currentSong]], sounds[instruments[currentInstrument]], mainSurface, False)
                playing = True
                startTime = time.time()
                song = currentSong
            elif x >= 0 and x <= 57 and y >= 53 and y <= 100:
                new_songs()
            elif x >= 0 and x <= 54 and y >= 100 and y <= 157:
                new_instruments()
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
            elif x >= 6 and x <= 280 and y >= 873 and y <= 900:
                del sounds[instruments[currentInstrument]]
                del instruments[currentInstrument]
                currentInstrument = len(instruments) - 1
            elif x >= 875 and x <= 1060 and y >= 873 and y <= 902:
                del midi[songs[currentSong]]
                del songs[currentSong]
                currentSong = len(songs) - 1
            elif x >= 403 and x <= 708 and y >= 871 and y <= 898:
                master = tk.Tk()
                tk.Label(master, text=f'Rename: {instruments[currentInstrument]}').grid(row=0)
                e1 = tk.Entry(master)
                e1.grid(row=0, column=1)
                tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
                tk.Button(master, text='Cancel', command=master.quit).grid(row=0, column=3, sticky=tk.W, pady=4)
                tk.mainloop()
                newSound = e1.get()
                master.destroy()
                if newSound != '':
                    instruments.append(newSound)
                    sounds[f'{newSound}'] = f'{sounds[instruments[currentInstrument]]}'
                    del sounds[instruments[currentInstrument]]
                    del instruments[currentInstrument]
                    currentInstrument = len(instruments) - 1
            elif x >= 1206 and x <= 1426 and y >= 873 and y <= 902:
                master = tk.Tk()
                tk.Label(master, text=f'Rename: {songs[currentSong]}').grid(row=0)
                e1 = tk.Entry(master)
                e1.grid(row=0, column=1)
                tk.Button(master, text='Enter', command=master.quit).grid(row=0, column=2, sticky=tk.W, pady=4)
                tk.Button(master, text='Cancel', command=master.quit).grid(row=0, column=3, sticky=tk.W, pady=4)
                tk.mainloop()
                newSong = e1.get()
                master.destroy()
                if newSong != '':
                    songs.append(newSong)
                    midi[f'{newSong}'] = f'{midi[songs[currentSong]]}'
                    del midi[songs[currentSong]]
                    del songs[currentSong]
                    currentSong = len(songs)- 1
            elif x >= 54 and x <= 105 and y >= 2 and y <= 49:
                startTime = 0
                playing = False
                play_MIDI('Null.mid', sounds[instruments[currentInstrument]], mainSurface, True)
            elif x >= 0 and x <= 61 and y >= 164 and y <= 183:
                if not auto_name:
                    auto_name = True
                else:
                    auto_name = False
        if playing == True and (time.time() - startTime) >= duration[songs[currentSong]]:
            playing = False
            startTime = 0
            
        mainSurface.fill(0)
     
        #draw the play button: 
        mainSurface.blit(playButton, (0, 0)) 
     
        #draw the add song button:
        mainSurface.blit(musicNote, (0, 50))
     
        #draw the add instrument button:
        mainSurface.blit(plusButton, (0, 100))

        #draw the pause song button:
        mainSurface.blit(pauseButton, (55, 0))
        
        #draw the auto name button:
        text = 'AUTO'
        if not auto_name:
            renderedText = font4.render(text, 0, (255, 0, 0))
        else:
            renderedText = font4.render(text, 0, (0, 255, 0))
        text_rect = renderedText.get_rect(center=(30, 176))
        mainSurface.blit(renderedText, text_rect)

        #draw the progress bar:
        pygame.draw.rect(mainSurface, [255, 255, 255], [515, 820, 410, 30])
        if playing:
            perc = 410 * ((time.time() - startTime) / int(duration[songs[song]]))
            pygame.draw.rect(mainSurface, [0, 255, 0], [515, 820, perc, 30])
            #draw the time:
            seconds = round(time.time() - startTime)
            minutes = 0
            while seconds >= 60:
                seconds -= 60
                minutes += 1
            if seconds < 10:
                text = f'{minutes}:0{seconds}'
            else:
                text = f'{minutes}:{seconds}'
            renderedText = font3.render(text, 0, (255, 255, 255))
            text_rect = renderedText.get_rect(center=(720, 780))
            mainSurface.blit(renderedText, text_rect)
             
        #draw the rename song button: 
        text = 'Rename Song'
        renderedText = font3.render(text, 0, (0, 255, 0))
        text_rect = renderedText.get_rect(center=(1317, 888)) 
        mainSurface.blit(renderedText, text_rect)

        #draw the delete song button:
        text = 'Delete Song'
        renderedText = font3.render(text, 0, (255, 0, 0))
        text_rect = renderedText.get_rect(center=(969, 888))
        mainSurface.blit(renderedText, text_rect)

        #draw the rename instrument button:
        text = 'Rename Instrument'
        renderedText = font3.render(text, 0, (0, 0, 255))
        text_rect = renderedText.get_rect(center=(557, 888))
        mainSurface.blit(renderedText, text_rect)
        
        #draw the delete instrument button:
        text = 'Delete Instrument'
        renderedText = font3.render(text, 0, (255, 0, 0))
        text_rect = renderedText.get_rect(center=(145, 888))
        mainSurface.blit(renderedText, text_rect)                                  
     
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
    
    
    

