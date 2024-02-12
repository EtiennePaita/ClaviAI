import numpy as np
import tensorflow as tf
import argparse
from sklearn.model_selection import GridSearchCV
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from scikeras.wrappers import KerasClassifier

# Add arguments to the script
# parser = argparse.ArgumentParser(description='A program to train the AI.')
# parser.add_argument("src_csv", help="The .csv dataset path.")
# args = parser.parse_args()

# Fonction pour créer le modèle
def create_model(neurons):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100,100,1))) # 6 filtres de taille 3x3 et spécificat° taille entrée
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(12, (3, 3), input_shape=(100,100,6)))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten()) # Transformer les caractéristiques spatiales en un vecteur 1D
    model.add(Dropout(0.3))
    model.add(Dense(neurons, activation='relu'))
    model.add(Dense(26, activation='softmax'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# if __name__ == "__main__":
#     data = np.loadtxt(args.src_csv, delimiter=',')

#     X = data[:, :-1] / 255.0
#     y = data[:, -1]

#     # Reshape 2D data for CNN model (nombre d'échantillons, hauteur, largeur, canaux)
#     X = X.reshape(y.size,100,100,1)

#     # Convertir les labels en valeurs numériques
#     label_encoder = LabelEncoder()
#     y_encoded = label_encoder.fit_transform(y)

#     # Convertir les labels en vecteurs binaires (one-hot encoding)
#     y_categorical = to_categorical(y_encoded)

#     # Séparer les données en ensembles d'entraînement et de test
#     X_train, X_test, y_train, y_test = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

#     optimizer = tf.keras.optimizers.Nadam(learning_rate=0.02)
#     model = KerasClassifier(model=create_model, loss="binary_crossentropy",optimizer=optimizer, epochs=10, batch_size=40, verbose=0)
#     # define the grid search parameters
#     neurons = [30, 50, 55, 60, 65, 70, 75, 100, 256]
#     param_grid = dict(model__neurons=neurons)
#     grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=3)
#     grid_result = grid.fit(X_train, y_train)
#     # summarize results
#     print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
#     means = grid_result.cv_results_['mean_test_score']
#     stds = grid_result.cv_results_['std_test_score']
#     params = grid_result.cv_results_['params']
#     for mean, stdev, param in zip(means, stds, params):
#         print("%f (%f) with: %r" % (mean, stdev, param))
