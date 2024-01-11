import subprocess

#subprocess.run(["python3", "-m", "venv", "~/tensorflow-metal"])
#subprocess.run(["source", "~/tensorflow-metal/bin/activate"])
subprocess.run(["python", "-m", "pip", "install", "-U", "pip"])
subprocess.run(["python", "-m", "pip", "install", "tensorflow-macos"])
subprocess.run(["python", "-m", "pip", "install", "tensorflow-metal"])
subprocess.run(["python", "-m", "pip", "install", "-U", "scikit-image"])
subprocess.run(["python", "-m", "pip", "install", "-U", "matplotlib"])
subprocess.run(["python", "-m", "pip", "install", "librosa"])
subprocess.run(["python", "-m", "pip", "install", "pyqt5"])
