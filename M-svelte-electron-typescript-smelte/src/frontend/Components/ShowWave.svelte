<script lang="ts">
    import * as d3 from "d3";
    import {
        totalDuration,
        orgData,
        filePath
    } from '../stores/status';
    import {
        onMount,
        onDestroy
    } from 'svelte';
    import {
        easeLinear
    } from "d3";

    let temporgData: any;
    let tempfilePath: any;
    let orgDataLen: number;
    let orgDataCircle: number[][] = [];
    let orgDataIdx: number[];

    let temptotalDuration: number;

    let audio: any = null;
    let paused = true;
    let duration = 0;
    let currentTime = 0;
    let muted = false;
    let volume = 1;
    let src: any;
    let preload = "metadata";

    let seeking = false;
    let volumeSeeking = false;

    let songBar: any;
    let volumeBar: any;

    filePath.subscribe(value => {
        src = value;
    })

    function seek(event: any, bounds: any) {
        let x = event.pageX - bounds.left;
        return Math.min(Math.max(x / bounds.width, 0), 1);
    }

    function seekAudio(event: any) {
        if (!songBar) return;
        audio.currentTime = seek(event, songBar.getBoundingClientRect()) * duration;
    }

    function seekVolume(event: any) {
        if (!volumeBar) return;
        volume = seek(event, volumeBar.getBoundingClientRect());
        audio.volume = volume;
        muted = false;
    }

    function formatSeconds(seconds: any) {
        if (isNaN(seconds)) return "No Data";
        var sec_num = parseInt(seconds, 10)
        var hours = Math.floor(sec_num / 3600)
        var minutes = Math.floor(sec_num / 60) % 60
        var seconds = sec_num % 60

        return [hours, minutes, seconds]
            .map(v => v < 10 ? "0" + v : v)
            .filter((v, i) => v !== "00" || i > 0)
            .join(":")
    }

    function trackMouse(event: any) {
        if (seeking) seekAudio(event);
        if (volumeSeeking) seekVolume(event);
    }

    let width: any = 600
    let height: any = 400
    var margin = {
        top: 40,
        right: 40,
        bottom: 40,
        left: 40
    };

    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0.0);

    totalDuration.subscribe(value => {
        temptotalDuration = value;
    })

    orgData.subscribe(value => {
        temporgData = value;
    });
    filePath.subscribe(value => {
        tempfilePath = value;
    });

    onMount(() => {
        requestOrgData();
    });

    function requestOrgData() {
        console.log(tempfilePath);
        fetch(`http://127.0.0.1:6005/orgdata/`, {
                method: 'post',
                body: JSON.stringify({
                    filepath: tempfilePath
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {
                return res.json().then((response) => {
                    console.log("response", response);
                    totalDuration.set(response['duration']);
                    orgData.set(response["orgdata"]);

                    initVariables();
                    drawWave();
                });
            })
            .catch((error) => {
                console.error(error);
            });
    }

    function initVariables() {
        orgDataLen = temporgData.length;
        console.log("org data len:")
        console.log(orgDataLen)

        // 由于三分多钟的歌曲渲染出来会死机出错，svg dom元素过多绘制报错，所以这里做一个插值？或者是叫做下采样的处理
        // 一分钟以内，step为1，1-2分钟，step为2，以此类推
        let step: number;
        step = Math.floor(orgDataLen / 22050 / 60) + 1;
        if (step <= 1) {
            step = 1;
        }
        if (step > 1) {
            step *= 2;
        }
        console.log("step " + String(step));

        orgDataIdx = new Array < number > (orgDataLen);
        for (var i = 0; i < orgDataLen; i = i + step) {
            orgDataIdx[i] = i;
        }
        for (var i = 0; i < orgDataLen; i = i + step) {
            let temp: any = new Array(2);
            if (temporgData[i] == null || temporgData[i] == undefined)
                temp[1] = 0;
            else
                temp[1] = temporgData[i];
            temp[0] = orgDataIdx[i];
            orgDataCircle.push(temp);
        }
    }

    function drawWave() {
        console.log("draw wave");
        d3.select("#waveplot").selectAll('*').remove();
        d3.select("#wavingline").selectAll('*').remove();

        var svg = d3.select('#waveplot')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLen + orgDataLen / 10])
            .range([0, width]);

        var yScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([0, height])

        var xAxis = d3.axisTop(xScale)
        yScale.range([height, 0]); // 重新设置y轴比例尺的值域,与原来的相反        
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + margin.bottom + ")")
            .call(xAxis);
        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + margin.bottom + ")")
            .call(yAxis);

        svg.selectAll("circle")
            .data(orgDataCircle)
            .enter()
            .append("circle")
            .attr("cx", function (d) {
                return margin.left + xScale(d[0]);
            })
            .attr("cy", function (d) {
                return yScale(d[1]) + margin.bottom;
            })
            .attr("r", 1)
            .attr("fill", "rgb(0,0,255)")
            .on("mouseover", function (event, d) {
                d3.select(this)
                    .attr("r", 5)
                    .style("fill", "green");

                tooltip.html("幅度：" + d[1])
                    .style("position", "absolute")
                    .style("left", (d3.pointer(event, this)[0]) + "px")
                    .style("top", (d3.pointer(event, this)[1] + 100) + "px")
                    .style("opacity", 1.0);
            })
            .on("mousemove", function (event, d) {
                tooltip.style("left", (d3.pointer(event, this)[0]) + "px")
                    .style("top", (d3.pointer(event, this)[1] + 100) + "px");
            })
            .on("mouseout", function (event, d) {
                tooltip.style("opacity", 0.0);
                d3.select(this)
                    .attr("r", 1)
                    .attr("fill", "rgb(0,0,255)");
            })
            //拓展：悬浮显示幅度，点击显示一个弹窗，为周边几十个采样点的放大图，稍后再做

        svg.append("line")
            .attr("id", "wavingline")
            .attr("x1", margin.left)
            .attr("y2", 20)
            .attr("x2", margin.left)
            .attr("y2", height + 20)
            .attr("stroke", "black")
            .attr("stroke-width", "4px");

        //问题在于svg画图形过程中是同步的吗？如果阻塞住了，那么不能同时画图和同时播放音乐
        // 结论：是可以的，但是画面卡顿
        // 解决方法：优化svg dom的渲染过程；增加加载中动画。但是对于1min的歌曲，加载时间会超过10s，不能接受

    };

    function play() {
        // currentTime永远小于temptotalDuration，相差的数量级在10e-4 到10e-6之间
        if(temptotalDuration-currentTime<0.0001){
            currentTime=0;
        }
        paused=false;

        console.log("function play()")
        console.log(temptotalDuration)
        console.log("currentTime")
        console.log(currentTime)

        audio.play()
        d3.select("#wavingline")
            .attr("x1", margin.left + (currentTime / temptotalDuration) * (width-width/11))
            .attr("y2", 20)
            .attr("x2", margin.left + (currentTime / temptotalDuration) * (width-width/11))
            .attr("y2", height + 20)
            .transition()
            .ease(easeLinear)
            .duration((temptotalDuration - currentTime) * 1000)
            .attr("x1", margin.left + (width-width/11))
            .attr("y2", 20)
            .attr("x2", margin.left + (width-width/11))
            .attr("y2", height + 20);

        // console.log("svg play line");
        // 一旦创建好了一个过渡效果，就不能再改变了
        // 但如果一个元素的一个属性正在进行过渡，此时又开始了这个属性的另一个过渡，则之前的过渡会被终止。
    }

    function pause() {
        console.log("function pause()")
        console.log(temptotalDuration)
        console.log("currentTime")
        console.log(currentTime)

        paused=true;
        audio.pause();
        d3.select("#wavingline")
            .transition()
            .ease(easeLinear)
            .attr("x1", margin.left + (currentTime / temptotalDuration) * (width-width/11))
            .attr("y2", 20)
            .attr("x2", margin.left + (currentTime / temptotalDuration) * (width-width/11))
            .attr("y2", height + 20);
        console.log("svg pause line");
    }
</script>

<svelte:window on:mouseup={()=> seeking = volumeSeeking = false}
    on:mousemove={trackMouse}
    />

    <body>
        <div class="playmusic">
            <audio bind:this={audio} bind:paused bind:duration bind:currentTime {muted} {volume} on:play on:ended {src}
                {preload}></audio>
            <div class="controls">
                <button class="material-icons" on:click={()=> audio.paused ? play() : pause()}>
                {#if paused}
                    play_arrow
                {:else}
                    pause
                {/if}
            </button>
            <progress
                bind:this={songBar}
                value={currentTime ? currentTime : 0}
                max={duration}
                on:mousedown={() => seeking = true}
                on:click={seekAudio}
                class="song-progress"
            ></progress>
            <div class="control-times">{formatSeconds(currentTime)}/{formatSeconds(duration)}</div>
            <button
                class="material-icons" on:click={() => muted = !muted}>
                {#if muted}
                    volume_off
                {:else if volume < .01}
                    volume_mute
                {:else if volume < .5}
                    volume_down
                {:else}
                    volume_up
                {/if}
            </button>
            <progress
                bind:this={volumeBar}
                value={volume}
                on:mousedown={() => volumeSeeking = true}
                on:click={seekVolume}
                class="volume-progress"
            ></progress>

        </div>
    </div>

    <div id="waveplot">
    </div>    
</body>

<style>
    body {
        margin: 0;
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }

    .controls {
        display: flex;
        flex-flow: row;
        justify-content: space-around;
        color: var(--color);
        background-color: var(--background-color);
        padding-left: 10px;
        padding-right: 10px;
        -webkit-user-select: none; /* Safari */
        -ms-user-select: none; /* IE 10+ and Edge */
        user-select: none; /* Standard syntax */
        padding-top: 5px;
        padding-bottom: 5px;
    }
    .control-times {
        margin: auto;
        margin-right: 5px;
    }
    .material-icons {
        font-size: 16px;
        margin-bottom: 0px;
        color: var(--icon-color);
        background-color: rgba(0,0,0,0);
        cursor: pointer;
        transition: 0.3s;
        border: none;
        border-radius:25px;
    }
    .material-icons:hover {
        box-shadow: 0px 6px  rgba(0,0,0,0.6);
    }
    .material-icons::-moz-focus-inner {
        border: 0;
    }
    progress {
		display: block;
        color: var(--primary-color);
        background: var(--secondary-color);
        border: none;
        height: 15px;
        margin: auto;
        margin-left: 5px;
        margin-right: 5px
    }
    
    progress::-webkit-progress-bar {background-color: var(--secondary-color); width: 100%}
    progress::-moz-progress-bar { background: var(--primary-color); }
    progress::-webkit-progress-value { background: var(--primary-color); }
    .song-progress {
        width: 100%;
    }
    .volume-progress {
        width: 10%;
        max-width: 100px;
        min-width: 50px;
    }
</style>