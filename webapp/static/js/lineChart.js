Chart.pluginService.register({
    beforeDraw: function (chart, easing) {
        if (chart.config.options.chartArea && chart.config.options.chartArea.backgroundColor) {
            var helpers = Chart.helpers;
            var ctx = chart.chart.ctx;
            var chartArea = chart.chartArea;

            ctx.save();
            ctx.fillStyle = chart.config.options.chartArea.backgroundColor;
            ctx.fillRect(chartArea.left, chartArea.top, chartArea.right - chartArea.left, chartArea.bottom - chartArea.top);
            ctx.restore();
        }
    }
});

var DATA = {};
var YEAR = {};

var config = {};

var line_cart_cutom = {};

function onload_line_chart() {
    selected_year = $("#YearSelect").val();
    console.log(selected_year);

      $.ajax({
        url: "./detail/" + selected_year + "/",
        success: function(the_json){
          console.log(DATA);

          DATA = the_json;

          DATA.year = selected_year;

          console.log("on change chart data", DATA.train);
          config = {
              type: 'line',
              data: {
                  labels: DATA.hour,
                  datasets: [{
                      label: 'Train',
                      backgroundColor: '#0073d0',
                      borderColor: '#0073d0',
                      data: DATA.train,
                      fill: false,
                  }, {
                      label: 'Bus',
                      fill: false,
                      backgroundColor: '#ff8201',
                      borderColor: '#ff8201',
                      data: DATA.bus,
                  }, {
                      label: 'Tram',
                      fill: false,
                      backgroundColor: '#78be1f',
                      borderColor: '#78be1f',
                      data: DATA.tram,
                  }]
                },
                  options: {
                      chartArea: {
                          backgroundColor: '#ffffff',
                      },
                      responsive: true,
                      title: {
                          display: true,
                          text: 'Number of transactions per hour in each mode in ' + DATA.year
                      },
                      tooltips: {
                          mode: 'index',
                          intersect: false,
                      },
                      hover: {
                          mode: 'nearest',
                          intersect: true
                      },
                      scales: {
                          xAxes: [{
                              display: true,
                              scaleLineColor: 'rgb(179, 242, 237)',
                              scaleLabel: {
                                  display: true,
                                  labelString: 'hour'
                              }
                          }],
                          yAxes: [{
                              display: true,
                              scaleLineColor: 'rgb(179, 242, 237)',
                              scaleLabel: {
                                  display: true,
                                  labelString: 'Number of passengers'
                              }
                          }]
                      }
                  }
              };

              console.log(config);


              $('#graph-container').html("");
              // $('#canvas').remove(); // this is my <canvas> element
              $('#graph-container').append('<canvas id="canvas"><canvas>');

            var ctx = canvas = document.querySelector('#canvas').getContext('2d');
            line_cart_cutom = new Chart(ctx, config);

        }
      });
}


function onchange_line_chart() {
    console.log("onchange_line_chart");

    selected_year = $("#YearSelect").val();

    DATA.year = selected_year;
    console.log(selected_year);

      $.ajax({
        url: "./detail/" + selected_year,
        success: function(the_json){
          DATA = the_json;

          console.log(line_cart_cutom.data.labels);
          line_cart_cutom.data.labels.pop();

          line_cart_cutom.data.labels = DATA.hour;
          console.log(line_cart_cutom.data.labels);

          line_cart_cutom.data.datasets.forEach((dataset) => {
              // console.log(dataset.data);
              dataset.data.pop();
          });

          line_cart_cutom.data.datasets = [{
              label: 'Train',
              backgroundColor: '#0073d0',
              borderColor: '#0073d0',
              data: DATA.train,
              fill: false,
          }, {
              label: 'Bus',
              fill: false,
              backgroundColor: '#ff8201',
              borderColor: '#ff8201',
              data: DATA.bus,
          }, {
              label: 'Tram',
              fill: false,
              backgroundColor: '#78be1f',
              borderColor: '#78be1f',
              data: DATA.tram,
          }];

          // line_cart_cutom.data = {};

          line_cart_cutom.update();
        }
      });
}


$(document).ready(function() {
    console.log( "ready!" );

      onload_line_chart();

      $( "#YearSelect" ).change(function() {
        onchange_line_chart();
      });
});

// document.getElementById('addData').addEventListener('click', function (datasets) {
//     if (config.data.datasets.length > 0) {
//         var year = YEAR[config.data.labels.length % YEAR.length];
//         config.data.labels.push(year);
//         config.data.datasets.forEach(function (dataset) {
//             dataset.data.push(datasets);
//         });
//         window.myLine.update();
//     }
// });
//
// document.getElementById('removeData').addEventListener('click', function () {
//     config.data.labels.splice(-1, 1); // remove the label first
//     config.data.datasets.forEach(function (dataset) {
//         dataset.data.pop();
//     });
//     window.myLine.update();
// });
