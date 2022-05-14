<script lang="ts">
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
    console.log(file.name)
}
</script>

<section class="w-full flex flex-col items-center justify-center gap-8">
    <form class="w-full flex flex-col md:flex-row items-center justify-center gap-7 mt-10 p-2">
        <div class="flex flex-col items-center gap-7" >
            <label for="audio" class="text-md text-gray-200 font-semibold mb-3">
                Upload file
            </label>
            <input type="file" id="audio" name="audio" accept=".wav,.mp3,.ogg" on:change={handleFileUploaded} class="block text-secondary
                file:mx-4 file:py-2 file:px-4 file:bg-secondary file:rounded-full file:border-0
                file:font-semibold file:text-secondary-content hover:file:bg-secondary-focus" />
        </div>
    </form>
</section>

  <style>
.recorder {
    width: var(--recorder-width);
}
</style>
