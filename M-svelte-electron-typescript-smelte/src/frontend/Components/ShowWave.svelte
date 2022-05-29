<script lang="ts">
    import * as d3 from "d3";
    import {onMount} from "svelte";
    import {totalDuration,orgData, filePath} from '../stores/status';

    let temporgData:any;
    let tempfilePath:any;
    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    let temptotalDuration:number;

    let width:any=600
    let height:any=600 
    var margin = { top: 40, right: 40, bottom: 40, left: 40 };

    totalDuration.subscribe(value=>{
        temptotalDuration=value;
    })

    orgData.subscribe(value=>{
        temporgData=value;
    });
    filePath.subscribe(value=>{
        tempfilePath=value;
    });

    onMount(()=>{
        requestOrgData();
    });
    
    function requestOrgData(){
        console.log(tempfilePath);
        fetch(`http://127.0.0.1:6005/orgdata/`, {
            method: 'post',
            body:JSON.stringify({filepath:tempfilePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log("response",response);
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

    function initVariables(){
        orgDataLen=temporgData.length;
        console.log("org data len:")
        console.log(orgDataLen)

        // 由于三分多钟的歌曲渲染出来会死机出错，svg dom元素过多绘制报错，所以这里做一个减半的处理
        let step:number;
        step=Math.floor(orgDataLen/22050/60)+1;
        if(step==0){
            step=1;
        }
        console.log("step "+String(step));

        orgDataIdx=new Array<number>(orgDataLen);
        for(var i=0;i<orgDataLen;i=i+step)
        {   
            orgDataIdx[i]=i;
        }
        for(var i=0;i<orgDataLen;i=i+step)
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

    function drawWave(){
        console.log("draw wave");
        d3.select("#waveplot").selectAll('*').remove();

        var svg = d3.select('#waveplot')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

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

        svg.append("line")
            .attr("x1", margin.left)
            .attr("y2", 20)
            .attr("x2", margin.left)
            .attr("y2", height+20)
            .attr("stroke", "black")
            .attr("stroke-width", "8px")
            .transition()
            .duration(temptotalDuration*1000)
            .attr("x1", margin.left+900)
            .attr("y2", 20)
            .attr("x2", margin.left+900)
            .attr("y2", height+20);
    };


</script>

<body>
    <div>
        <p>
            the player buttons...
        </p>
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
</style>