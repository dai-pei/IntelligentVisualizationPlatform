<script>
    import { onMount } from 'svelte';
    import { MediaPlayer } from "../stores/waveplayer";
    import { formatSongLength } from "../logic/helper";

    let seekWidth;
    let currentTime;
    let mouseDown = false;
    let progressSlider;

    function updateProgress() {
        seekWidth = ($MediaPlayer.wavesurfer) ? ($MediaPlayer.wavesurfer.getCurrentTime()/$MediaPlayer.wavesurfer.getDuration())*100 : 0;
        currentTime = ($MediaPlayer.wavesurfer) ? $MediaPlayer.wavesurfer.getCurrentTime() : 0;

        requestAnimationFrame(updateProgress);
    }

    function handleSeekMouseDown(event) {
        mouseDown = true;
        document.addEventListener('mouseup', handleSeekMouseUp);
    }

    function handleSeekMouseUp(event) {
        mouseDown = false;
        document.removeEventListener('mouseup', handleSeekMouseUp);
        progressSlider.classList.remove("dragging");
    }

    function handleSeekDrag(event) {
        if (mouseDown) {
            progressSlider.classList.add("dragging");
            requestAnimationFrame(function() {
                handleSeek(event);
            });
        }
    }

    function handleSeek(event) {
        let seekElementWidth = event.target.offsetWidth;
        let seekClickLocation = event.clientX - event.target.getBoundingClientRect().left;

        if ($MediaPlayer.wavesurfer) {
            let seekFraction = seekClickLocation / seekElementWidth;
            $MediaPlayer.wavesurfer.seekTo(seekFraction);
        }
    }

    function startPlay(){
        console.log("player seekbar start play")
        $MediaPlayer.start();
    }

    onMount(() => {
        progressSlider = document.querySelector(".site-player__seekBar");
        requestAnimationFrame(updateProgress);
    });
</script>

<div>
    <button on:click={$MediaPlayer.playPause()}>
        play
    </button>
</div>
<div on:click={handleSeek} on:mousedown={handleSeekMouseDown} on:mousemove={handleSeekDrag}>
    <span class="site-player__progress" data-value="{formatSongLength(currentTime)}" style="transform: translateX({seekWidth}vw)"></span>
</div>

<style>
</style>