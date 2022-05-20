<script lang="ts">
import moment from 'moment';
import * as d3 from 'd3';
var COLORS: any, COLORS_G: any, DATA: any, H: any, M: any, W: any, area: any, g: any, generate: any, keys: any, oH: any, oW: any, randomize: any, resize: any, stack, stacked_data, svg: any, x: any,
    xAxis: any, y: any, yAxis: any;

COLORS = ['#eaa54b', '#66a1e2', '#8065e4', '#48cb80'];

COLORS_G = ['#b5b5b5', '#8c8c8c', '#6b6b6b', '#565656'];

randomize = function(min: any, max: any) {
    return (Math.random() * (max - min) + min).toFixed(2);
};

/*
Final data looks like this
[
  { date: '11-Oct-14', A: '10', B: '9', C: '10', D: '8' },
  { date: '11-Oct-14', A: '10', B: '9', C: '10', D: '8' },
  { date: '11-Oct-14', A: '10', B: '9', C: '10', D: '8' }
]
 */

generate = function(count: any) {
    var data, i, j, ref;
    data = [];
    for (i = j = 1, ref = count; 1 <= ref ? j <= ref : j >= ref; i = 1 <= ref ? ++j : --j) {
        data.push({
            date: moment().add(i, 'days').toDate(),
            A: randomize(20, 25),
            B: randomize(15, 20),
            C: randomize(20, 25),
            D: randomize(20, 30)
        });
    }
    return data;
};

M = {
    top: 20,
    right: 0,
    bottom: 30,
    left: 50
};

oW = window.innerWidth;

oH = window.innerHeight;

W = oW - M.left - M.right;

H = oH - M.top - M.bottom;

DATA = generate(300);

keys = Object.keys(DATA[0]).filter(function(k: any) {
    return k !== 'date';
});

// x = d3.scaleTime().domain(d3.extent(DATA, function(d) {return d.date;})).range([0, W]);
let temp_array:any=d3.extent(DATA)
x = d3.scaleTime().domain(temp_array).range([0, W]);

y = d3.scaleLinear().range([H, 0]);

xAxis = d3.axisBottom(x);

yAxis = d3.axisLeft(y);
// yAxis = d3.axisLeft(y).tickFormat(d3.format('.0%'));

area = d3.area().x(function(d: any) {
    return x(d.date);
}).y0(function(d) {
    return y(d.y0);
}).y1(function(d) {
    return y(d.y0 + d.y);
});

stack = d3.stack().value(function(d: any) {
    return d.values;
});

stacked_data = stack(keys.map(function(k: any) {
    return {
        name: k,
        values: DATA.map(function(d: any) {
            return {
                date: d.date,
                y: d[k] / 100
            };
        })
    };
}));

svg = d3.select('body').append('svg').attr('width', oW).attr('height', oH).append('g').attr('transform', "translate(" + M.left + ", " + M.top + ")").on('mousemove', function() {
    var i, iX, point;
    point = d3.pointer(this);
    iX = x.invert(point[0]);
    i = x(iX);
    return console.log(i, iX);
});

g = svg.selectAll('g').data(stacked_data).enter().append('g');

g.append('path').attr('d', function(d: any) {
    return area(d.values);
}).attr('class', 'path').style('fill', function(d: any, i: any) {
    return COLORS[i];
});

svg.append('g').attr('class', 'x axis').attr('transform', "translate(0, " + H + ")").call(xAxis);

svg.append('g').attr('class', 'y axis').call(yAxis);

svg.append('g').selectAll('circle').data([0, 1, 2, 3]).enter().append('circle').attr('r', 3).style('fill', '#b5b5b5').style('opacity', .5);

resize = function() {
    oW = window.innerWidth;
    oH = window.innerHeight;
    W = oW - M.left - M.right;
    H = oH - M.top - M.bottom;
    x.range([0, W]);
    y.range([H, 0]);
    xAxis.scale(x);
    yAxis.scale(y);
    d3.select('svg').attr('width', oW).attr('height', oH);
    svg.select('.x.axis').transition().attr('transform', "translate(0, " + H + ")").call(xAxis);
    svg.select('.y.axis').transition().call(yAxis);
    return svg.selectAll('.path').transition().attr('d', function(d) {
        return area(d.values);
    });
};

d3.select(window).on('resize', resize);
</script>

<style>
html,
body {
    margin: 0;
    padding: 0;
    background: #474747;
}

svg {
    font-size: 0.75em;
    display: block;
}

svg .axis path,
svg .axis line {
    fill: none;
    stroke: #757575;
    stroke-width: 0.8px;
}

svg .axis text {
    fill: #757575;
}
</style>

<div>
    <body>
        <svg></svg>
    </body>
</div>
