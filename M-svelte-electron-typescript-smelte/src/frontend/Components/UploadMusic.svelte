<script lang="ts">
    import Ripple from '@smui/ripple';
    import Button, {
        Label
    } from '@smui/button';
    import Textfield from '@smui/textfield';
    import {
        filePath,
        showWave
    } from "../stores/status";
    import ShowWave from './ShowWave.svelte';

    let tempshowWave: boolean=false;
    let tempfilePath: any = null;

    filePath.subscribe(value => {
        tempfilePath = value;
    });
    showWave.subscribe(value => {
        tempshowWave = value;
    })

    function setFilePaths(){
        filePath.set(tempfilePath);
        tempshowWave=!tempshowWave;
        showWave.set(tempshowWave);

        console.log(tempfilePath);
    }
</script>

<body>
    <p use:Ripple={{ surface: true, color: 'primary' }} tabindex="0">
        准备好全新的体验吧，您将学习到如何进行音乐转录<br>
        先从选择一首歌开始吧
    </p>

    <div class="hide-file-ui">
        <Textfield bind:files={tempfilePath} label="File" type="file" />
    </div>

    <Button on:click={setFilePaths}>
        <Label>展示波形</Label>
    </Button>
    {#if tempshowWave}
        <ShowWave/>
    {/if}
</body>

<style>
    p {
        padding: 10px;
        border-radius: 5px;
    }

    [tabindex='0'] {
        cursor: pointer;
    }
   
    .hide-file-ui :global(input[type='file']::file-selector-button) {
        display: none;
    }
    .hide-file-ui
        :global(:not(.mdc-text-field--label-floating) input[type='file']) {
        color: transparent;
    }
</style>