# Guide d'utilisation ClaviAI


Membres du groupe : Etienne Païta, Elsa Firmin


------------------------------



Le dossier **KeyboardAudio** contient notre dataset audio des sons des touches d'un clavier. Chaque audio comporte 20 pressions de la touche indiqué dans le nom du fichier.

Le dossier **Data** est généré avec le programme `dataset_generator.py`. Il contient les audios du dataset découpés afin d'avoir uniquement le son d'une touche, les spectrogrammes générés à partir des sons des touches, ainsi que le fichier images.csv


------------------------------


Pour générer le dataset il faut lancer `dataset_generator.py` dans le fichier **Algos**. Paramètres du programme :
* **src_directory**, "The directory path containing the audio files. Make sure to add '/' at the end of the path."
* **dest_directory**, "The directory path that will contain the spectograms image files. Make sure to add '/' at the end of the path."

Exemple : `python3 dataset_generator.py ./KeyboardAudio ./`

`dataset_generator.py` utilise les programmes audio_spliter.py et spectrum_generator.py



------------------------------



`training_algo.py` permet de lancer l'apprentissage à partir du csv généré avec le programme précédent. Paramètres du programme :
* **src_csv**, The .csv dataset path.
    
Exemple : `python3 dataset_generator.py ./Data/images.csv`



------------------------------



**app.py** est le prototype d'application fait avec PyQT5

Ce programme n'a pas encore été lié avec les autres programmes.



------------------------------

Pour lancer les différents script sur MacOS M1 et +, il faut faire les étapes suivantes :

* Executer les commandes suivantes pour créer un environnement virtuel:
```
python3 -m venv ~/tensorflow-metal
source ~/tensorflow-metal/bin/activate
```

* Lancer le script `setup_mac_script.py` :
```
python3 setup_mac_script.py
```


------------------------------

Sources :

https://superfastpython.com/multiprocessing-pool-configure/
https://superfastpython.com/multiprocessing-shared-ctypes-in-python/
https://superfastpython.com/multiprocessing-in-python/




