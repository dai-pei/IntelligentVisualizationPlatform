<script lang="ts">
    // import * as http from 'http';

    let filePath: string | null | undefined = "";

    async function requestNet() {
        console.log(filePath);
        const res = await fetch(`http://127.0.0.1:6005/`);
	    let photos:string = await res.json();
        console.log(photos)
    }
  
// import { onMount } from 'svelte';

// let photos = [];

// onMount(async () => {
// 	const res = await fetch(`https://jsonplaceholder.typicode.com/photos?_limit=20`);
// 	photos = await res.json();
// });
</script>

<input type = "file" bind:value = {filePath}/> 
<button on:click = {requestNet} > 请求网络 </button>