<script lang='ts'>
    import * as d3 from 'd3';
    import {filePathMulti} from '../stores/status';
    let tempfilePathMulti:any;
    let classArr=["Tom","close"];
    let classArrList=["close","open","crash","kick","ride","snare","Tom"]

    let orgDataKNN:any;
    let orgDataLen:number;
    let orgDataCircle:number[][]=[];
    let orgDataIdx:number[];

    // 最多只支持7种类别的区分
    var colorName = ["red", "blue", "green", "yellow", "black","purple","orange"];


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
                    return compute(d[2]);  
                });

    }

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
            else{
                tempArr.push("close");
            }
            tempfilePathMulti.push(tempArr)
        }
        filePathMulti.set(tempfilePathMulti);
        // console.log(tempfilePathMulti);
    }
</script>

<body>
    <form>
        <span>
            
        </span>
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
        {#each menu as flavour}
            <option value={flavour}>
                {flavour}
            </option>
        {/each}
    </select>
    <button on:click = {requestZeroCentMaxForKNN} > tom and close-hat & zcrs/cent/knn </button>    
    <div id="zerocentknn"></div>
</body>