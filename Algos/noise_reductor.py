from scipy.io import wavfile
import librosa
import noisereduce as nr
import os
import argparse


# Add arguments to the script
# parser = argparse.ArgumentParser(description='A program to generate a csv dataset based on audio files.')
# parser.add_argument("src_directory", help="The directory path containing the audio files. Make sure to add '/' at the end of the path.")
# parser.add_argument("dest_directory", help="")
# args = parser.parse_args()


AUDIO_VALID_EXTENSIONS = ('.m4a','.wav')

def isValidFile(filename: str) -> bool:
    for extension in AUDIO_VALID_EXTENSIONS:
        if filename.__contains__(extension):
            return True
    return False

def reduce_noise(src_directory, dest_directory):
    print("Reducing noises...")
    files = os.listdir(src_directory)
    print(f"{len(files)} files")

    for filename in files:
        if isValidFile(filename):
            filePath = os.path.join(src_directory, filename) 
            reducedFileName = filename.replace(".m4a", ".wav")
            filePathReduced = os.path.join(dest_directory, reducedFileName) 
            # load data
            data, sample_rate= librosa.load(filePath)
            # perform noise reduction
            reduced_noise = nr.reduce_noise(y=data, sr=sample_rate)
            wavfile.write(filePathReduced, sample_rate, reduced_noise)

            

# if __name__ == "__main__":
#     reduce_noise(args.src_directory, args.dest_directory)