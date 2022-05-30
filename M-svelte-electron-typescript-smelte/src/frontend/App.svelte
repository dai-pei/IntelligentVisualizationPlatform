<style>
main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
}

@media (min-width: 640px) {
    main {
        max-width: none;
    }
}
</style>

<script lang="ts">
import Overview from "./components/Overview.svelte";
</script>

<main>
    <Overview/>
</main>
