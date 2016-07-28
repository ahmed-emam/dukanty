var data = [
        {
            name: "Lavon Hilll I",
            BMI: 20.57,
            age: 12,
            birthday: "1994-10-26T00:00:00.000Z",
            city: "Annatown",
            married: true,
            index: 1
        },
        {
            name: "Clovis Pagac",
            BMI: 24.28,
            age: 26,
            birthday: "1995-11-10T00:00:00.000Z",
            city: "South Eldredtown",
            married: false,
            index: 3
        },
        {
            name: "Gaylord Paucek",
            BMI: 24.41,
            age: 30,
            birthday: "1975-06-12T00:00:00.000Z",
            city: "Koeppchester",
            married: true,
            index: 5
        },
        {
            name: "Ashlynn Kuhn MD",
            BMI: 23.77,
            age: 32,
            birthday: "1985-08-09T00:00:00.000Z",
            city: "West Josiemouth",
            married: false,
            index: 6
        }
]


// var BarChart = rd3.BarChart;

// var barData = [
//   {label: 'A', value: 5},
//   {label: 'B', value: 6},
//   {label: 'F', value: 7}
// ];

// var Hello = React.createClass({
//     render: function() {
//         return <BarChart
//                   data={barData}
//                   width={500}
//                   height={200}
//                   fill={'#3182bd'}
//                   title='Bar Chart'/>;
//     }
// });
 
// ReactDOM.render(<Hello name="World" />, document.getElementById('content'));



// var width = 700,
// height = 300,
// margins = {left: 100, right: 100, top: 50, bottom: 50},
// title = "User sample",
// // chart series,
// // field: is what field your data want to be selected
// // name: the name of the field that display in legend
// // color: what color is the line
// chartSeries = [
//   {
//     field: 'BMI',
//     name: 'BMI',
//     color: '#ff7f0e'
//   }
// ],
// // your x accessor
// x = function(d) {
//   return d.index;
// }

// ReactDOM.render(
//     <Chart
//       title={title}
//       width={width}
//       height={height}
//       margins= {margins}
//       >
//         <LineChart
//             showXGrid= {false}
//             showYGrid= {false}
//             margins= {margins}
//             title={title}
//             data={data}
//             width={width}
//             height={height}
//             chartSeries={chartSeries}
//             x={x}
//         />
//     </Chart>
//   , document.getElementById('line-user')
// );

var Chart = React.createClass({
  propTypes: {
    data: React.PropTypes.array
  },
  render: function () {
    var data = this.props.data
    var margin = {top: 20, right: 20, bottom: 30, left: 50}
    var width = 960 - margin.left - margin.right
    var height = 500 - margin.top - margin.bottom

    var parseDate = d3.time.format('%d-%b-%y').parse

    var x = d3.time.scale()
    .range([0, width])

    var y = d3.scale.linear()
    .range([height, 0])

    var xAxis = d3.svg.axis()
    .scale(x)
    .orient('bottom')

    var yAxis = d3.svg.axis()
    .scale(y)
    .orient('left')

    var line = d3.svg.line()
    .x(function (d) { return x(d.date) })
    .y(function (d) { return y(d.close) })

    var node = ReactFauxDOM.createElement('svg')
    var svg = d3.select(node)
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')

    data.forEach(function (d) {
      d.date = parseDate(d.date)
      d.close = +d.close
    })

    x.domain(d3.extent(data, function (d) { return d.date }))
    y.domain(d3.extent(data, function (d) { return d.close }))

    svg.append('g')
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + height + ')')
    .call(xAxis)

    svg.append('g')
    .attr('class', 'y axis')
    .call(yAxis)
    .append('text')
    .attr('transform', 'rotate(-90)')
    .attr('y', 6)
    .attr('dy', '.71em')
    .style('text-anchor', 'end')
    .text('Price ($)')

    svg.append('path')
    .datum(data)
    .attr('class', 'line')
    .attr('d', line)

    return node.toReact()
  }
})

function render (data) {
  React.render(React.createElement(Chart, {
    data: data
  }), document.getElementById('mount'))
}

d3.tsv(data, function (error, data) {
  if (error) {
    throw error
  }

  render(data)
})

