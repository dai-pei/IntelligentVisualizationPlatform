<script lang='ts'>
    import * as d3 from 'd3';
    import {
        filePath
    } from '../../stores/status';
    import {
        onMount
    } from 'svelte';
    let orgData: number[] | undefined | null;
    let orgDataLenFreq: number | undefined | null;
    let orgDataLenTime: number | undefined | null;
    let orgDataIdx: number[] | undefined | null;
    let orgDataCircle: number[][][] = [];

    var compute = d3.interpolate("red", "yellow");
    let maxAmp: number = -100;
    let minAmp: number = 100;

    let linear: any;

    var width = 1000;
    var height = 600;
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
                temp[1] = j;
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
            });
    }
</script>

<body>
    <div id="spectrum"></div>
</body>