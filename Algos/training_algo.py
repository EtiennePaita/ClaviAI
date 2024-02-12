import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

# Add arguments to the script
# parser = argparse.ArgumentParser(description='A program to train the AI.')
# parser.add_argument("src_csv", help="The .csv dataset path.")
# args = parser.parse_args()

def fit_model(model_path, csv_path):
    data = np.loadtxt(csv_path, delimiter=',')
    X = data[:, :-1] / 255.0
    y = data[:, -1]
    X = X.reshape(y.size,100,100,1)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    y = to_categorical(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    model = load_model(model_path)   #inclut déjà les infos sur compil du modèle (optimizer,fonction perte, metric)
    print("----------------ENTRAINEMENT-------------------")
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)   #Arret précoce pour éviter le surapprentissage
    model.fit(X_train, y_train, epochs=60, validation_data=(X_test, y_test), verbose=0, callbacks=[early_stop])

    model.save(model_path)

def first_fit(model_path, csv_path):
    data = np.loadtxt(csv_path, delimiter=',')

    X = data[:, :-1] / 255.0
    y = data[:, -1]

    # Reshape 2D data for CNN model (nombre d'échantillons, hauteur, largeur, canaux)
    X = X.reshape(y.size,100,100,1)

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)  # Transformer labels en valeur numeric
    y = to_categorical(y)   # Converti en vecteur binaire

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)

    # CNN Model
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100,100,1))) # 6 filtres de taille 3x3 et spécificat° taille entrée
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(12, (3, 3), activation='relu', input_shape=(100,100,6)))
    model.add(BatchNormalization())     # normaliser les données - accélère la durée d'entrainement en augmenttant le learning rate
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten()) # Transformer les caractéristiques spatiales en un vecteur 1D
    model.add(Dropout(0.5)) # contrer l’overfitting    //désactive des sorties de neurones aléatoirement évite la co-adaptation
    model.add(Dense(20, activation='relu'))    # couche de 60 neurones
    model.add(Dense(26, activation='softmax'))  # 26 classification pour 26 lettres

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("----------------ENTRAINEMENT-------------------")
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)   #Arret précoce pour éviter le surapprentissage
    history = model.fit(X_train, y_train, epochs=60, validation_data=(X_test, y_test), callbacks=[early_stop])

    model.save(model_path)

    #Courbe d'apprentissage
    """
    training_accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']
    plt.plot(training_accuracy, label='Training')
    plt.plot(validation_accuracy, label='Validation')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    """

    #Matrice de confusion
    """
    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)

    cm = confusion_matrix(y_test_classes, y_pred_classes)
    color = 'white'
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()
    """


# Implement Neurones
# if __name__ == "__main__":
#     first_fit('model_clavier.keras', args.src_csv)