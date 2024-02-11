import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


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
    X = X.reshape(y.size,100,100,1)

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)  # Transformer labels en valeur numeric
    y = to_categorical(y)   # Converti en vecteur binaire

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6) #random => garantit la reproductibilité des résultats  random_state=42

    # CNN Model
    model = Sequential()
    model.add(Conv2D(12, (3, 3), activation='relu', input_shape=(100,100,1))) # 6 filtres de taille 3x3 et spécificat° taille entrée
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(30, (3, 3), input_shape=(100,100,12)))
    model.add(MaxPooling2D((2, 2))) 

    model.add(Flatten()) # Transformer les caractéristiques spatiales en un vecteur 1D
    model.add(Dropout(0.5)) # contrer l’overfitting    //désactive des sorties de neurones aléatoirement évite la co-adaptation
    model.add(Dense(50, activation='relu'))    # couche de 512 neurones
    model.add(Dense(26, activation='softmax'))  # 26 classification pour 26 lettres

    model = load_model("model_clavier.keras")   #inclut déjà les infos sur compil du modèle (optimizer,fonction perte, metric)
    #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    print("----------------ENTRAINEMENT-------------------")
    model.fit(X_train, y_train, epochs=110, validation_data=(X_test, y_test))

    #model.save('model_clavier.keras')

    y_pred = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)

    cm = confusion_matrix(y_test_classes, y_pred_classes)
    color = 'white'
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()
    
    plt.plot(y_test_classes, linewidth=0.5)
    plt.plot(y_pred_classes, linewidth=0.5)
    plt.show()



    

