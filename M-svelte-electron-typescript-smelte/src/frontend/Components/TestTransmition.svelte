<script>
import * as d3 from 'd3'
function getDemo() {
    // 图表的宽度和高度
    var width = 1000;
    var height = 600;
    // 预留给轴线的距离
    var padding = { top: 100, right: 100, bottom: 100, left: 100 };
    var dataset = [[1, 224],[2, 328],[3, 156],[4, 232],[5, 382],[6, 304],[7, 366]];
     //数据最大最小值
    var min = d3.min(dataset, function(d) {
      return d[1];
    });
    var max = d3.max(dataset, function(d) {
      return d[1];
    });
     //比例尺
    var xScale = d3
      .scaleLinear()
      .domain([1, 7]) //比例尺的定义域
      .range([0, width - padding.left - padding.right]); //比例尺的值域
 
    var yScale = d3
      .scaleLinear()
      .domain([0, max])
      .range([height - padding.top - padding.bottom, 0]);
     //添加svg
    var svg = d3
      .select("body")
      .append("svg")
      .attr("width", width + "px")
      .attr("height", height + "px");
     //刻度线位置
    var xAxis = d3.axisTop().scale(xScale);
    var yAxis = d3.axisLeft().scale(yScale);
 
    //添加表标题
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", 20)
      .attr("text-anchor", "middle")
      .style("fill", "#000")
      .style("font-size", "18px")
      .style("text-decoration", "underline")
      .text("月销售表");
    //添加x轴坐标轴
    svg
      .append("g")
      .attr("class", "axis")
      .attr(
        "transform",
        "translate(" + padding.left + "," + (height - padding.bottom) + ")"
      )
      .call(xAxis)
      .append("text")
      .style("fill", "#000")
      .style("text-anchor", "middle")
      .attr(
        "transform",
        "translate(" + (width - padding.left - padding.right) + "," + 20 + ")"
      )
      .text("月份");
    //添加y轴坐标轴
    svg
      .append("g")
      .attr("class", "axis")
      .attr(
        "transform",
        "translate(" + padding.left + "," + padding.top + ")"
      )
      .call(yAxis)
      .append("text")
      .style("fill", "#000")
      .style("text-anchor", "middle")
      .attr("transform", "translate(" + 0 + "," + -10 + ")")
      .text("销售量");
 
    // 坐标轴上的线
    var linePath = d3
      .line()
      .x(function(d) {
        return xScale(d[0]);
      })
      .y(function(d) {
        return yScale(d[1]);
      });
 
    // 折线图上的线
    svg
      .append("g")
      .append("path")
      .attr("class", "line-path")
      .attr(
        "transform",
        "translate(" + padding.left + "," + padding.top + ")"
      )
      .attr("d", linePath(dataset))
      .attr("fill", "none")
      .attr("stroke-width", 2)
      .attr("stroke", "skyblue");
    // 折线图上的圆点
    svg
      .append("g")
      .selectAll("circle")
      .data(dataset)
      .enter()
      .append("circle")
      .attr("r", 6)
      .attr("transform", function(d) {
        return (
          "translate(" +
          (xScale(d[0]) + padding.left) +
          "," +
          (yScale(d[1]) + padding.top) +
          ")"
        );
      })
      .attr("fill", "#CCFFFF")
      .transition()
      .duration(5000)
      .attr("r", 10)
      .attr("fill","black");
  }
</script>

<body>
    <button on:click = {getDemo} > load data </button>
</body>