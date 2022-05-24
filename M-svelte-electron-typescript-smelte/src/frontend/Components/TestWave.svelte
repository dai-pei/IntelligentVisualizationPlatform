<script lang='ts'>
    import * as d3 from 'd3';
    import {onMount} from 'svelte';
    let filePath: any;
    let orgData:number[]|undefined|null;
    let orgDataLen:number|undefined|null;
    let orgDataIdx:number[]|undefined|null;
    let orgDataCircle:number[][]=[];

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

        filePath=file.path
        console.log(filePath)
    }

    async function requestLoadData() {
        console.log(filePath);
        fetch(`http://127.0.0.1:6005/orgdata/`, {
            method: 'post',
            body:JSON.stringify({filepath:filePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log(response["loaddata"]);
                orgData=response["loaddata"];
                // console.log("one data_______");
                // console.log(orgData[5])
                orgDataLen=orgData.length;

                console.log(orgDataLen)

                orgDataIdx=new Array<number>(orgDataLen);
                for(var i=0;i<orgDataLen;i++)
                {   
                    orgDataIdx[i]=i;
                }

                for(var i=0;i<orgDataLen;i++)
                {   
                    let temp:any=new Array(2);
                    temp[1]=orgData[i];
                    temp[0]=orgDataIdx[i];
                    orgDataCircle.push(temp);
                }               
                drawSVG();
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }


    // var data = [[0.5, 0.5],[0.7, 0.8],[0.4, 0.9],
    // [0.11, 0.32],[0.88, 0.25],[0.75, 0.12],
    // [0.5, 0.1],[0.2, 0.3],[0.4, 0.1]];
    
    var _width = 1500, height = 800;
    var margin = { top: 40, right: 40, bottom: 800, left: 40 };

    var width = _width - margin.left - margin.right;
    var height = width;

    function drawSVG(){
        var svg = d3.select('#mychart')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);


        var yScale = d3.scaleLinear()
            .domain([-1, 1])
            .range([0, 500])

        var xScale = d3.scaleLinear()
            .domain([-1000, orgDataLen+1000])
            .range([0, 800]);



        var xAxis = d3.axisTop(xScale)
        
        // yScale.range([1, 0]);  // 重新设置y轴比例尺的值域,与原来的相反
        
        var yAxis = d3.axisLeft(yScale)


        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom) +")")
                .call(xAxis);

        svg.append("g").attr("class", "axis")
                .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom - 1) +")")
                .call(yAxis);


        svg.selectAll("circle")  
            .data(orgDataCircle)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                    return margin.left + xScale(d[0]);
            })
            .attr("cy", function(d) {
                    return  yScale(d[1])+ (height - margin.bottom - 1)
            })
            .attr("r", 5)
            .attr("fill", "rgb(0,0,255)")
            .on("mousedown", function(d,i){
                console.log("这里是添加交互的内容");
                d3.select(this)
                    .style("fill", "black");
                    d3.select(this) //在传给任何D3方法的匿名函数中，如果想操作当前元素，只要引用this就行
             });
    }
    onMount(()=>{       

        // var svg = d3.select('#mychart')
        //     .append('svg')
        //     .attr('width', width + margin.left + margin.right)
        //     .attr('height', height + margin.top + margin.bottom);


        // var xScale = d3.scaleLinear()
        //     .domain([0, 1])
        //     .range([0, 200]);

        // var yScale = d3.scaleLinear()
        //     .domain([0, 1])
        //     .range([0, 200])


        // var xAxis = d3.axisBottom(xScale)
        
        // // yScale.range([1, 0]);  // 重新设置y轴比例尺的值域,与原来的相反
        
        // var yAxis = d3.axisLeft(yScale)


        // svg.append("g").attr("class", "axis")
        //         .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom) +")")
        //         .call(xAxis);

        // svg.append("g").attr("class", "axis")
        //         .attr("transform", "translate("+ margin.left +","+ (height - margin.bottom - 1) +")")
        //         .call(yAxis);


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
        //     .attr("r", 5)
        //     .attr("fill", "rgb(0,0,255)");
    });
</script>

<body>
    <button on:click = {requestLoadData} > load data </button>
    
    <input type = "file" on:change = {handleFileUploaded}/> 
    <div id="mychart"></div>
</body>