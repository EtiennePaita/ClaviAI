import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
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

    unique_classes = np.unique(data[:, -1])
    print("Classes d'origine:", unique_classes)

    # Reshape 2D data for CNN model (nombre d'échantillons, hauteur, largeur, canaux)
# "-1" car NumPy calcule automatiquement cette dimension en fonction des autres dimensions et de la taille totale des données
    X = X.reshape(y.size,100,100,1)

    # Encode labels
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)  # Transformer labels en valeur numeric
    y = to_categorical(y)   # Converti en vecteur binaire

    #print("Shape of X before split:", X.shape)
    #print("Shape of y before split:", y.shape)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4) #random => garantit la reproductibilité des résultats  random_state=42

    # CNN Model
    model = Sequential()
    model.add(Conv2D(6, (3, 3), activation='relu', input_shape=(100,100,1))) # 6 filtres de taille 3x3 et spécificat° taille entrée
    model.add(MaxPooling2D((2, 2)))

    model.add(Conv2D(12, (3, 3), input_shape=(100,100,6)))
    model.add(MaxPooling2D((2, 2))) 

    model.add(Flatten(input_shape=(48, 48, 32))) # Transformer les caractéristiques spatiales en un vecteur 1D
    #print("Shape after Flatten:", model.output_shape)
    model.add(Dropout(0.5)) # contrer l’overfitting    //désactive des sorties de neurones aléatoirement évite la co-adaptation
    model.add(Dense(20, activation='relu'))    # couche de 512 neurones
    model.add(Dense(2, activation='softmax'))  # 26 classification pour 26 lettres

    model = load_model("model_clavier.keras")   #inclut déjà les infos sur compil du modèle (optimizer,fonction perte, metric)
    #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print("----------------ENTRAINEMENT-------------------")
    y_test_classes = np.argmax(y_test, axis=1)
    y_test_original = label_encoder.inverse_transform(y_test_classes)
    print(f"Classes réelles : {y_test_original}\n")

    for epoch in range(10):
        #[0. 1.] représente la classe 0 (Q)
        #[1. 0.] représente la classe 1 (M)
        
        model.fit(X_train, y_train, epochs=1, validation_data=(X_test, y_test))

        y_pred = model.predict(X_test)
        
        # Transforme mon tableau de 2 dimensions en 1 tableau de 1 dimension en renvoyant l'indice de la valeur max
        # par ex: np.argmax([1., 0.]) renvoie 0
        y_pred_classes = np.argmax(y_pred, axis=1)
        
        # Remplace les indices par les valeurs originales(13 et 17)
        y_pred_original = label_encoder.inverse_transform(y_pred_classes)
        print(f"Époque {epoch + 1} - Classes prédites : {y_pred_original}")
    
    model.save('model_clavier.keras')
