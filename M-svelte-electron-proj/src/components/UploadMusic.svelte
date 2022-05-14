<form class="w-full flex flex-col md:flex-row items-center justify-center gap-7 mt-10 p-2">
    <div class="flex flex-col items-center gap-7" bind:clientWidth={uploadWidth}>
        <label for="audio" class="text-md text-gray-200 font-semibold mb-3">
            Upload file
        </label>
        <input type="file" id="audio" name="audio" accept=".wav,.mp3,.ogg" on:change={handleFileUploaded} class="block text-secondary
               file:mx-4 file:py-2 file:px-4 file:bg-secondary file:rounded-full file:border-0
               file:font-semibold file:text-secondary-content hover:file:bg-secondary-focus" />
    </div>

    {#if canRecord()}
      {#await navigator.mediaDevices.getUserMedia({ audio: true }) then stream}
        <p class="text-xl font-bold text-secondary my-8">OR</p>
        <div
          class="flex items-center justify-center recorder"
          style:--recorder-width={`${uploadWidth}px`}
        >
          <div class="flex flex-col items-center gap-7">
            <AudioRecorder
              audiosStream={stream}
              onUploadRecording={(file) => {
                requestAudioProcessing(file);
              }}
            />
          </div>
        </div>
      {/await}
    {/if}
  </form>