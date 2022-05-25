<script lang='ts'>
    import * as d3 from 'd3';
    import {totalDuration,orgData} from '../stores/status';
    let temporgData:any;

    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    let width:number=1000
    let height:number=1000 
    var margin = { top: 40, right: 40, bottom: 40, left: 40 };

    orgData.subscribe(value=>{
        temporgData=value;
    })

    function initVariables(){
        // console.log("temp org data in testwave");
        // console.log(temporgData);
        orgDataLen=temporgData.length;
        console.log("org data len:")
        console.log(orgDataLen)
        orgDataIdx=new Array<number>(orgDataLen);
        for(var i=0;i<orgDataLen;i++)
        {   
            orgDataIdx[i]=i;
        }
        for(var i=0;i<orgDataLen;i++)
        {   
            let temp:any=new Array(2);
            if(temporgData[i]==null || temporgData[i]==undefined)
                temp[1]=0;
            else
                temp[1]=temporgData[i];
            temp[0]=orgDataIdx[i];
            orgDataCircle.push(temp);
        }                  
    }

    function drawWaveplot(){
        initVariables()
        
        d3.select('#waveplot').selectAll('*').remove();
        d3.select("g").selectAll('*').remove();

        var svg = d3.select('#waveplot')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);
            
        // svg.selectAll("*").remove();

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLen+orgDataLen/10])
            .range([0, 800]);

        var yScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([0, 500])

        var xAxis = d3.axisTop(xScale)
        yScale.range([500, 0]);  // 重新设置y轴比例尺的值域,与原来的相反        
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ margin.bottom +")")
                .call(xAxis);
        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ margin.bottom +")")
                .call(yAxis);

        svg.selectAll("circle")  
            .data(orgDataCircle)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                    return margin.left + xScale(d[0]);
            })
            .attr("cy", function(d) {
                    return  yScale(d[1]) + margin.bottom;
            })
            .attr("r", 1)
            .attr("fill", "rgb(0,0,255)");
            // .on("mousedown", function(d,i){
            //     console.log("这里是添加交互的内容");
            //     d3.select(this)
            //         .style("fill", "black");
            //         d3.select(this) //在传给任何D3方法的匿名函数中，如果想操作当前元素，只要引用this就行
            //  });
    }
</script>

<body>
    <form>
        <span>
            svgWidth:
        </span>
        <input type="text" bind:value={width}/>
        <span>
            svgHeight:
        </span>
        <input type="text" bind:value={height}/>
    </form>
    <button on:click = {drawWaveplot} > load wave </button>    
    <div id="waveplot"></div>
</body>