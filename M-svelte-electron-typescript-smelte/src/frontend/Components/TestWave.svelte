<script lang="ts">
    import * as d3 from 'd3';
    let filePath: any;
    async function requestLoadData() {
        fetch(`http://127.0.0.1:6005/orgdata/`, {
            method: 'post',
            // body:"filepath="+filePath,
            body:JSON.stringify({filepath:filePath}),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((res) => {
            return res.json().then((response) => {
                console.log("json loaddata")
                console.log(response["loaddata"]);
        });
      })
      .catch((error) => {
        console.error(error);
      });
    }

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

    var width = 400;    // 可视区域宽度
    var height = 400;   // 可视区域高度
    var padding = {top: 20, right: 20, bottom:20, left:50};

    var svg = d3.select("body").select("#content")
            .append("svg")
            .attr("width", width).attr("height", height);
    var xAxisWidth = 300;   // x轴宽度
    var yAxisWidth = 300;   // y轴宽度

    var xScale = d3.scaleLinear()
        .domain([0, 1])
        .range([0, xAxisWidth]);

    var yScale = d3.scaleLinear()
        .domain([0, 1])
        .range([0, yAxisWidth]);
    


</script>

<input type = "file" on:change = {handleFileUploaded}/> 
<button on:click = {requestLoadData} > load data </button>
<div id="wave-content">

</div>