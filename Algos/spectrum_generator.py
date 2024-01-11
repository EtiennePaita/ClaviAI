import os
import audio_spliter as AudioSpliter
import librosa
import matplotlib.pyplot as plt


# This function generate the spectrogram of all audio file in audio_split_directory_path directory into images_directory_path directory
def generate_spectrograms(
    audio_split_directory_path: str,
    images_directory_path: str
):
    print("Generating spectrograms ...")
    files = os.listdir(audio_split_directory_path)

    for filename in files:
        if AudioSpliter.isValidFile(filename):
            filePath = os.path.join(audio_split_directory_path, filename) 
            data_array, sample_rate= librosa.load(filePath) # Load audio file

            x = librosa.stft(data_array)
            xdb = librosa.amplitude_to_db(abs(x))

            # Create mel-spectrogram
            plt.figure(figsize=(0.5,0.5)) # Can modify figSize
            librosa.display.specshow(xdb, cmap='gray', sr=sample_rate, x_axis='off', y_axis='off') # Generate spectrogram
            infos = filename.split('.')
            name = infos[0]
            imagePath = os.path.join(images_directory_path, f"{name}.png") 
            plt.savefig(imagePath) # Save spectrogram image in imagePath
                 
