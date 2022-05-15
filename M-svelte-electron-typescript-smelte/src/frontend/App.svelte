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
import Test from "./Components/Test.svelte";
import UploadMusic from "./Components/UploadMusic.svelte";
</script>

<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
<main>
    <h1>Hello {name}!</h1>
    <Test></Test>
</main>
