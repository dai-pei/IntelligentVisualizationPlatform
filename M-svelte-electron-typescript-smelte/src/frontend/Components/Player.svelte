<script>
    import PlayerSeekBar from './PlayerSeekbar.svelte';
</script>

<style>
    #waveform {
        position: absolute;
        top: 20;
        bottom: 0;
        left: 0;
        right: 0;
    }
</style>


<div class="site-player" id='waveform'>
    <PlayerSeekBar />
</div>