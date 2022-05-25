<script lang='ts'>
    import * as d3 from 'd3';
    import {filePath,startSecond,endSecond,} from '../stores/status';
    let tempfilePath:any;
    let tempstartSecond:number=-1;
    let tempendSecond:number=-1;

    let orgDatacent:any;
    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    let width:number=1000
    let height:number=1000 
    var margin = { top: 40, right: 40, bottom: 40, left: 40 };

    filePath.subscribe(value=>{
        tempfilePath=value;
    })   
    startSecond.subscribe(value=>{
        tempstartSecond=value;
    })
    endSecond.subscribe(value=>{
        tempendSecond=value;
    })

    function requestSpectrumCentroid()
    {
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/spectrumcentroid/`, {
            method: 'post',
            body:JSON.stringify({filepath:tempfilePath,startsecond:tempstartSecond,endsecond:tempendSecond}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                orgDatacent=response['cent'];
                console.log("cent: ",orgDatacent);
                // console.log("zcrs: ",orgDatacent[5],orgDatacent[10]);         
                initVariables();
                drawSpectrumCentroid();       
        });
      })
      .catch((error) => {
        console.error(error);
      });
      console.log("end of function request spec cent function")
    }

    function initVariables(){
        console.log("function initVariables")
        orgDataLen=orgDatacent.length;
        orgDataIdx=new Array<number>(orgDataLen);

        for(var i=0;i<orgDataLen;i++)
        {   
            orgDataIdx[i]=i;
        }
        for(var i=0;i<orgDataLen;i++)
        {   
            let temp:any=new Array(2);
            if(orgDatacent[i]==null || orgDatacent[i]==undefined)
                temp[1]=0;
            else
                temp[1]=orgDatacent[i];
            temp[0]=orgDataIdx[i];
            orgDataCircle.push(temp);
        }                  
    }

    function drawSpectrumCentroid(){        
        d3.select('#spectrumcentroid').selectAll('*').remove();
        d3.select("g").selectAll('*').remove();

        var svg = d3.select('#spectrumcentroid')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLen+orgDataLen/10])
            .range([0, 500]);

        var yScale = d3.scaleLinear()
            .domain([0, 0.03])
            .range([0, 500])

        var xAxis = d3.axisTop(xScale)
        yScale.range([500, 0]);  // 重新设置y轴比例尺的值域,与原来的相反        
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (margin.bottom+500) +")")
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
            .attr("r", 5)
            .attr("fill", "rgb(0,0,255)");

    }
</script>

<body>
    <form>
        <span>
            
        </span>
        <input type="file" multiple="multiple"/>
    </form>
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
    <button on:click = {requestSpectrumCentroid} > load cent </button>    
    <div id="spectrumcentroid"></div>
</body>