<script lang='ts'>
    import * as d3 from 'd3';
    import {
        filePath
    } from '../../stores/status';
    import {
        onMount
    } from 'svelte';
    import Ripple from '@smui/ripple';
    let orgData: number[] | undefined | null;
    let orgDataLenFreq: number | undefined | null;
    let orgDataLenTime: number | undefined | null;
    let orgDataIdx: number[] | undefined | null;
    let orgDataCircle: number[][][] = [];

    var compute = d3.interpolate("purple", "yellow");
    let maxAmp: any = -100;
    let minAmp: any = 100;

    let linear: any;

    var width = 600;
    var height = 400;
    var margin = {
        top: 40,
        right: 40,
        bottom: 40,
        left: 40
    };

    onMount(() => {
        requestSpectrum();
    });

    function requestSpectrum() {
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/spectrum/`, {
                method: 'post',
                body: JSON.stringify({
                    filepath: $filePath
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then((res) => {
                return res.json().then((response) => {
                    console.log(response["loaddata"]);
                    orgData = response["loaddata"];
                    orgDataLenFreq = orgData.length; //1024
                    orgDataLenTime = orgData[0].length; //625

                    orgDataIdx = new Array < number > (orgDataLenTime);
                    for (var i = 0; i < orgDataLenTime; i++) {
                        orgDataIdx[i] = i;
                    }

                    initVariables();
                    drawSVG();
                });
            })
            .catch((error) => {
                console.error(error);
            });
    }

    function initVariables() {
        console.log(orgDataLenFreq, orgDataLenTime);
        for (var i = 0; i < orgDataLenTime; i++) {
            for (var j = 0; j < orgDataLenFreq; j++) {
                let temp: any = new Array(3);
                temp[0] = i;
                temp[1] = j*1024;
                // console.log(i,j)
                let num: number | undefined | null = orgData[j][i];
                if (num == undefined)
                    temp[2] = 0;
                else
                    temp[2] = Math.abs(num);
                if (num > maxAmp)
                    maxAmp = num
                if (num < minAmp)
                    minAmp = num
                orgDataCircle.push(temp);
            }

        }
        // console.log(orgDataCircle.length,orgDataCircle[0].length)
        linear = d3.scaleLinear().domain([0, maxAmp]).range([0, 1])
    }

    function drawSVG() {
        var svg = d3.select('#spectrum')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLenTime])
            .range([0, width]);
        var yScale = d3.scaleLinear()
            .domain([0, orgDataLenFreq])
            .range([height, 0]);

        var xAxis = d3.axisTop(xScale);
        yScale.range([height, 0]);
        var yAxis = d3.axisLeft(yScale);

        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + margin.bottom+height + ")")
            .call(xAxis);

        svg.append("g").attr("class", "axis")
            .attr("transform", "translate(" + margin.left + "," + margin.bottom + ")")
            .call(yAxis);

        svg.selectAll("rect")
            .data(orgDataCircle)
            .enter()
            .append("rect")
            .attr("x", function (d) {
                return margin.left + xScale(d[0]);
            })
            .attr("y", function (d) {
                return yScale(d[1]) + margin.bottom;
            })
            .attr('width', 5)
            .attr('height', 5)
            .style("fill", function (d) {
                return compute(linear(d[2]));
            })
            .on("mouseover", function (event, d) {
                d3.select(this)
                .attr("r", 10)
                .style("fill", "black");

                tooltip.html("频率：" + d[1] + ",幅度：" + d[2])
                .style("position", "absolute")
                .style("left", (d3.pointer(event, this)[0]) + "px")
                .style("top", (d3.pointer(event, this)[1] + width/10) + "px")
                .style("opacity", 1.0);
            })
            .on("mousemove", function (event, d) {
                tooltip.style("left", (d3.pointer(event, this)[0]) + "px")
                .style("top", (d3.pointer(event, this)[1] + width/10) + "px");
            })
            .on("mouseout", function (event, d) {
                d3.select(this)
                .attr("r", 5)
                .style("fill", compute(linear(d[2])));
                tooltip.style("opacity", 0.0);
            });
            
    }
    
    var tooltip = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0.0);
</script>

<body>    
    <p use:Ripple={{ surface: true, color: 'primary' }} tabindex="0">
        频谱其实是一个幅度谱，表示信号在各个频率分量上的幅度值
    </p>
    <div id="spectrum"></div>
</body>