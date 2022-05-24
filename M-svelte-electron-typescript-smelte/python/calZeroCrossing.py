import librosa.display
import librosa
import numpy as np
import matplotlib.pyplot as plt

filepath='C:\\Users\\WINDOWS10\\Desktop\\dai-lab-workspace\\IntelligentVisualizationPlatform\\M-svelte-electron-typescript-smelte\\public\\medias\\test.wav'

y,sr=librosa.load(filepath)
# y=y[:250000]
zcrs = librosa.feature.zero_crossing_rate(y)
print(zcrs.shape)

plt.figure(figsize=(14, 5))
plt.plot(zcrs[0])
plt.show()

# n0 = 5000
# n1 = 10000
# plt.figure(figsize=(14, 5))
# plt.plot(y[n0:n1])
# plt.show()