import pyaudio
import wave
import os
import argparse
import audio_spliter as AudioSpliter
import spectrum_generator as SpectrumGenerator

# Add arguments to the script
parser = argparse.ArgumentParser(description='A program to record audio files.')
parser.add_argument("src_directory", help="The directory path containing the orignals audio files.")
parser.add_argument("dest_directory", help="The directory path that will contain the splitted audio files.")
args = parser.parse_args()

class AudioRecorder:
    def __init__(self, src_directory, dest_directory):
        self.srcDirectory, self.destDirectory, self.isRecording = src_directory, dest_directory, False
        self.initRecorder()

    def startRecording(self):
        self.isRecording = True

    def stopRecording(self):
        self.isRecording = False

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

        AudioSpliter.split_all(args.src_directory, args.dest_directory)


        spectrum_path = os.path.join(args.dest_directory, "../Spectrums") 
        try:
            os.mkdir(spectrum_path)
            print("spectrum_path created")
        except FileExistsError:
            print("spectrum_path already created")
        
        SpectrumGenerator.generate_spectrograms(args.src_directory, spectrum_path)
        SpectrumGenerator.generate_spectrograms(args.dest_directory, spectrum_path)

if __name__ == "__main__":
    audioRecorder = AudioRecorder(args.src_directory, args.dest_directory)
    