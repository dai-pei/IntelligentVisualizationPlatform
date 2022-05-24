import librosa.display
import librosa
import numpy as np
import matplotlib.pyplot as plt

filepath='C:\\Users\\WINDOWS10\\Desktop\\dai-lab-workspace\\IntelligentVisualizationPlatform\\M-svelte-electron-typescript-smelte\\public\\medias\\test.wav'

y,sr=librosa.load(filepath)

print(librosa.get_duration(y,sr))