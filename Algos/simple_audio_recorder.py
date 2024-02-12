import pyaudio
import wave
import os, shutil


class SimpleAudioRecorder:
    
    def __init__(self, dest_directory):
        self.destDirectory = dest_directory
        self.outputFolderPath = os.path.join(dest_directory, "DataPlus")
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

    def getOutputFolderPath(self):
        return self.outputFolderPath

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


    def clearFiles(self):
        self.removeFolder(self.outputFolderPath)

    def record(self, _filename_, seconds):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        filename = os.path.join(self.outputFolderPath, _filename_)

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