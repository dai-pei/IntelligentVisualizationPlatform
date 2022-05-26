<style>
main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
}

h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
}

@media (min-width: 640px) {
    main {
        max-width: none;
    }
}
</style>

<script lang="ts">
export let name: string;
import "smelte/src/tailwind.css";
// import Player from "./components/Player.svelte";
import PlayerWave from "./components/PlayerWave.svelte";
import TestD3 from "./components/TestD3.svelte";
import Test from "./components/TestD3.svelte";
import TestDuration from "./components/TestDuration.svelte";
import TestKnn from "./components/TestKNN.svelte";
import TestNet from "./components/TestNet.svelte";
import TestSpecCent from "./components/TestSpecCent.svelte";
import TestSpectrum from "./components/TestSpectrum.svelte";
import TestTransmition from "./components/TestTransmition.svelte";
import TestWave from "./components/TestWave.svelte";
import TestZero from "./components/TestZero.svelte";
import UploadMusic from "./components/UploadMusic.svelte";
// import {CurrentSongPath} from './stores/status'
// let count_value:any;
// CurrentSongPath.subscribe(value => {
// 		count_value = value;
// 	})
</script>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
<main>
    <!-- <h1>test hello</h1>
    <h1>Hello {name}!</h1> -->
    <!-- <UploadMusic/> -->
    <!-- <Test></Test> -->
    <!-- <PlayerWave/> -->
    <!-- <p>{count_value}</p> -->
    <!-- <TestNet/> -->
    <!-- <TestSpectrum/> -->
    <!-- <TestTransmition/> -->
    <TestDuration/>
    <p>
        ------------------------------------------<br><br>
    </p>
    <!-- <TestWave/> -->
    <!-- <TestZero/> -->
    <!-- <TestSpecCent/> -->
    <TestKnn/>

</main>
