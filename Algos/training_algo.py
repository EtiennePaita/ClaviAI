import numpy as np
import tensorflow as tf
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.python.keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import argparse

# Add arguments to the script
parser = argparse.ArgumentParser(description='A program to train the AI.')
parser.add_argument("src_csv", help="The .csv dataset path.")
args = parser.parse_args()

# Implement Neurones
if __name__ == "__main__":
    data = np.loadtxt(args.src_csv, delimiter=',')

    X = data[:, :-1] / 255.0
    y = data[:, -1] 

    # Reshape 2D data for CNN model (nombre d'échantillons, hauteur, largeur, canaux)
# "-1" car NumPy calcule automatiquement cette dimension en fonction des autres dimensions et de la taille totale des données
    X = X.reshape(y.size,100,100,1)

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)  # Transformer labels en valeur numeric
    y = to_categorical(y)   # Converti en vecteur binaire

    print("Shape of X before split:", X.shape)
    print("Shape of y before split:", y.shape)

    # Split data into training and testing set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4) #random => garantit la reproductibilité des résultats  random_state=42

    # CNN Model
    model = Sequential()
    model.add(Conv2D(6, (3, 3), activation='relu', input_shape=(100,100,1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten(input_shape=(48, 48, 32))) # Transformer les caractéristiques spatiales en un vecteur 1D
    print("Shape after Flatten:", model.output_shape)
    model.add(Dropout(0.5)) # contrer l’overfitting
    model.add(Dense(20, activation='relu'))    # couche de 512 neurones
    model.add(Dense(2, activation='softmax'))  # 26 classification pour 26 lettres

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    print("----------------FIN-------------------")
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test))
