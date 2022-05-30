<script lang='ts'>
    import * as d3 from 'd3';
    import {filePath} from '../stores/status'
    let orgData:number[]|undefined|null;
    let orgDataLenFreq:number|undefined|null;
    let orgDataLenTime:number|undefined|null;
    let orgDataIdx:number[]|undefined|null;
    let orgDataCircle:number[][][]=[];

    var a = d3.rgb(0,0,0);     
    var b = d3.rgb(255,255,255);   
    var compute = d3.interpolate("purple","yellow");      
    // var colorRange=d3.range(6).map(function(i) { return "q" + i + "-6"; });
    // var threshold=d3.scaleThreshold()//阈值比例尺
    //         .domain([10,20,30,40,50])
    //         .range(colorRange);

    let maxAmp:number=-100;
    let minAmp:number=100;
    
    
    let linear:any;


    function handleFileUploaded(e:Event){
        const target = e.target as HTMLInputElement;
        const files = target.files;
        if (!files) {
            console.log(1);
            return;
        }

        const file = files[0];
        if (!file) {
            console.log(2);
            return;
        }

        filePath.set(file.path)
        console.log(filePath)
    }

    async function requestLoadData() {
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/spectrum/`, {
            method: 'post',
            body:JSON.stringify({filepath:$filePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log(response["loaddata"]);
                orgData=response["loaddata"];
                orgDataLenFreq=orgData.length; //1024
                orgDataLenTime=orgData[0].length; //625

                orgDataIdx=new Array<number>(orgDataLenTime);
                for(var i=0;i<orgDataLenTime;i++)
                {   
                    orgDataIdx[i]=i;
                }

                console.log(orgDataLenFreq,orgDataLenTime);
                for(var i=0;i<orgDataLenTime;i++)
                {   
                    for(var j=0;j<orgDataLenFreq;j++)
                    {
                        let temp:any=new Array(3);
                        temp[0]=i;
                        temp[1]=j;
                        // console.log(i,j)
                        let num:number|undefined|null=orgData[j][i];
                        if(num==undefined)
                            temp[2]=0;
                        else
                            temp[2]=Math.abs(num);
                            if(num>maxAmp)
                                maxAmp=num
                            if(num<minAmp)
                                minAmp=num
                        // console.log(temp[2]);
                        orgDataCircle.push(temp);
                    }   
                    
                }               
                // console.log(orgDataCircle.length,orgDataCircle[0].length)
                linear = d3.scaleLinear().domain([0, maxAmp]).range([0, 1])
                drawSVG();
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }

    var _width = 1500, height = 800;
    var margin = { top: 40, right: 40, bottom: 800, left: 40 };

    var width = _width - margin.left - margin.right;
    var height = width;

    function drawSVG(){
        console.log("color");
        // var temparr=[];
        // for(var i=0;i<orgDataLenTime;i++)
        // {   
        //     for(var j=0;j<orgDataLenFreq;j++)
        //     {
        //         temparr.push(orgData[i][j]);
        //     }            
        // }   
        // console.log(temparr);
        // let arr=[0.2,0.6]
        // console.log(compute(arr));
        var svg = d3.select('#mychart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, orgDataLenTime])
            .range([0, 800]);
        var yScale = d3.scaleLinear()
            .domain([0, orgDataLenFreq])
            .range([800, 0])

        var xAxis = d3.axisTop(xScale)        
        var yAxis = d3.axisLeft(yScale)

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom) +")")
                .call(xAxis);

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom - 1) +")")
                .call(yAxis);


        // svg.selectAll("circle")  
        //     .data(orgDataCircle)
        //     .enter()
        //     .append("circle")
        //     .attr("cx", function(d) {
        //             return margin.left + xScale(d[0]);
        //     })
        //     .attr("cy", function(d) {
        //             return  yScale(d[1])+ (height - margin.bottom - 1)
        //     })
        //     .attr("r", 4)
        //     // .attr("fill", "rgb(0,0,255)")
        //     .style("fill",function(d){  
        //             return compute(linear(d[2]));  
        //         });
        svg.selectAll("rect")  
            .data(orgDataCircle)
            .enter()
            .append("rect")
            .attr("x", function(d) {
                    return margin.left + xScale(d[0]);
            })
            .attr("y", function(d) {
                    return  yScale(d[1])+ (height - margin.bottom)
                    })
            .attr('width', 10)
            .attr('height',10)
            .style("fill",function(d){  
                    // return threshold(d[2]);  
                    return compute(linear(d[2]));  
                });
            // .on("mousedown", function(d,i){
            //     console.log("这里是添加交互的内容");
            //     d3.select(this)
            //         .transition(300)
            //         .style("fill", "black");
            //         d3.select(this) //在传给任何D3方法的匿名函数中，如果想操作当前元素，只要引用this就行
            //  })
            // })
            
    }    
</script>

<body>
    <button on:click = {requestLoadData} > load data </button>
    
    <input type = "file" on:change = {handleFileUploaded}/> 
    <div id="mychart"></div>
</body>

<style>
    /* .q0-6{fill:rgb(165,0,38)}
    .q1-6{fill:rgb(215,48,39)}
    .q2-6{fill:rgb(244,109,67)}
    .q3-6{fill:rgb(253,174,97)}
    .q4-6{fill:rgb(254,224,139)}
    .q5-6{fill:rgb(255,255,191)} */
    svg text　{pointer-event:none;}

</style>