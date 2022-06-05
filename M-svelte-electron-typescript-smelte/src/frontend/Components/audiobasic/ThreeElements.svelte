<script lang='ts'>
    import * as d3 from "d3";
    import Ripple from '@smui/ripple';
    import Textfield from '@smui/textfield';
    import HelperText from '@smui/textfield/helper-text';
    import LayoutGrid, {
        Cell
    } from '@smui/layout-grid';
    import Button, {
        Label
    } from '@smui/button';

    let valueAmp: number = -1;
    let valueFreq: number = -1;
    $: valueOmega = valueFreq * 2 *3.1415926;
    let valuePhase: number = -1;

    let sampleRate: number = 22050
    let totalSeconds: number = 2
    $: sampleNumber = sampleRate * totalSeconds;

    let sinWave: any[] = [];
    let audio: any = null;
    let src: any;
    let preload = "metadata";
    let paused = true;
    let duration = 0;
    let currentTime = 0;
    let muted = false;
    let volume = 1;

    let width: number = 400
    let height: number = 200
    var margin = {
        top: 40,
        right: 40,
        bottom: 40,
        left: 40
    };

    function generateSinWave() {
        sinWave=[]
        for (var i = 0; i < sampleNumber; i++) {
            var tempArr=new Array()
            tempArr.push(i)
            tempArr.push(valueAmp * Math.sin(valueOmega * (i%sampleRate)/sampleRate + valuePhase))
            sinWave.push(tempArr);
        }
        drawSinWave();
        generateAudio();
    }

    function generateAudio(){
        fetch(`http://127.0.0.1:6005/generateaudiofromsamples/`, {
        method: "post",
        body: JSON.stringify({
            wavedata:sinWave,
            samplerate:sampleRate
        }),
        headers: {
            "Content-Type": "application/json",
        },
        }).then((res) => {
            return res.json().then((response) => {
            // console.log(response);
            src = response["path"];      
            if(src!=''|| src!=null){
                console.log("src set");
                console.log(src)      
            }

            });
        })
        .catch((error) => {
            console.error(error);
        });
    }

    function drawSinWave() {
        d3.select('#sinwave').selectAll('*').remove();
        d3.select("g").selectAll('*').remove();

        var svg = d3.select('#sinwave')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, sampleNumber])
            .range([0, width]);

        var yScale = d3.scaleLinear()
            .domain([-valueAmp,valueAmp])
            .range([0, height])

        var xAxis = d3.axisTop(xScale)
        yScale.range([height, 0]);     
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + (margin.bottom + height) + ")")
            .call(xAxis);
        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + margin.bottom + ")")
            .call(yAxis);

        svg.selectAll("circle")
            .data(sinWave)
            .enter()
            .append("circle")
            .attr("cx", function (d) {
                return margin.left + xScale(d[0]);
            })
            .attr("cy", function (d) {
                return yScale(d[1]) + margin.bottom;
            })
            .attr("r", 0.1)
            .attr("fill","red");
    }
</script>

<body>
    <div>
        <audio bind:this={audio} bind:paused bind:duration bind:currentTime {muted} {volume} {src} 
        on:play on:ended {preload} crossOrigin="anonymous"></audio>
    </div>
    <LayoutGrid>
        <Cell span={12}>
            <div class="demo-cell">
                <p use:Ripple={{ surface: true, color: 'primary' }} tabindex="0">
                    单一频率的声音——固定形状的正弦波;<br>
                    sin_wave=A*sin(w*t+p)<br>
                    A：振幅<br>
                    f：频率<br>
                    w：角频率，w=2*pi*f<br>
                    p：相位<br>
                </p>
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Textfield variant="outlined" bind:value={valueAmp} label="振幅">
                    <HelperText slot="helper">代表响度</HelperText>
                </Textfield>
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Textfield variant="outlined" bind:value={valueFreq} label="频率">
                    <HelperText slot="helper">周期为频率的倒数</HelperText>
                </Textfield>
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Textfield disabled variant="outlined" bind:value={valueOmega} label="角频率">
                    <HelperText slot="helper">角频率=2*频率*PI</HelperText>
                </Textfield>
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Textfield variant="outlined" bind:value={valuePhase} label="相位">
                    <HelperText slot="helper">代表偏移量</HelperText>
                </Textfield>
            </div>
        </Cell>
        <Cell span={6}>
            <div class="demo-cell">
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Button on:click={generateSinWave}>
                    <Label>生成正弦波</Label>
                </Button>
            </div>
        </Cell>
        <Cell span={3}>
            <div class="demo-cell">
                <Button on:click={()=> audio.paused ? audio.play() : audio.pause() }>
                    {#if paused}
                        <Label>播放正弦波</Label>
                    {:else}                    
                        <Label>暂停播放</Label>
                    {/if}
                </Button>
            </div>
        </Cell>
        <Cell span={12}>
            <div id="sinwave" />
        </Cell>
    </LayoutGrid>
</body>