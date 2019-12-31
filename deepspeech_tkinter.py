#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 16:54:31 2019

@author: batman
"""

from tkinter import Tk      	       # GUI library in python 
from tkinter import Text
from tkinter import Button, END
from tkinter import N, W
from tkinter import Label
import numpy as np
import wave			       # write audio data in raw format to file
from deepspeech import Model    # recognize words in a given audio
import pyaudio		      # used to write audio data to stream
import threading                           
import os

class deepspeech_tkinter_window():
    def __init__(self):
        self.t1 = None
        self.t2 = None
        self.filename = 'output.wav'
        self.welcome_text = None
        self.change_status = False
        

    
    def start_recording(self):
        chunk = 320  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample Done
        channels = 1  # Done
        fs = 16000  # Record at 44100 samples per second Done        
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        print(self.filename,"filename")
        
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)
        frames = []  # Initialize array to store frames
        
        while True:
            data = stream.read(chunk)
            frames.append(data)
            if self.change_status:
                data = stream.read(chunk)
                frames.append(data)
                break
        
                
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    def stop_recording(self):
        self.change_status = True
        
    def thread_start(self):
        self.t1.start()
    
    def thread_stop(self):
        self.t2.start()
    	
    	
    def generate_text(self):
        print(self.t1.isAlive(),"check thread t1 is alive or not")
        print(self.t2.isAlive(),"check thread t2 is alive or not")
        
        self.change_status = False
        
        self.t1 = threading.Thread(target=self.start_recording)
        self.t2 = threading.Thread(target=self.stop_recording)
        
        model_path = '/home/batman/python_projects/flask_blog_version1/myblog/models/deepspeech/deepspeech-0.5.1-models/'
        # Numeric values are configurable
        ds = Model(model_path+'output_graph.pbmm',
                   26,
                   9,
                   model_path+'alphabet.txt',
                   500)
        ds.enableDecoderWithLM(model_path+'alphabet.txt',
                               model_path+'lm.binary',
                               model_path+'trie',
                               0.75, 1.85)
        
        
        def load_audio(audio_path):
            fin = wave.open(audio_path, 'rb')
            audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
            fin.close()
            return audio
        
        
        def frame_rate(audio_path):
            fin = wave.open(audio_path, 'rb')
            sample_rate = fin.getframerate()
            fin.close()
            return sample_rate
        
        
        audio_file = self.filename
        field_value = ds.stt(load_audio(audio_file), frame_rate(audio_file))
        self.welcome_text.delete('1.0', END)
        self.welcome_text.insert(END, field_value)
    
    	
    def main(self):
                
        root = Tk()
        root.minsize(600,400)
        root.title("Speech to Text Using DeepSpeech") # welcome window title
        root.configure(background="light blue") 
        window_height = 300
        window_width = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
                # finding middle place of screen
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.welcome_text = Text(root,width=50, height=15)
        self.welcome_text.grid(column=0, row=0,rowspan=3,columnspan=3,padx=20,pady=20)
        quote = "Audio text appear here"
        self.welcome_text.insert(END, quote)
        
        # threading module is used for recording audio
        self.t1 = threading.Thread(target=self.start_recording)
        self.t2 = threading.Thread(target=self.stop_recording)
        
        
        
        Button(root, text='Start Rec.', command=self.thread_start,
               height= 2, 
               width=8, 
               font=(None, 15),bg='white').grid(row=0,column=3)
        Button(root,command=self.thread_stop,
               text='Stop Rec.',
               height=2, 
               width=8, 
               font=(None, 15),bg='white').grid(row=1,column=3)
        Button(root, text='TEXT !!',command=self.generate_text,
               height=2, width=8, font=(None, 15),bg='white').grid(row=2,column=3)
        
        Label(root, text=self.filename,width=70,
              height=3,bg='white').grid(column=0, row=4, 
                                 columnspan=5, sticky=(N, W), padx=20,pady=20)        
        root.mainloop()


tkinter_window_var = deepspeech_tkinter_window()
tkinter_window_var.main()
	
	
	

