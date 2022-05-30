<script lang="ts">
    import Drawer, {
        AppContent,
        Content
    } from '@smui/drawer';
    import List, {
        Item,
        Text
    } from '@smui/list';
    import LinearAndLogSpectrum from './features/LinearAndLogSpectrum.svelte';
    import SpectrumCentroid from './features/SpectrumCentroid.svelte';
    import ZeroCrossingRate from './features/ZeroCrossingRate.svelte';

    let showFeatureIdx = 0;
    // showFeatureIdx值对应关系：
    // 0：不展示内容
    // 1：过零率
    // 2：线性频谱图
    // 3：频谱质心
</script>

<body>
    <div class="drawer-container">
        <Drawer>
            <Content>
                <List>
                    <Item href="javascript:void(0)" on:click={()=> (showFeatureIdx=1)}
                        >
                        <Text>过零率</Text>
                    </Item>
                    <Item href="javascript:void(0)" on:click={()=> (showFeatureIdx=2)}
                        >
                        <Text>线性和对数频谱图</Text>
                    </Item>
                    <Item href="javascript:void(0)" on:click={()=> (showFeatureIdx=3)}
                        >
                        <Text>频谱质心</Text>
                    </Item>
                </List>
            </Content>
        </Drawer>

        <AppContent class="app-content">
            <main class="main-content">
                <!-- <pre class="status">Clicked: {clicked}</pre> -->
                {#if showFeatureIdx==1}
                    <ZeroCrossingRate/>
                {:else if showFeatureIdx==2}
                    <LinearAndLogSpectrum/>
                {:else if showFeatureIdx==3}
                    <SpectrumCentroid/>
                {/if}
            </main>
        </AppContent>
    </div>
</body>

<style>
    /* These classes are only needed because the
      drawer is in a container on the page. */
    .drawer-container {
        position: relative;
        display: flex;
        height: 350px;
        max-width: 600px;
        border: 1px solid var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.1));
        overflow: hidden;
        z-index: 0;
    }

    * :global(.app-content) {
        flex: auto;
        overflow: auto;
        position: relative;
        flex-grow: 1;
    }

    .main-content {
        overflow: auto;
        padding: 16px;
        height: 100%;
        box-sizing: border-box;
    }
</style>