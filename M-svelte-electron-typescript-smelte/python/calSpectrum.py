import librosa.display
import librosa
import numpy as np
import matplotlib.pyplot as plt

y,sr=librosa.load('C:\\Users\\WINDOWS10\\Desktop\\dai-lab-workspace\\IntelligentVisualizationPlatform\\M-svelte-electron-typescript-smelte\\public\\medias\\drum.wav')
# stft参数配置
# https://blog.csdn.net/sinat_35821976/article/details/105739909
S = np.abs(librosa.stft(y,n_fft=2048,window='hann'))
S_db=librosa.power_to_db(S ** 2)
librosa.display.specshow(S_db,y_axis='log', x_axis='time')
plt.show()

# print(S_db.shape)