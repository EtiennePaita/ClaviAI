import numpy as np
import argparse
import os
from tensorflow.keras.models import load_model
import dataset_generator as DatasetGenerator

# parser = argparse.ArgumentParser(description='A program to generate a csv dataset based on audio files.')
# parser.add_argument("src_directory", help="The directory path containing the audio files. Make sure to add '/' at the end of the path.")
# parser.add_argument("dest_directory", help="The directory path that will contain the spectograms image files. Make sure to add '/' at the end of the path.")
# args = parser.parse_args()


# Ajouter l'audio path
def predict_letter(model_path, src_directory):
    csv_file = DatasetGenerator.process_audio_files(src_directory, src_directory, True)
    csvPath = os.path.join(src_directory, "Data")
    csvPath = os.path.join(csvPath, csv_file) 

    data = np.loadtxt(csvPath, delimiter=',')
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    X = data[:, :-1] / 255.0
    y = data[:, -1]
    X = X.reshape(y.size, 100, 100, 1)
    
    model = load_model(model_path)
    predictions = model.predict(X)

    return predictions

#if __name__ == "__main__":
    # Spécifiez le chemin du fichier audio que vous souhaitez prédire
    #audio_file_path = "chemin/vers/votre/fichier/audio.m4a"
    #model_path = "model_clavier.keras"

#     predictions = predict_letter(model_path, args.src_directory)
#     predictions = np.argmax(predictions, axis=1)    #prend l'indice de la plus grande valeur => enleve les pourcentages de
#                                                     # chaque classe

#     # classe 0 => A / classe 1 => B ...
#     print(predictions)