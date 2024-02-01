import pyaudio
import wave
import os, shutil
import audio_spliter as AudioSpliter
import spectrum_generator as SpectrumGenerator
import real_test as RealTest
import time
from multiprocessing import Process, Value
import ctypes

import numpy as np


#   TODO : 
#       - call createEnv() only on record()
#       - delete Output folder at each record()
#       - save outputs and global specters in Cache folder
#


class AudioRecorder:
    
    def __init__(self, dest_directory):
        self.destDirectory = dest_directory
        self.outputFolderPath = os.path.join(dest_directory, "Outputs")
        self.model_path = os.path.join(dest_directory, "model_clavier.keras") #"Algos/model_clavier.keras"
        print(self.model_path)
        self.cacheFolderPath = os.path.join(dest_directory, "Cache")
        self.rtAudioFolderPath = os.path.join(self.outputFolderPath, "RTAudios")
        self.spectrum_path = os.path.join(self.outputFolderPath, "Spectrums") 
        self.createEnv()

    def removeFolder(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def createEnv(self):
        # Create Output folder
        try:
            os.mkdir(self.outputFolderPath)
            print("Output folder created")
        except FileExistsError:
            # TODO : Delete folder and all files inside
            print("Output folder already created")
            print("Removing...")
            self.removeFolder(self.outputFolderPath)

        # # Create Cache folder to save an history
        # try:
        #     os.mkdir(self.cacheFolderPath)
        #     print("Cache folder created")
        # except FileExistsError:
        #     print("Cache folder already created")

        # # Create RTAudios & Spectrums folders inside of Output folder
        # try:
        #     os.mkdir(self.rtAudioFolderPath)
        #     os.mkdir(self.spectrum_path)
        #     print("Folders created")
        # except FileExistsError:
        #     print("Folders seems to be already created")

    def getCachedFilename(self):
        files = os.listdir(self.cacheFolderPath)
        return f"output_{files.size}.wav"

    def getLetter(self, value):
        if(value == 0): return 'M' 
        else: return 'Q'

    def convertToString(self, tab):
        res = ""
        for letter in tab:
            res += self.getLetter(letter)

        return res

    def record(self):
        self.createEnv()
        
        
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 2
        filename = os.path.join(self.outputFolderPath, "output.wav")

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording...')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)

        # Stop and close the stream 
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('Finished recording')

        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        predictions = RealTest.predict_letter(self.model_path, self.outputFolderPath)
        print(f"--------------------======== Predictions result : ->{predictions}")
        predict = np.argmax(predictions, axis=1)
        return predict
        # AudioSpliter.split_all(self.outputFolderPath, self.rtAudioFolderPath)
        # SpectrumGenerator.generate_spectrograms(self.outputFolderPath, self.spectrum_path)
        # SpectrumGenerator.generate_spectrograms(self.rtAudioFolderPath, self.spectrum_path)

    def build(self, isRecordingValue, responseValue):
        print("Building....")
        while True:
            if isRecordingValue.value == 1:
                print("recording")
                try:
                    prediction = self.record()
                    print(f"************ Prediction result : ->{prediction}")
                    responseValue.value = responseValue.value + self.convertToString(prediction)
                except Exception as e:
                    print(f"Exception value: {e}")