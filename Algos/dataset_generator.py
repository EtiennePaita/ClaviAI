from skimage import io
import os
import audio_spliter as AudioSpliter
import spectrum_generator as SpectrumGenerator
import argparse

# Add arguments to the script
parser = argparse.ArgumentParser(description='A program to generate a csv dataset based on audio files.')
parser.add_argument("src_directory", help="The directory path containing the audio files. Make sure to add '/' at the end of the path.")
parser.add_argument("dest_directory", help="The directory path that will contain the spectograms image files. Make sure to add '/' at the end of the path.")
args = parser.parse_args()

CSV_FILE_NAME = 'images_test.csv'
AUDIO_SPLIT_DIRECTORY_NAME = 'AudioSplit'
IMAGES_DIRECTORY_NAME = 'Images'
IMG_VALID_EXTENSION = '.png'

# This function convert an alphabet char to ascii normalized value (0-25)
def convert_letter_to_ascii_result(letter):
    ascii = ord(letter)
    if ascii >= ord('a') and ascii <= ord('z'):
        return ascii - ord('a') + 1
    if ascii >= ord('A') and ascii <= ord('Z'):
        return ascii - ord('A') + 1
    return -1


# This function generate the .csv dataset with the spectrograms created
def generate_dataset(
    images_directory_path: str,
    data_directory_path: str
):
    print("Generating dataset ...")
    files = os.listdir(images_directory_path)

    csvPath = os.path.join(data_directory_path, CSV_FILE_NAME) 
    f = open(csvPath, 'w') # open or create .csv data
    for filename in files:
        if filename.__contains__(IMG_VALID_EXTENSION):
            filePath = os.path.join(images_directory_path, filename) 
            img = io.imread(filePath) # Read image pixels
            infos = filename.split('_')
            letter = infos[0]
            print(f"letter : {letter}")
            line = img.flatten()
            line = ', '.join(map(str, line)) + f', {convert_letter_to_ascii_result(letter)}\n'
            f.write(line)
    f.close()    

if __name__ == "__main__":
    
    # Creation of required directories
    dataPath = os.path.join(args.dest_directory, "Data") 
    audioSplitPath = os.path.join(dataPath, AUDIO_SPLIT_DIRECTORY_NAME) 
    imagesPath = os.path.join(dataPath, IMAGES_DIRECTORY_NAME) 
    try:
        os.mkdir(dataPath)
        print("dataPath created")
    except FileExistsError:
        # Should delete --force dataPath and recreate it
        print("dataPath already created")

    try:
        os.mkdir(audioSplitPath) 
        print("audioSplitPath created")
    except FileExistsError:
        print("audioSplitPath already created")

    try:
        os.mkdir(imagesPath)
        print("imagesPath created")
    except FileExistsError:
        print("imagesPath already created")


    # Split src_directory's audio files (if multiple press)
    AudioSpliter.split_all(args.src_directory, audioSplitPath)

    # First step : generate the spectrogram of audio data
    SpectrumGenerator.generate_spectrograms(audioSplitPath, imagesPath)

    # Second step : generate the csv dataset of the images
    generate_dataset(imagesPath, dataPath)