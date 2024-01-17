import pyaudio
import wave
import os
import audio_spliter as AudioSpliter
import spectrum_generator as SpectrumGenerator
import time
from multiprocessing import Process, Value
import ctypes

isRecording = False
isRunning = True

class AudioRecorder:
    
    def __init__(self, src_directory, dest_directory):
        self.srcDirectory, self.destDirectory = src_directory, dest_directory
        #self.initRecorder()
    
    def startRecording(self):
        global isRecording
        isRecording = True

    def stopRecording(self):
        global isRecording
        isRecording = False

    def initRecorder(self):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 3
        filename = os.path.join(self.srcDirectory, "output.wav")

        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording...')

        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 3 seconds
        
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

        AudioSpliter.split_all(self.srcDirectory, self.destDirectory)


        spectrum_path = os.path.join(self.destDirectory, "../Spectrums") 
        try:
            os.mkdir(spectrum_path)
            print("spectrum_path created")
        except FileExistsError:
            print("spectrum_path already created")
        
        SpectrumGenerator.generate_spectrograms(self.srcDirectory, spectrum_path)
        SpectrumGenerator.generate_spectrograms(self.destDirectory, spectrum_path)

    def build(self, isRecordingValue, responseValue):
        print("Building....")
        while isRunning:
            if isRecordingValue.value == 1:
                print("recording")
                responseValue.value = responseValue.value + "a"
                time.sleep(1)
            else:
                print("NOT recording")
                time.sleep(1)