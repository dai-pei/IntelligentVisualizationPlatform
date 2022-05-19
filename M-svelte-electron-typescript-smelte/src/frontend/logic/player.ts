import WaveSurfer from 'wavesurfer.js'
import { CurrentSongPath } from '../stores/status'

class Player{
    // 初始化
    constructor(){
        this.wavesurfer=null
        this.currentSongPath=null
        CurrentSongPath.subscribe(value=>{
            this.currentSongPath=value
        })
    }
    // 创建wavesurfer实例并播放
    async function start(song:string) {
        if(song)
        {
            CurrentSongPath.set(song)
        }        
        try{
            this.wavesurfer=WaveSurfer.create({
                backend: 'MediaElementWebAudio',
                container: '#waveform',
                height: 80,
                barMinHeight: 1,
                cursorWidth: 0,
                normalize: true,
                responsive: true,
                hideScrollbar: true,
            });
        }
    }

}