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

function onload_line_chart(selected_year, stop_id) {
      var DATA = {};
      var YEAR = {};

      var config = {};

      var line_cart_cutom = {};

      $.ajax({
        url: "./lineChartStopAPI/" + selected_year + "/" + stop_id + "/",
        success: function(the_json){
          console.log(DATA);

          DATA = the_json;

          DATA.year = selected_year;

          console.log("on change chart data", DATA.train);
          config = {
              type: 'line',
              data: {
                  labels: DATA.hour,
                  datasets: []
                },
                  options: {
                      chartArea: {
                          backgroundColor: '#ffffff',
                      },
                      responsive: true,
                      title: {
                          display: true,
                          text: 'Number of transactions per hour in each route in ' + DATA.year
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

              var colorNames = Object.keys(window.chartColors);
              var i;
              for (i = 0; i < DATA.data.length; i++) {
                  datasets_route = DATA.data[i]
                  var colorName = colorNames[config.data.datasets.length % colorNames.length];
                  var newColor = window.chartColors[colorName];
                  var newDataset = {
                    label: 'Route ID ' + datasets_route.route_id,
                    backgroundColor: newColor,
                    borderColor: newColor,
                    data: datasets_route.data,
                    fill: false
                  };

                  // newDataset.data = [500000,500000]
                  config.data.datasets.push(newDataset);
                  // window.myLine.update();
              }

              console.log(config);


              $('#line-graph-container').html("");
              // $('#canvas').remove(); // this is my <canvas> element
              $('#line-graph-container').append('<canvas id="line-graph-containe"><canvas>');

            var ctx = canvas = document.querySelector('#line-graph-containe').getContext('2d');
            line_cart_cutom = new Chart(ctx, config);

        }
      });
}

function onload_bar_chart_stop(year, stop_id) {
      var DATA = {};
      var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      var barChartData = {};

      $.ajax({
        url: "./barChartStopAPI/" + year + "/" + stop_id + "/",
        success: function(the_json){

          DATA = the_json;
          var barChartData = {
            labels: MONTHS,
            datasets: [{
              label: 'Number of scan-on transactions',
              backgroundColor: '#0073d0',
              borderColor: '#0073d0',
              borderWidth: 1,
              data: DATA.scan_on
            }, {
              label: 'Number of scan-off transactions',
              backgroundColor: '#ff8201',
              borderColor: '#ff8201',
              borderWidth: 1,
              data: DATA.scan_off
            }]

          };

          var ctx = document.getElementById('canvas-bar-graph').getContext('2d');
          window.myBar = new Chart(ctx, {
            type: 'bar',
            data: barChartData,
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Number of scan_on/off for stop ' + DATA.stop_id + '-' + DATA.stop_name + ' in ' + year
              }
            }
          });

        }
      });
}

$(document).ready(function() {
    console.log( "ready!" );

      onload_bar_chart_stop(global_year, global_stop_id);
      onload_line_chart(global_year, global_stop_id);

      // $( "#YearSelect" ).change(function() {
      //   onchange_line_chart();
      // });
});
