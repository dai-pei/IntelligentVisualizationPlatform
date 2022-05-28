<!-- <script>
    import {filePath} from "../stores/status";
    let musicPath="";
    filePath.subscribe((value)=>{
        musicPath=value;
    });
</script>

<body>
    <audio src={musicPath} id="currentMusic"></audio>

</body> -->

<style>
    body {
        margin: 0;
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
    }
</style>
<body>

</body>

<script lang="ts">
    import * as d3 from "d3"
    var start = [0, 0];
    var end = [100, 20];

    var length = Math.sqrt(Math.pow(start[0] - end[0], 2) +
        Math.pow(start[1] - end[1], 2));

    var dirUnitVector = [
        (end[0] - start[0]) / length,
        (end[1] - start[1]) / length
    ];

    var svg = d3.select("body").append("svg")
        .attr("width", 300)
        .attr("height", 200)
        .attr('viewBox', '-10 0 120 20')
        .style('stroke', "black");

    svg.append('line')
        .attr('x1', start[0])
        .attr('y1', start[1])
        .attr('x2', end[0])
        .attr('y2', end[1]);

    var c = svg.append('circle')
        .attr('cx', start[0])
        .attr('cy', start[1])
        .attr('r', 2)
        .style('fill', 'blue')
        .call(d3.drag().on("drag", function (event,d) {
            var mouseVector = [
                d3.pointer(event)[0] - start[0],
                d3.pointer(event)[1] - start[1],
            ];
            var projection =
                mouseVector[0] * dirUnitVector[0] +
                mouseVector[1] * dirUnitVector[1];
            c.attr('cx', start[0] + dirUnitVector[0] * projection);
            c.attr('cy', start[1] + dirUnitVector[1] * projection);
        }));
</script>