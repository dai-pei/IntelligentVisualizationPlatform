<script lang='ts'>
    import * as d3 from 'd3';
    import {filePath} from '../../stores/status';
    import { onMount } from 'svelte';
    let tempfilePath:any;

    let orgDatazcrs:any;
    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    let orgDataZeroMax:any;

    let width:number=1000
    let height:number=600 
    var margin = { top: 40, right: 40, bottom: 40, left: 40 };

    filePath.subscribe(value=>{
        tempfilePath=value;
    })  

    onMount(()=>{
        requestZeroCrossingRate();
    })

    function requestZeroCrossingRate()
    {
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/zerocrossingrate/`, {
            method: 'post',
            body:JSON.stringify({filepath:tempfilePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                // console.log("response",response);
                orgDatazcrs=response['zcrs'];
                orgDataZeroMax=response['zcrsmax'];
                console.log("zcrs: ",orgDatazcrs);
                console.log("zcrs: ",orgDatazcrs[5],orgDatazcrs[10]);         
                initVariables();
                drawZeroCrossingRate();       
        });
      })
      .catch((error) => {
        console.error(error);
      });
      console.log("end of function request zcrs function")
    }

    function initVariables(){
        console.log("function initVariables")
        orgDataLen=orgDatazcrs.length;
        orgDataIdx=new Array<number>(orgDataLen);

        for(var i=0;i<orgDataLen;i++)
        {   
            orgDataIdx[i]=i;
        }
        for(var i=0;i<orgDataLen;i++)
        {   
            let temp:any=new Array(2);
            if(orgDatazcrs[i]==null || orgDatazcrs[i]==undefined)
                temp[1]=0;
            else
                temp[1]=orgDatazcrs[i];
            temp[0]=orgDataIdx[i];
            orgDataCircle.push(temp);
        }                  
    }

    // 过零率就是每一帧内过零点的数量除以帧内总样本数量
    function drawZeroCrossingRate(){        
        d3.select('#zerocrossingrate').selectAll('*').remove();
        d3.select("g").selectAll('*').remove();

        var svg = d3.select('#zerocrossingrate')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLen+orgDataLen/10])
            .range([0, width]);

        var yScale = d3.scaleLinear()
            .domain([0, orgDataZeroMax])
            .range([0, height])

        var xAxis = d3.axisTop(xScale)
        yScale.range([height, 0]);  // 重新设置y轴比例尺的值域,与原来的相反        
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (margin.bottom+height) +")")
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
            .attr("r", 2)
            .attr("fill", "rgb(0,0,255)");
    }
</script>

<body>
    <!-- <Button on:click = {requestZeroCrossingRate} > load zcrs </Button>     -->
    <div id="zerocrossingrate"></div>
</body>