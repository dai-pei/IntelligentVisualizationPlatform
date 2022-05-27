<script lang='ts'>
    import * as d3 from 'd3';
    import Button from "smelte/src/components/Button";
    import {filePathMulti} from '../stores/status';
    let tempfilePathMulti:any;
    let classArr=["close"];
    let classArrList=["close","open","crash","kick","ride","snare","Tom"]

    let orgDataKNN:any|undefined|null;
    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    // 最多只支持7种类别的区分
    var colorName = ["red", "black", "green", "yellow", "blue","purple","orange","crimson"];


    let width:number=1000
    let height:number=1000 
    var margin = { top: 40, right: 40, bottom: 40, left: 40 };

    filePathMulti.subscribe(value=>{
        tempfilePathMulti=value;
    })   

    function requestZeroCentMaxForKNN()
    {
        console.log(tempfilePathMulti);
        fetch(`http://127.0.0.1:6005/zerocentmaxforknn/`, {
            method: 'post',
            body:JSON.stringify({filepathmulti:tempfilePathMulti,classes:classArr}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                // console.log(response);
                orgDataKNN=response['data'];
                console.log("orgDataKNN: ",orgDataKNN);
                
                initVariables();
                drawZeroCentKNN();       
        });
      })
      .catch((error) => {
        console.error(error);
      });
      console.log("end of function request spec cent function")
    }

    function initVariables(){
        console.log("function initVariables")
        orgDataLen=orgDataKNN.length;
        orgDataIdx=new Array<number>(orgDataLen);

        for(var i=0;i<orgDataLen;i++)
        {   
            orgDataIdx[i]=i;
        }
        for(var i=0;i<orgDataLen;i++)
        {   
            let temp:any=new Array(2);
            if(orgDataKNN[i]==null || orgDataKNN[i]==undefined)
                temp[1]=0;
            else
                temp[1]=orgDataKNN[i];
            temp[0]=orgDataIdx[i];
            orgDataCircle.push(temp);
        }                  
    }

    function compute(classname:string){
        let idx=classArr.findIndex(value=>value == classname);
        return colorName[idx];
    }

    function drawZeroCentKNN(){        
        d3.select('#zerocentknn').selectAll('*').remove();
        d3.select("g").selectAll('*').remove();

        var svg = d3.select('#zerocentknn')
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom);

        var xScale = d3.scaleLinear()
            .domain([0, 1])
            .range([0, 500]);

        var yScale = d3.scaleLinear()
            .domain([0, 6000])
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
            .data(orgDataKNN)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                    return margin.left + xScale(d[0]);
            })
            .attr("cy", function(d) {
                    return  yScale(d[1]) + margin.bottom;
            })
            .attr("r", 5)
            .style("fill", function(d){  
                    // return threshold(d[2]);  
                    return compute(d[2])
                })
            // .on("mousedown", function(){
            //     console.log("这里是添加交互的内容");
            //     d3.select(this)
            //         // .transition()
            //         // .duration(500)
            //         // .attr("r",8)
            //         // .style("fill", "blue");
            //     // d3.select(this)
            //         // .append("title")
            //         .append("p")
            //         .text(function(){
            //             return "aaa";
            //         });
            //         //d3.select(this) //在传给任何D3方法的匿名函数中，如果想操作当前元素，只要引用this就行
            //  });
            .on("mouseover",function(event,d){
                /*
                鼠标移入时，
                    （1）通过 selection.html() 来更改提示框的文字
                    （2）通过更改样式 left 和 top 来设定提示框的位置
                    （3）设定提示框的透明度为1.0（完全不透明）
                    */
                d3.select(this)
                    .attr("r",10)
                    .style("fill","green");

                tooltip.html(d[0]+","+d[1]+","+d[2])
                            .style("position","absolute")
                            .style("left", (d3.pointer(event,this)[0]) + "px")
                            .style("top", (d3.pointer(event,this)[1]+100) + "px")
                            .style("opacity",1.0);
                })
                .on("mousemove",function(event,d){
                /* 鼠标移动时，更改样式 left 和 top 来改变提示框的位置 */

                    // console.log(d3.pointer(event,this));
                    tooltip.style("left", (d3.pointer(event,this)[0]) + "px")
                            .style("top", (d3.pointer(event,this)[1]+100) + "px");
                })
                .on("mouseout",function(event,d){
                /* 鼠标移出时，将透明度设定为0.0（完全透明）*/

                    d3.select(this)
                        .attr("r",5)
                        .style("fill",compute(d[2]));
                    tooltip.style("opacity",0.0);
            })
    }

    var tooltip = d3.select("body")
        .append("div")
        .attr("class","tooltip")
        .style("opacity",0.0);

    function handleMultiFileUploaded(e:Event){
        const target = e.target as HTMLInputElement;
        const files = target.files;
        // console.log(files);
        for (var i = 0; i < files.length; i++) {
            let tempArr=new Array();
            //打印所有的文件名
            // console.log(files[i].name);
            tempArr.push(files[i].path);
            if(files[i].name.includes("Tom")){
                tempArr.push("Tom");
            }
            else if(files[i].name.includes("close")){
                tempArr.push("close");
            }
            else if(files[i].name.includes("open")){
                tempArr.push("open");
            }
            else if(files[i].name.includes("crash")){
                tempArr.push("crash");
            }
            else if(files[i].name.includes("kick")){
                tempArr.push("kick");
            }
            else if(files[i].name.includes("snare")){
                tempArr.push("snare");
            }
            tempfilePathMulti.push(tempArr)
        }
        filePathMulti.set(tempfilePathMulti);
        // console.log(tempfilePathMulti);
    }
</script>

<body>
        <form>
        <input type="file" multiple="multiple" on:change={handleMultiFileUploaded}/>
    </form>
    <form>
        <span>
            svgWidth:
        </span>
        <input type="text" bind:value={width} />
        <span>
            svgHeight:
        </span>
        <input type="text" bind:value={height}/>
    </form>
    <select multiple bind:value={classArr}>
        {#each classArrList as chosenclass}
            <option value={chosenclass}>
                {chosenclass}
            </option>
        {/each}
    </select>
    <Button color="secondary" light block on:click={requestZeroCentMaxForKNN}>zcrs/cent/knn</Button>
    <div id="zerocentknn"></div>

    {#if classArr.length === 0}
        <p>Please select at least one class</p>
    {:else}
        <p>
            here is chosen classes:{classArr}
        </p>
    {/if}
</body>