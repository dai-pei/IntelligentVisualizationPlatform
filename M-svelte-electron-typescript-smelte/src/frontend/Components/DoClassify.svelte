<script lang="ts">
    import LayoutGrid,{Cell} from '@smui/layout-grid';
    import Textfield from '@smui/textfield';
    import Checkbox from '@smui/checkbox';
    import FormField from '@smui/form-field'; 
    import HelperText from '@smui/textfield/helper-text';

    let valueTypeFiles;
    let checkedZero=false;
    let checkedCent=false;
    let checkedMfcc=false;
    
    // let textContent="";

</script>

<body>
    <LayoutGrid>
        <Cell span={6}>
            <div class="hide-file-ui">
                <Textfield bind:files={valueTypeFiles} label="File" type="file" multiple/>
            </div>
        </Cell>        
        <Cell span={6}>
            <div></div>
        </Cell>
        <Cell span={6}>
            <Textfield textarea bind:value={valueTypeFiles} label="FilePaths" invalid>
                <HelperText slot="helper">选中的音频路径</HelperText>
            </Textfield>
        </Cell>
        <Cell span={6}>
            <FormField>
                <Checkbox bind:checkedZero />
                    <span slot="label">过零率</span>    
            </FormField>
            <FormField>
                <Checkbox bind:checkedCent />
                    <span slot="label">频谱质心</span>
            </FormField>
            <FormField>
                <Checkbox bind:checkedMfcc />
                    <span slot="label">MFCC</span>
            </FormField>
        </Cell>
    </LayoutGrid>
</body>

<style>
    /* .hide-file-ui :global(input[type='file']::file-selector-button) {
        display: none;
    }
    .hide-file-ui
        :global(:not(.mdc-text-field--label-floating) input[type='file']) {
        color: transparent;
    } */
    .demo-cell {
        height: 60px;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: var(--mdc-theme-secondary, #333);
        color: var(--mdc-theme-on-secondary, #fff);
    }
</style>