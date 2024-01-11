import librosa
import soundfile as sf
import os

AUDIO_VALID_EXTENSIONS = ('.m4a','.wav')

def isValidFile(filename: str) -> bool:
    for extension in AUDIO_VALID_EXTENSIONS:
        if filename.__contains__(extension):
            return True
    return False



def split_file(
    filename: str, 
    srcDirectory: str, 
    destDirectory: str
):
     # Load the audio file
    fPath = os.path.join(srcDirectory, filename)
    y, sr = librosa.load(fPath)

    # Define the duration in seconds for splitting
    sound_duration_frame = librosa.time_to_frames(0.15, sr=sr) # convert a time (in second) to a frame value based on the sample_rate (sr)

    # Get beat_frames of the audio (every peep of noise)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
    print(beat_frames)

    num_splits = int(len(beat_frames))
    # Split the audio file
    for i in range(num_splits):
        #Calculate start and end frame of each beat_frame
        start = beat_frames[i] - librosa.time_to_frames(0.07, sr=sr)
        end = beat_frames[i] + sound_duration_frame

        res = librosa.frames_to_samples((start,end)) # Convert start and end frames to samples
        split_audio = y[res[0]:res[1]] # Get split audio at the interval
        
        new_file_name = f"{filename.split('.')[0]}_{i + 1}.wav"
        # Save split audio
        split_filename = os.path.join(destDirectory, new_file_name)
        sf.write(split_filename, split_audio, sr)



def split_all(
    srcDirectory: str, 
    destDirectory: str
):
    print("Splitting ...")
    files = os.listdir(srcDirectory)
    print(f"{len(files)} files")

    for filename in files:
        if isValidFile(filename):
            split_file(filename, srcDirectory, destDirectory)

