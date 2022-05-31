import librosa.display
import librosa
import numpy as np
import matplotlib.pyplot as plt

def getNearestLen(framelength,sr):
    framesize = framelength*sr  
    #找到与当前framesize最接近的2的正整数次方
    nfftdict = {}
    lists = [32,64,128,256,512,1024]
    for i in lists:
        nfftdict[i] = abs(framesize - i)
    sortlist = sorted(nfftdict.items(), key=lambda x: x[1])#按与当前framesize差值升序排列
    framesize = int(sortlist[0][0])#取最接近当前framesize的那个2的正整数次方值为新的framesize
    return framesize

y,sr=librosa.load('C:/Users/WINDOWS10/Desktop/dai-lab-workspace/0_IntelligentVisualizationPlatform/M-svelte-electron-typescript-smelte/public/medias/longdrumsong.wav')
# N_FFT=getNearestLen(0.25,sr)
# print(N_FFT)
N_FFT=1024

mfcc_data=librosa.feature.mfcc(y=y, sr=sr,S=None, n_mfcc=20, dct_type=2, 
norm='ortho',n_fft=N_FFT,hop_length=int(N_FFT/4))

print(mfcc_data)