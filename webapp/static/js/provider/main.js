function formatResult(result) {
    if (!result.id) return result.text;

    var myElement = $(result.element);

    var markup = '<div class="custom-select-item">' +
                      '<h4 class="m-0">' + result.text + '</h4>';

    if(result.asqa_code){
      markup += '<small><b>ASQA Code:</b>' + result.asqa_code + '</small> <br />' ;
    }

    if(result.address){
      markup += '<small><b>Address: </b>' + result.address + '</small>';
    }

    markup +='</div>';

    return markup;
  }

  function formatSelection(result) {
    return result.full_name || result.text;
  }


$("#institutes-datatable tbody tr").click(function(){
      marker = markers[this.id];

      $([document.documentElement, document.body]).animate({
        scrollTop: $("#btn-search-institutes").offset().top
      }, 1000);

      var latLng = marker.getPosition(); // returns LatLng object
      map_object.setCenter(latLng);

      var infoContent = "<h5>" + marker.title + "</h5>";
      var address_row = $(this).find(".address-hidden")[0];
      // console.log($(address_row).html());
      infoContent += $(address_row).html();
      infowindow.setContent(infoContent);
      infowindow.open(map_object, marker);

});

$('#search-institutes').select2({
  placeholder: {
    id: '-1', // the value of the option
    text: 'Start typing for institutes'
  },
  escapeMarkup: function(m) {
        return m;
  },
  templateResult: formatResult,
  // templateSelection: formatSelection,
  allowClear: true,
  ajax: {
    type: 'POST',
    dataType: "json",
    url: function (params) {
      return "/providers/fetch_details/";
    },
    data: function (params) {
      var queryParameters = {
        "csrfmiddlewaretoken": '{{ csrf_token }}',
        'search': params.term,
      }

      return queryParameters;
    },
  },
  tags: true,
  createTag: function (params) {
    return {
      id: params.term,
      text: params.term,
      newOption: true
    }
  }
});

$('#search-institutes').on('select2:select', function (e) {
  submit_form();
});
$('#search-institutes').on('select2:unselecting', function (e) {
  submit_form();
});

  $( "#btn-search-institutes" ).click(function() {
    submit_form();
  });

  $("#show-regional").change(function() {
    submit_form();
  });

  function submit_form(){
    var data = $('#search-institutes').select2('data');
    var search_query = "";
    if(data.length > 0){
      console.log(data);
      search_query = data[0].text;
    }

    var search_show_regional = "";
    if($("#show-regional").is(':checked')) {
        search_show_regional = "&show-regional=1";
    } else {
        search_show_regional = "&show-regional=0";
    }

    var encoded = "/providers/?provider_filter=" + encodeURIComponent(search_query) + search_show_regional;
    // console.log(encoded);
    location.href = encoded ;

  }
