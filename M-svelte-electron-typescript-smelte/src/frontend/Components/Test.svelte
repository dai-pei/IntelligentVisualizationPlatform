<script lang="ts">
import {
    onMount
} from 'svelte';
import * as d3 from "d3"

let el:any;

onMount(() => {

    var p = d3.select(el)
        .selectAll("p");

    p.text("Hello World");
    //修改段落的颜色和字体大小
    p.style("color", "red")
        .style("font-size", "72px");
});
</script>

<section class="w-full flex flex-col items-center justify-center gap-8">
    <body bind:this={el}>
        <p >testtstdaafdasfdaf</p>
        <p>1111111111111</p>
    </body>

</section>

<style>
.recorder {
    width: var(--recorder-width);
}
</style>
