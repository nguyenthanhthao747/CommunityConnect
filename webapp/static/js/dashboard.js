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
  stops_map = L.map('mapid').setView([-37.778042, 145.134805], 9);

  // pk.eyJ1IjoiYW1pdDAwMDciLCJhIjoiY2ptNTlrZGhpMDBzejNrcXEwZnloOTAzcCJ9.1Sg9Tl2kvO0wQ5JuMStthQ

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoiYW1pdDAwMDciLCJhIjoiY2ptNTlrZGhpMDBzejNrcXEwZnloOTAzcCJ9.1Sg9Tl2kvO0wQ5JuMStthQ'
  }).addTo(stops_map);

  render_map();

  stops_map.on('moveend', function(e) {
    render_map();
  });

});

$("#select-year").change(function() {
  render_map();
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
  selected_scan_range = $("#scan_range").val();

  // update label of map
  $("#map_header").html("Top 10 busiest stops of " + selected_year + " - Map of State Victoria");
  // $("#pie_header").html("Transport Mode used in " + selected_year);


  // get near by points to the map center
  get_nearby_stops_top(center_long_lat, max_radius/1000, selected_year, selected_scan_range);
}

var oTable = {};
$(document).ready(function() {
  oTable = $('#stops-datatable').DataTable({
      "serverSide": true,
      "processing": true,
      "ajax": "/api/data/stops/?format=datatables",
      "pagingType": "full_numbers",
      "columns": [
          {"data": "name_short"},
          {"data": "name_long"},
          {"data": "stop_type"},
          {"data": "suburb"},
          {"data": "post_code"},
          {"data": "region_name"},
          {"data": "local_gov_area"},
          {"data": "state_division"},

      ]
  });

  $('#stops-datatable tbody').on('click', 'tr', function () {
    var data = oTable.row(this).data();

    console.log(data);

  });
});


function get_nearby_stops_top(center_long_lat, max_radius, year_selected, min_max){
  $("#stop_info_container").hide();
  console.log("get_nearby_stops_top", center_long_lat, max_radius);

  $.ajax({
      type: "POST",
      url: "../api/",
      data: {
          required: 'get_nearby_stops_top',
          lat: center_long_lat.lat,
          lng: center_long_lat.lng,
          max_radius: max_radius,
          year: year_selected,
          take_this_much: 10
      },
      beforeSend: function(){
        $(".btn-filter-now").button('loading');
      },
      success: function(msg){
        // console.log(msg.data);
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
              // marker_touched(e);
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
  console.log(ev.target.options);

  if(ev.target.options){
    var stop_id = ev.target.options.alt;
    var scan_count = ev.target.options.title;
    selected_year = $("#select-year").val();

    $.ajax({
        type: "GET",
        url: "../stop/stop_analysis_ajax/" + selected_year+"/" +stop_id,
        data: {

        },
        beforeSend: function(){
          $(".btn-filter-now").button('loading');
        },
        success: function(msg){
          $("#stop_info_container").show();
          $("#stop_info_container").html(msg);

          $(".btn-filter-now").button('reset');
        }
    });

  }

}
