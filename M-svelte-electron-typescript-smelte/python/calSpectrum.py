from stat import S_IFBLK
import librosa
import numpy as np

y,sr=librosa.load('C:\\Users\\WINDOWS10\\Desktop\\dai-lab-workspace\\IntelligentVisualizationPlatform\\M-svelte-electron-typescript-smelte\\public\\medias\\test.wav')
# stft参数配置
# https://blog.csdn.net/sinat_35821976/article/details/105739909
S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
S_db=librosa.power_to_db(S ** 2)

print(S_db.shape)