<script lang="ts">
import {CurrentSongPath} from '../stores/status.ts';
import { onMount } from 'svelte';
import * as d3 from "d3"


let el: any;

onMount(() => {

    var p = d3.select(el)
        .selectAll("p");

    p.text("Hello World");
    //修改段落的颜色和字体大小
    p.style("color", "red")
        .style("font-size", "72px");
});

function handleFileUploaded(e: Event) {
        const target = e.target as HTMLInputElement;
        const files = target.files;
        if (!files) {
            return;
        }

        const file = files[0];
        if (!file) {
            return;
        }

        CurrentSongPath.set(file.name)
        console.log(file.name)
    }

</script>

<section class="w-full flex flex-col items-center justify-center gap-8">
    <body bind:this={el}>
        <form >
            <label for="audio" class="text-md text-gray-200 font-semibold mb-3">
                Upload file
            </label>
            <input type="file" id="audio" name="audio" accept=".wav,.mp3,.ogg" on:change={handleFileUploaded} class="block text-secondary
                file:mx-4 file:py-2 file:px-4 file:bg-secondary file:rounded-full file:border-0
                file:font-semibold file:text-secondary-content hover:file:bg-secondary-focus" />
        </form>
    </body>

</section>

<style>
.recorder {
    width: var(--recorder-width);
}
</style>
