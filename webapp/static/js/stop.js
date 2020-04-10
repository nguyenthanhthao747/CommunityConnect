var stops_map = {}
var markers = new L.FeatureGroup();

const faIconTrain = L.divIcon({
    html: '<i class="color-train fas fa-fw fa-subway fa-2x"></i>',
    iconSize: [25, 25],
    className: 'myDivIcon'
});
const faIconTram = L.divIcon({
    html: '<i class="color-tram fas fa-fw fa-train fa-2x"></i>',
    iconSize: [25, 25],
    className: 'myDivIcon'
});
const faIconBus = L.divIcon({
    html: '<i class="color-bus fas fa-fw fa-bus fa-2x"></i>',
    iconSize: [25, 25],
    className: 'myDivIcon'
});

$(function() {

  // Handler for .ready() called.
  stops_map = L.map('mapid').setView([-37.814, 144.9631], 12);

  // pk.eyJ1IjoiYW1pdDAwMDciLCJhIjoiY2ptNTlrZGhpMDBzejNrcXEwZnloOTAzcCJ9.1Sg9Tl2kvO0wQ5JuMStthQ

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiYW1pdDAwMDciLCJhIjoiY2ptNTlrZGhpMDBzejNrcXEwZnloOTAzcCJ9.1Sg9Tl2kvO0wQ5JuMStthQ'
  }).addTo(stops_map);

  render_map();

  $(".btn-filter-now").click(function() {
    render_map();
  });

  stops_map.on('moveend', function(e) {
    render_map();
  });


  var slider = document.getElementById('scan_range');

  noUiSlider.create(slider, {
      start: [80000, 200000],
      step: 10,
      connect: true,
      range: {
          'min': 0,
          'max': 600000
      },
      ariaFormat: wNumb({
        decimals: 0
      }),
      format: wNumb({
          decimals: 0,
          thousand: ','
      })
  }).on('update', function (values, handle) {
    if (handle) {
        $("#max_range").val(values[handle]);
    } else {
        $("#min_range").val(values[handle]);
    }
  });

});

function render_map(){

  // stops_map.removeLayer(markers);
  markers.clearLayers();

  var center_long_lat = stops_map.getCenter();
  // console.log("Map center", stops_map.getCenter())

  // console.log("Map Bounds", stops_map.getBounds())

  var stop_map_bounds = stops_map.getBounds();
  // console.log(stop_map_bounds._northEast);
  // console.log(stop_map_bounds._southWest);

  // console.log(stops_map.distance(stop_map_bounds._northEast, stop_map_bounds._southWest));

  var distance_1 = stops_map.distance(center_long_lat, stop_map_bounds._northEast);
  var distance_2 = stops_map.distance(center_long_lat, stop_map_bounds._southWest);

  var max_radius = distance_2;
  if(distance_1 < distance_2){
    max_radius = distance_1;
  }

  selected_year = $("#select-year").val();
  var min_range = $("#min_range").val();
  var max_range = $("#max_range").val();

  selected_scan_range = min_range.replace(",", "") + "," + max_range.replace(",", "");


  // get near by points to the map center
  get_nearby_stops(center_long_lat, max_radius/1000, selected_year, selected_scan_range);
}

function get_nearby_stops(center_long_lat, max_radius, year_selected, min_max){
  $("#stop_info_container").hide();
  // console.log("get_nearby_stops", center_long_lat, max_radius);

  $.ajax({
      type: "POST",
      url: "../api/",
      data: {
          required: 'get_nearby_stops',
          lat: center_long_lat.lat,
          lng: center_long_lat.lng,
          max_radius: max_radius,
          year_selected: year_selected,
          min_max: min_max
      },
      beforeSend: function(){
        $(".btn-filter-now").button('loading');
      },
      success: function(msg){
        // console.log(msg);
        // var scanon = new Map(kvArray);
        // var scanoff = new Map(kvArray);
        msg.data.forEach(function(elem) {
          var add_options = {};

          add_options = {
            'icon': faIconTrain,
            'alt': elem[0]
          };

          if(elem[7] == 1){
            add_options = {
              'icon': faIconBus,
              'alt': elem[0]
            };
          }

          if(elem[7] == 3){
            add_options = {
              'icon': faIconTram,
              'alt': elem[0]
            };
          }

          var cur_mark = L.marker([elem[2], elem[3]], add_options).on('click', function(e) {
            marker_touched(e);
          });

            var popup = L.popup()
              .setLatLng([elem[2], elem[3]])
              .setContent(`
<div class="row">
  <div class="col-6 mb-1"><b>Stop ID:</b> ${elem[0]}</div>
  <div class="col-6 mb-1 text-right"><b>Year:</b> ${year_selected}</div>
  <div class="col-12 mb-1"><b>Scan On Count:</b> ${elem[1]}</div>
  <div class="col-12 mb-1"><b>Stop Name:</b> ${elem[4]}</div>
  <div class="col-12 mb-1"><b>Suburb:</b> ${elem[6]}</div>
  <div class="col-12 mb-1"><b>Post code:</b> ${elem[5]}</div>
</div>`);

            cur_mark.bindPopup(popup);

            markers.addLayer(cur_mark);
        });

        markers.addTo(stops_map)

        $(".btn-filter-now").button('reset');
      }
  });
}

function marker_touched(ev){
  // console.log(ev.target.options);

  if(ev.target.options){
    var stop_id = ev.target.options.alt;
    var scan_count = ev.target.options.title;
    selected_year = $("#select-year").val();

    onload_bar_chart_stop(selected_year, stop_id);
    onload_line_chart(selected_year, stop_id);

    $.ajax({
        type: "GET",
        url: "../stop/stop_analysis_ajax/" + selected_year+"/" +stop_id + "/",
        beforeSend: function(){
          $(".btn-filter-now").button('loading');
          $("#stop_info_list").html('');
        },
        success: function(msg){
          // console.log(msg.stop_info);
          var stop_info_arr = msg.stop_info;

          if(msg.mode){
            $("#stop_mode_info").attr("class", 'text-center text-white p-3 bg-train');
            $("#stop_mode_info .icon").html('<i class="fas fa-fw fa-subway fa-4x"></i>');

            if(msg.mode == 1){
              $("#stop_mode_info").attr("class", 'text-center text-white p-3 bg-bus');
              $("#stop_mode_info .icon").html('<i class="fas fa-fw fa-bus fa-4x"></i>');
            }

            if(msg.mode == 3){
              $("#stop_mode_info").attr("class", 'text-center text-white p-3 bg-tram');
              $("#stop_mode_info .icon").html('<i class="fas fa-fw fa-train fa-4x"></i>');
            }
          }

          if(stop_info_arr.length> 0){
            stop_info = stop_info_arr[0];

            $("#stop_info_list").append('<tr><td><b>Stop ID</b></td><td>' + stop_info.stop_id + '</td></tr>');
            // $("#stop_info_list").append('<tr><td><b>Stop Type</b></td><td>' + stop_info.stop_type + '</td></tr>');
            $("#stop_mode_info .name").html('<h3>' + stop_info.name_short + '</h3>');
            $("#stop_info_list").append('<tr><td><b>Short Name</b></td><td>' + stop_info.name_short + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>Long Name</b></td><td>' + stop_info.name_long + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>Region</b></td><td>' + stop_info.region_name + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>Suburb</b></td><td>' + stop_info.suburb + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>Post Code</b></td><td>' + stop_info.post_code + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>State Division</b></td><td>' + stop_info.state_division + '</td></tr>');
            $("#stop_info_list").append('<tr><td><b>Local Governemt Area</b></td><td>' + stop_info.local_gov_area + '</td></tr>');

          } else {

          }

          $("#stop_info_container").show();

          // $("#stop_info_container").html(msg);

          $([document.documentElement, document.body]).animate({
              scrollTop: $("#stop_info_container").offset().top
          }, 2000);

          $(".btn-filter-now").button('reset');
        }
    });

  }

}


// charting functions

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

function onload_bar_chart_stop(year, stop_id) {
      var DATA = {};
      var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      var barChartData = {};

      $.ajax({
        url: "./barChartStopAPI/" + year + "/" + stop_id + "/",
        beforeSend: function(){
          $("#bar-graph-container").html('');
          $('#bar-graph-container').append('<canvas id="canvas-bar-graph"><canvas>');
        },
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

function onload_line_chart(selected_year, stop_id) {
      var DATA = {};
      var YEAR = {};

      var config = {};

      var line_cart_cutom = {};

      $.ajax({
        url: "./lineChartStopAPI/" + selected_year + "/" + stop_id + "/",
        success: function(the_json){
          // console.log(DATA);
          // $("#route_info_container").show();

          DATA = the_json;

          DATA.year = selected_year;

          // console.log("on change chart data", DATA.train);
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

              // console.log(config);


              $("#route_info_container").show();
              $('#line-graph-container').html("");
              // $('#canvas').remove(); // this is my <canvas> element
              $('#line-graph-container').append('<canvas id="canvas-line-graph"><canvas>');


            var ctx = canvas = document.querySelector('#canvas-line-graph').getContext('2d');
            line_cart_cutom = new Chart(ctx, config);

        }
      });
}
