<script lang="ts">
import WaveSurfer from 'wavesurfer.js'
import TimelinePlugin from 'wavesurfer.js/src/plugin/timeline';
import SpectrogramPlugin from 'wavesurfer.js/src/plugin/spectrogram'
import CursorPlugin from 'wavesurfer.js/src/plugin/cursor'
import {
    onMount
} from 'svelte'
import {
    Sleep
} from '../logic/helper'

let wavesurfer: any
onMount(() => {
    wavesurfer = WaveSurfer.create({
        container: '#waveform',
        barHeight: 2,
        cursorColor: '#ff0000',
        progressColor: '#0000ff',
        scrollParent: true,
        height: 160,
        cursorWidth: 2,
        autoCenter: false,
        fillParent: true,
        hideScrollbar: false,

        plugins: [
            TimelinePlugin.create({ //timeline plugin
                container: "#wave-timeline",
                height: 90,
            }),
            CursorPlugin.create({ //cursor plugin
                container: "#wave-cursor",
                showTime: true,
                customShowTimeStyle: {
                    'background-color': '#000',
                    color: '#fff',
                    padding: '2px',
                    'font-size': '10px'
                }
            }),
            SpectrogramPlugin.create({
                wavesurfer: wavesurfer,
                container: "#wave-spectrogram",
                labels: true,
                fftSamples: 512
            })
        ]

    });
    //TimeLine
    wavesurfer.on('ready', function() {
        var timeline = Object.create(TimelinePlugin);

        timeline.create({
            wavesurfer: wavesurfer,
            container: '#wave-timeline'
        });
    });

})

var d1 = new Date(); //test
console.log(d1.toLocaleString()); //test
console.log('test'); //test

// // Zoom slider
// var slider = document.querySelector('[data-action="zoom"]');
// slider.value = wavesurfer.params.minPxPerSec;
// slider.min = wavesurfer.params.minPxPerSec;
// slider.addEventListener('input', function() {
//     wavesurfer.zoom(Number(this.value));
// });

function btnStop1() {
    wavesurfer.stop();
}

function btnPlay1() {
    wavesurfer.play();
}

function btnPause1() {
    wavesurfer.pause();
}

function btnPlayPause1() {
    wavesurfer.playPause();
}

async function fileUploadedAndInitWave(e: Event) {
    const target = e.target as HTMLInputElement;
    const files = target.files;
    if (!files) {
        return;
    }

    const file = files[0];
    if (!file) {
        return;
    }

    console.log(file.name)

    if (file) {
        var reader = new FileReader();

        reader.onload = function(evt) {
            // Create a Blob providing as first argument a typed array with the file buffer
            var blob = new window.Blob([new Uint8Array(evt.target.result)]);

            // Load the blob into Wavesurfer
            wavesurfer.loadBlob(blob);
        };

        reader.onerror = function(evt) {
            console.error("An error ocurred reading the file: ", evt);
        };

        // Read File as an ArrayBuffer
        reader.readAsArrayBuffer(file);

        console.log(wavesurfer.getDuration());
        console.log(wavesurfer.getVolume()); 
        await Sleep(10000);
        console.log(wavesurfer.getDuration());
    }
}
</script>

<body>
    <form >
        <label for="audio" class="text-md text-gray-200 font-semibold mb-3">
            Upload file
        </label>
        <input type="file" id="audio" name="audio" accept=".wav,.mp3,.ogg" on:change={fileUploadedAndInitWave} class="block text-secondary
            file:mx-4 file:py-2 file:px-4 file:bg-secondary file:rounded-full file:border-0
            file:font-semibold file:text-secondary-content hover:file:bg-secondary-focus" />
    </form>
</body>

<div id="waveform" class="waveform"></div>
<br/>
<p>bar</p>
<div id="wave-timeline" class="wave-timeline"></div>
<div class="zoom">
    <!-- <input data-action="zoom" type="range" min="1" max="200" value="0" style="width: 100%" />    -->
    <input data-action="zoom" type="range" min="1" max="200" value="0" />
</div>
<div id="wave-spectrogram" class="wave-spectrogram"></div>
<br/> <br/>
<div class="box">
    <button id="playPause" on:click="{btnPlayPause1}">
        <span id="play" on:click={btnPlay1}>
            <i class=""></i>
            Play
        </span>

        <span id="pause" style="display: none" on:click={btnPause1}>
            <i class=""></i>
            Pause
        </span>
    </button>

    <button id="btnStop" on:click={btnStop1}>Stop</button>
</div>
