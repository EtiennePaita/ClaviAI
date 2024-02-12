from skimage import io
import os
import audio_spliter as AudioSpliter
import spectrum_generator as SpectrumGenerator
import noise_reductor as NoiseReductor
import argparse

# Add arguments to the script
# parser = argparse.ArgumentParser(description='A program to generate a csv dataset based on audio files.')
# parser.add_argument("src_directory", help="The directory path containing the audio files. Make sure to add '/' at the end of the path.")
# parser.add_argument("dest_directory", help="The directory path that will contain the spectograms image files. Make sure to add '/' at the end of the path.")
# args = parser.parse_args()

CSV_FILE_NAME = 'images.csv'
AUDIO_SPLIT_DIRECTORY_NAME = 'AudioSplit'
AUDIO_PROCESSED_DIRECTORY_NAME = 'AudioProcessed'
IMAGES_DIRECTORY_NAME = 'Images'
IMG_VALID_EXTENSION = '.png'
ORIGINAL_DIRECTORY = 'original'
REDUCED_DIRECTORY = 'reduced'

# This function convert an alphabet char to ascii normalized value (0-25)
def convert_letter_to_ascii_result(letter):
    ascii = ord(letter[0])
    if ascii >= ord('a') and ascii <= ord('z'):
        return ascii - ord('a') + 1
    if ascii >= ord('A') and ascii <= ord('Z'):
        return ascii - ord('A') + 1
    return -1


# This function generate the .csv dataset with the spectrograms created
def generate_dataset(
    images_directory_path: str,
    data_directory_path: str,
    random_generation: bool
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

            if random_generation:
                line = ', '.join(map(str, line)) + f", {ord('_')}\n"
            else:
                line = ', '.join(map(str, line)) + f', {convert_letter_to_ascii_result(letter)}\n'
            
            f.write(line)
    f.close()    

def process_audio_files(src_directory, dest_directory, random_generation: bool = False):
    # Creation of required directories
    dataPath = os.path.join(dest_directory, "Data") 
    audioProcessedPath = os.path.join(dataPath, AUDIO_PROCESSED_DIRECTORY_NAME) 
    audioSplitPath = os.path.join(dataPath, AUDIO_SPLIT_DIRECTORY_NAME) 
    audioSplitOriginalPath = os.path.join(audioSplitPath, ORIGINAL_DIRECTORY) 
    audioSplitReducedPath = os.path.join(audioSplitPath, REDUCED_DIRECTORY) 
    imagesPath = os.path.join(dataPath, IMAGES_DIRECTORY_NAME) 
    imagesOriginalPath = os.path.join(imagesPath, ORIGINAL_DIRECTORY) 
    imagesReducedPath = os.path.join(imagesPath, REDUCED_DIRECTORY) 
    
    try:
        os.mkdir(dataPath)
        print("dataPath created")
    except FileExistsError:
        # Should delete --force dataPath and recreate it
        print("dataPath already created")


    try:
        os.mkdir(audioProcessedPath) 
        print("audioSplitPath created")
    except FileExistsError:
        print("audioSplitPath already created")


    try:
        os.mkdir(audioSplitPath) 
        print("audioSplitPath created")
    except FileExistsError:
        print("audioSplitPath already created")

    try:
        os.mkdir(audioSplitOriginalPath) 
        print("audioSplitOriginalPath created")
    except FileExistsError:
        print("audioSplitOriginalPath already created")
    
    try:
        os.mkdir(audioSplitReducedPath) 
        print("audioSplitReducedPath created")
    except FileExistsError:
        print("audioSplitReducedPath already created")



    try:
        os.mkdir(imagesPath)
        print("imagesPath created")
    except FileExistsError:
        print("imagesPath already created")

    try:
        os.mkdir(imagesOriginalPath)
        print("imagesOriginalPath created")
    except FileExistsError:
        print("imagesOriginalPath already created")

    try:
        os.mkdir(imagesReducedPath)
        print("imagesReducedPath created")
    except FileExistsError:
        print("imagesReducedPath already created")


    # Reduce noise of audios
    NoiseReductor.reduce_noise(src_directory, audioProcessedPath)

    # Split src_directory's audio files (if multiple press)
    AudioSpliter.split_all(src_directory, audioSplitOriginalPath)
    AudioSpliter.split_all(audioProcessedPath, audioSplitReducedPath)

    # First step : generate the spectrogram of audio data
    SpectrumGenerator.generate_spectrograms(audioSplitOriginalPath, imagesOriginalPath)
    SpectrumGenerator.generate_spectrograms(audioSplitReducedPath, imagesReducedPath)

    # Second step : generate the csv dataset of the images
    generate_dataset(imagesReducedPath, dataPath, random_generation)    

    return CSV_FILE_NAME

# if __name__ == "__main__":
#     process_audio_files(args.src_directory, args.dest_directory)