export let temp:number=1;
// import WaveSurfer from 'wavesurfer.js'
// // import { CurrentSongPath } from '../stores/status'

// class WavePlayer{
//     // 初始化
//     wavesurfer:any;
//     currentSongPath:string;
//     constructor(){
//         this.wavesurfer=null;
//         this.currentSongPath="";
//         CurrentSongPath.subscribe(value=>{
//             this.currentSongPath=value
//         });
//     }
//     // 创建wavesurfer实例并播放
//     async start(song:string) {
//         if(song)
//         {
//             CurrentSongPath.set(song)
//         }        
//         try{
//             this.wavesurfer=WaveSurfer.create({
//                 backend: 'MediaElementWebAudio',
//                 container: '#waveform',
//                 height: 80,
//                 barMinHeight: 1,
//                 cursorWidth: 0,
//                 normalize: true,
//                 responsive: true,
//                 hideScrollbar: true,
//             });
//             this.wavesurfer.play();
//         }catch(e){
//             console.warn("in player start func",e);
//         }
//     }
//     async playPause() {
//         if (this.wavesurfer) {
//             if (this.wavesurfer.isPlaying()) {
//                 await this.fadeOut();
//                 this.wavesurfer.pause();
//             } else {
//                 this.wavesurfer.play();
//                 await this.fadeIn();
//             }
//         } else {
//             CurrentSongPath.subscribe(value=>{
//                 this.currentSongPath=value;
//             });
//             await this.start(this.currentSongPath);
//         }
//     }
//     async fadeIn() {
//         // this.filterFade.gain.setValueAtTime(0.01, this.filterFade.context.currentTime);
//         // this.filterFade.gain.exponentialRampToValueAtTime(1, this.filterFade.context.currentTime + 0.5);
//         console.log("function fade in");
//     }

//     async fadeOut() {
//         // this.filterFade.gain.setValueAtTime(1, this.filterFade.context.currentTime);
//         // this.filterFade.gain.exponentialRampToValueAtTime(0.01, this.filterFade.context.currentTime + 0.3);
//         // await sleep(300); // wait for fade to end before continuing
//         console.log("function fade out");
//     }

// }

// export default WavePlayer;