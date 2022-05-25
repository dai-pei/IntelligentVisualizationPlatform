from cgi import print_arguments
import librosa
filepath='C:\\Users\\WINDOWS10\\Desktop\\dai-lab-workspace\\IntelligentVisualizationPlatform\\M-svelte-electron-typescript-smelte\\public\\medias\\test.wav'
y,sr=librosa.load(filepath)
startsec=0
endsec=0.5
samples = librosa.samples_like(y,hop_length=1)
print('samples = %s'%samples)
times = librosa.frames_to_time(samples,sr=sr,hop_length=1)
print('times = %s'%times)



findTimeIndex(0.5)
