<script lang="ts">
    import Paper, {
        Title,
        Content
    } from '@smui/paper';
    import FormField from '@smui/form-field';
    import Button, {
        Label
    } from '@smui/button';
    import Dialog, {Actions } from '@smui/dialog';
    import SinWave from './audiobasic/SinWave.svelte';
    import ThreeElements from './audiobasic/ThreeElements.svelte';
    
    
    let color = 'default';
    let openWaveDialog=false;
    let openThreeElemDialog=false;
    let openCompoundToneDialog=false;

    function closeHandler(e: CustomEvent<{ action: string }>) {
        console.log("close handler function");
    }
</script>

<body>
    <div class="paper-container">
        <Paper transition elevation={24} {color}>
            <Title>声音是什么？</Title>
            <Content>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-left: 50px; width: max-content; display: block;">
                                本质：一种波
                            </span>
                            <Button on:click={() => (openWaveDialog = true)}>
                                <Label>查看音波图</Label>
                            </Button>
                        </FormField>
                    </div>
                </Paper>
                <br><br>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-left: 50px; width: max-content; display: block;">
                                三要素：响度、频率、音色
                            </span>
                            <Button on:click={() => (openThreeElemDialog = true)}>
                                <Label>查看三要素</Label>
                            </Button>
                        </FormField>
                    </div>
                </Paper>
                <br><br>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-left: 50px; width: max-content; display: block;">
                                正弦波的叠加——复合音<br>
                                复合音的分解——正弦波
                            </span>
                            <Button on:click={() => (openCompoundToneDialog = true)}>
                                <Label>查看频率</Label>
                            </Button>
                        </FormField>
                    </div>
                </Paper>
                
            </Content>
        </Paper>
    </div>

    <Dialog bind:open={openWaveDialog}  
        fullscreen
        aria-labelledby="fullscreen-title"
        aria-describedby="fullscreen-content"
        on:SMUIDialog:closed={closeHandler}
        >
        <!-- <Title id="event-title">The Best Dog</Title> -->
        <Content id="event-content">
            <SinWave/>
        </Content>
        <!-- <Actions>
            <Button action="none">
            <Label>None of Them</Label>
            </Button>
            <Button action="all" default>
            <Label>All of Them</Label>
            </Button>
        </Actions> -->
    </Dialog>
    <Dialog bind:open={openThreeElemDialog}  
        fullscreen
        aria-labelledby="fullscreen-title"
        aria-describedby="fullscreen-content"
        on:SMUIDialog:closed={closeHandler}
        >
        <Content id="event-content">
            <ThreeElements/>
        </Content>
    </Dialog>
    <Dialog bind:open={openCompoundToneDialog}  
        fullscreen
        aria-labelledby="fullscreen-title"
        aria-describedby="fullscreen-content"
        on:SMUIDialog:closed={closeHandler}
        >
        <Content id="event-content">
            <SinWave/>
        </Content>
    </Dialog>
</body>

<style>
    .paper-container {
        width: 60%
    }
</style>