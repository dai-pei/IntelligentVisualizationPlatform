<style>
  .hide-file-ui :global(input[type="file"]::file-selector-button) {
    display: none;
  }

  .hide-file-ui :global(:not(.mdc-text-field--label-floating) input[type="file"]) {
    color: transparent;
  }

  .demo-cell {
    height: 200px;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--mdc-theme-secondary, #333);
    color: var(--mdc-theme-on-secondary, rgb(245, 241, 241));
  }

  * :global(.demo-list) {
    max-width: 300px;
  }
</style>

<script lang="ts">
  import LayoutGrid, {
    Cell
  } from "@smui/layout-grid";
  import Textfield from "@smui/textfield";
  import Checkbox from "@smui/checkbox";
  import Button, {
    Label
  } from "@smui/button";
  import List, {
    Item,
    Meta
  } from '@smui/list';
  import HelperText from '@smui/textfield/helper-text';
  import * as d3 from 'd3';


  let selected: any[] = [];

  let allFilePaths: any = null;
  let checkedZero: any = true;
  let checkedCent: any = true;
  let checkedMfcc: any = true;

  let textContent = "";
  let tempfilePathMulti: any[] = [];
  let classArr: any[] = [];

  let orgDataKNN: any;
  let feature1max: number;
  let feature1min: number;
  let feature2max: number;
  let feature2min: number;

  // 最多只支持7种类别的区分
  let colorName = ["red", "green", "blue", "yellow", "black", "purple", "orange"];
  let classArrList = ["open", "close", "crash", "ride", "kick", "snare", "Tom"]
  let width: number = 600
  let height: number = 400
  var margin = {
    top: 40,
    right: 40,
    bottom: 40,
    left: 40
  };


  function handleFilesUploaded() {
    textContent = "";
    for (var i = 0; i < allFilePaths.length; i++) {
      textContent += allFilePaths[i].name;
      textContent += "\n";

      let tempArr = new Array();
      tempArr.push(allFilePaths[i].path);
      if (allFilePaths[i].name.includes("Tom")) {
        tempArr.push("Tom");
      } else if (allFilePaths[i].name.includes("close")) {
        tempArr.push("close");
      } else if (allFilePaths[i].name.includes("open")) {
        tempArr.push("open");
      } else if (allFilePaths[i].name.includes("crash")) {
        tempArr.push("crash");
      } else if (allFilePaths[i].name.includes("kick")) {
        tempArr.push("kick");
      } else if (allFilePaths[i].name.includes("snare")) {
        tempArr.push("snare");
      }
      tempfilePathMulti.push(tempArr);

      if (classArr == null || classArr == [] || classArr.findIndex((value) => value == tempArr[1]) == -1) {
        classArr.push(tempArr[1]);
      }
    }
    console.log(classArr);
  }

  function showFeaturesChart() {
    console.log("showFeaturechart");
    var cnt = 3;

    if (selected.findIndex((value) => value == 'zero') == -1) {
      cnt--;
      checkedZero = false;
    }
    if (selected.findIndex((value) => value == 'cent') == -1) {
      cnt--;
      checkedCent = false;
    }
    if (selected.findIndex((value) => value == 'mfcc') == -1) {
      cnt--;
      checkedMfcc = false;
    }
    if (cnt != 2) {
      console.log("cnt " + String(cnt));
      alert("必须要勾选两个特征，不可以少于也不可多于2个！");
    } else {
      if (checkedZero == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("cent", "mfcc");
      } else if (checkedCent == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("zero", "mfcc");
      } else if (checkedMfcc == false) {
        console.log("requestFeaturesForKNN");
        requestFeaturesForKNN("cent", "zero");
      }
    }
  }

  function requestFeaturesForKNN(chosenfeature1: string, chosenfeature2: string) {
    fetch(`http://127.0.0.1:6005/featuresforknn/`, {
        method: "post",
        body: JSON.stringify({
          filepathmulti: tempfilePathMulti,
          classes: classArr,
          feature1: chosenfeature1,
          feature2: chosenfeature2,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      }).then((res) => {
        return res.json().then((response) => {
          console.log(response);
          orgDataKNN = response["featuresforknn"];
          feature1max = response["ret1max"];
          feature1min = response["ret1min"];
          feature2max = response["ret2max"];
          feature2min = response["ret2min"];
          drawZeroCentKNN();
        });
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function compute(classname: string) {
    let idx = classArrList.findIndex(value => value == classname);
    return colorName[idx];
  }

  function drawZeroCentKNN() {
    d3.select('#knnchart').selectAll('*').remove();
    d3.select("g").selectAll('*').remove();

    var svg = d3.select('#knnchart')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom);

    var xScale = d3.scaleLinear()
      .domain([feature1min - feature1min / 5.0, feature1max + feature1max / 5.0])
      .range([0, width]);

    var yScale = d3.scaleLinear()
      .domain([feature2min - feature2min / 5.0, feature2max + feature2max / 5.0])
      .range([0, height])

    var xAxis = d3.axisTop(xScale)
    yScale.range([height, 0]); // 重新设置y轴比例尺的值域,与原来的相反        
    var yAxis = d3.axisLeft(yScale)

    svg.append("g").attr("class", "axis")
      .attr("transform", "translate(" + margin.left + "," + (margin.bottom + height) + ")")
      .call(xAxis);
    svg.append("g").attr("class", "axis")
      .attr("transform", "translate(" + margin.left + "," + margin.bottom + ")")
      .call(yAxis);

    svg.selectAll("circle")
      .data(orgDataKNN)
      .enter()
      .append("circle")
      .attr("cx", function (d) {
        return margin.left + xScale(d[0]);
      })
      .attr("cy", function (d) {
        return yScale(d[1]) + margin.bottom;
      })
      .attr("r", 5)
      .style("fill", function (d) {
        return compute(d[2])
      })
      .on("mouseover", function (event, d) {
        d3.select(this)
          .attr("r", 10)
          .style("fill", "black");

        tooltip.html(d[0] + "," + d[1] + "," + d[2])
          .style("position", "absolute")
          .style("left", (d3.pointer(event, this)[0]) + "px")
          .style("top", (d3.pointer(event, this)[1] + width/10) + "px")
          .style("opacity", 1.0);
      })
      .on("mousemove", function (event, d) {
        tooltip.style("left", (d3.pointer(event, this)[0]) + "px")
          .style("top", (d3.pointer(event, this)[1] + width/10) + "px");
      })
      .on("mouseout", function (event, d) {
        d3.select(this)
          .attr("r", 5)
          .style("fill", compute(d[2]));
        tooltip.style("opacity", 0.0);
      })
  }

  var tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0.0);
</script>

<body>
  <LayoutGrid>
    <Cell span="{12}">
      <div class="hide-file-ui">
        <input multiple type="file" bind:files="{allFilePaths}" on:change="{handleFilesUploaded}" />
      </div>
    </Cell>
    <Cell span="{6}">
      <div class="demo-cell">
        <Textfield class="demo-cell" style="width: 80%;" helperLine$style="width: 80%;" disabled textarea
          bind:value="{textContent}" label="FilePaths" invalid>
          <HelperText slot="helper">选中的音频路径</HelperText>
        </Textfield>
      </div>
    </Cell>
    <Cell span="{6}">
      <div>
        <List class="demo-list" checkList>
          <Item>
            <Label>过零率</Label>
            <Meta>
            <Checkbox bind:group={selected} value="zero" />
            </Meta>
          </Item>
          <Item>
            <Label>频谱质心</Label>
            <Meta>
            <Checkbox bind:group={selected} value="cent" />
            </Meta>
          </Item>
          <Item>
            <Label>MFCC</Label>
            <Meta>
            <Checkbox bind:group={selected} value="mfcc" />
            </Meta>
          </Item>
        </List>
        <div class="comfirm-button">
          <Button on:click={showFeaturesChart} variant="outlined">
            <Label>生成二维特征数组</Label>
          </Button>
        </div>
      </div>
    </Cell>
    <Cell span="{12}">
      <div id="knnchart">
      </div>
    </Cell>
  </LayoutGrid>
</body>