<script lang='ts'>
    import * as d3 from 'd3';
    import {filePath,orgData,orgDataCircle,orgDataIdx,orgDataLen} from '../stores/status'

    function printfile(){
            $: if ( $filePath.length != 0) {
            console.log($filePath);
        }
    }


    // let startSecond:number|null|undefined=-1;
    // let endSecond:number|null|undefined=-1;

    // let totalDuration:number|null=0;

    // function handleFileUploaded(e:Event){
    //     const target = e.target as HTMLInputElement;
    //     const files = target.files;
    //     if (!files) {
    //         console.log(1);
    //         return;
    //     }

    //     const file = files[0];
    //     if (!file) {
    //         console.log(2);
    //         return;
    //     }

    //     filePath=file.path
    //     console.log(filePath)
    // }

    // async function requestDuration() {
    //     console.log(startSecond);
    //     console.log(endSecond);
    //     fetch(`http://127.0.0.1:6005/duration/`, {
    //         method: 'post',
    //         body:JSON.stringify({filepath:filePath}),
    //         headers: {
    //             'Content-Type': 'application/json'
    //         }
    //     }).then((res) => {
    //         return res.json().then((response) => {
    //             totalDuration=response["duration"];
    //             console.log(totalDuration);                
    //     });
    //   })
    //   .catch((error) => {
    //     console.error(error);
    //   });
    // }  

    // function drawSVG(){
    //     var _width = 1500, height = 800;
    //     var margin = { top: 40, right: 40, bottom: 800, left: 40 };

    //     var width = _width - margin.left - margin.right;
    //     var height = width;

    //     var svg = d3.select('#mychart')
    //         .append('svg')
    //         .attr('width', width + margin.left + margin.right)
    //         .attr('height', height + margin.top + margin.bottom);


    //     var yScale = d3.scaleLinear()
    //         .domain([-1, 1])
    //         .range([0, 500])

    //     var xScale = d3.scaleLinear()
    //         .domain([-1000, orgDataLen+1000])
    //         .range([0, 800]);



    //     var xAxis = d3.axisTop(xScale)
        
    //     // yScale.range([1, 0]);  // 重新设置y轴比例尺的值域,与原来的相反
        
    //     var yAxis = d3.axisLeft(yScale)


    //     svg.append("g").attr("class", "axis")
    //             .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom) +")")
    //             .call(xAxis);

    //     svg.append("g").attr("class", "axis")
    //             .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom - 1) +")")
    //             .call(yAxis);


    //     svg.selectAll("circle")  
    //         .data(orgDataCircle)
    //         .enter()
    //         .append("circle")
    //         .attr("cx", function(d) {
    //                 return margin.left + xScale(d[0]);
    //         })
    //         .attr("cy", function(d) {
    //                 return  yScale(d[1])+ (height - margin.bottom - 1)
    //         })
    //         .attr("r", 5)
    //         .attr("fill", "rgb(0,0,255)")
    //         .on("mousedown", function(d,i){
    //             console.log("这里是添加交互的内容");
    //             d3.select(this)
    //                 .style("fill", "black");
    //                 d3.select(this) //在传给任何D3方法的匿名函数中，如果想操作当前元素，只要引用this就行
    //          });
    // }

</script>

<body>
    <button on:click={printfile}>
        btn
    </button>
    <!-- <input type = "file" on:change = {handleFileUploaded}/> 
    <button on:click = {requestDuration} > durationBtn </button>
    <span>Current Duration: {totalDuration}</span>
    <form name =“test”>
        <label >startSecond:</label>
        <input type = "text" bind:value={startSecond}>
        <label >endSecond:</label>
        <input type = "text" bind:value={endSecond}>    
    </form>
    <button on:click = {getWave} > waveBtn </button>
    <div id="mychart"></div> -->
</body>