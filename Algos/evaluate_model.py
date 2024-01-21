import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import argparse

parser = argparse.ArgumentParser(description='A program to train the AI.')
parser.add_argument("src_csv", help="The .csv dataset path.")
args = parser.parse_args()

if __name__ == "__main__":
    data = np.loadtxt(args.src_csv, delimiter=',')

    X = data[:, :-1] / 255.0
    y = data[:, -1]

    X = X.reshape(y.size,100,100,1)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    y = to_categorical(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)

    loaded_model = load_model("model_clavier.keras") 
    evaluation_results = loaded_model.evaluate(X_test, y_test)
    print("Perte (Loss):", evaluation_results[0])
    print("Précision (Accuracy):", evaluation_results[1])

    #Prediction pour les 20 premiers exemples de l'ensemble de test
    predictions = loaded_model.predict(X_test[:20])
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = np.argmax(y_test[:20], axis=1)

    print("Classes réelles:", true_classes)
    print("Classes prédites:", predicted_classes)
    