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

    let color = 'default';
    let openWaveDialog=false;
    let openAmpDialog=false;
    let openFreqDialog=false;
    let openTimbreDialog=false;

    let response = 'Nothing yet.';
    function closeHandler(e: CustomEvent<{ action: string }>) {
        switch (e.detail.action) {
        case 'none':
            response = "Ok, well, you're wrong.";
            break;
        case 'all':
            response = 'You are correct. All dogs are the best dog.';
            break;
        default:
            // This means the user clicked the scrim or pressed Esc to close the dialog.
            // The actions will be "close".
            response = "It's a simple question. You should be able to answer it.";
            break;
        }
    }
</script>

<body>
    <div class="paper-container">
        <Paper transition elevation={24} {color}>
            <Title>声音</Title>
            <Content>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-right: 30px; width: max-content; display: block;">
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
                            <span slot="label" style="padding-right: 30px; width: max-content; display: block;">
                                三要素：响度
                            </span>
                            <Button on:click={() => (openAmpDialog = true)}>
                                <Label>查看响度</Label>
                            </Button>
                        </FormField>
                    </div>
                </Paper>
                <br><br>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-right: 30px; width: max-content; display: block;">
                                三要素：频率
                            </span>
                            <Button on:click={() => (openFreqDialog = true)}>
                                <Label>查看频率</Label>
                            </Button>
                        </FormField>
                    </div>
                </Paper>
                <br><br>
                <Paper>
                    <div>
                        <FormField align="end" style="display: flex;">
                            <span slot="label" style="padding-right: 30px; width: max-content; display: block;">
                                三要素：音色
                            </span>
                            <Button on:click={() => (openTimbreDialog = true)}>
                                <Label>查看音波图</Label>
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
        <Actions>
            <Button action="none">
            <Label>None of Them</Label>
            </Button>
            <Button action="all" default>
            <Label>All of Them</Label>
            </Button>
        </Actions>
    </Dialog>
</body>

<style>
    .paper-container {
        width: 60%
    }
</style>