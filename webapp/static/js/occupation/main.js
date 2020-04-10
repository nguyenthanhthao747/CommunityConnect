$(document).ready(function () {
  $(".menu-occupations").addClass("menu-active");
});



  $(document).ready(function () {
    $('#search-occupation').select2({
      placeholder: {
        id: '-1', // the value of the option
        text: 'Start typing for suggestions'
      },
      allowClear: true,
      ajax: {
        type: 'POST',
        dataType: "json",
        url: function (params) {
          return "/occupations/fetch_details/";
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

      $('#search-occupation').on('select2:select', function (e) {
        submit_form();
      });
      $('#search-occupation').on('select2:unselecting', function (e) {
        submit_form();
      });


      $( "#btn-search-occupation" ).click(function() {
        submit_form();
      });

      $("#high_demand").change(function() {
        submit_form();
      });

      function submit_form(){
        var data = $('#search-occupation').select2('data');
        var search_query = "";
        if(data.length > 0){
          console.log(data);
          search_query = data[0].text;
        }

        var high_demand = "";
        if($("#high_demand").is(':checked')) {
            high_demand = "&high_demand=1";
        } else {
            high_demand = "&high_demand=0";
        }

        var encoded = "/occupations/?occupation_filter=" + encodeURIComponent(search_query) + high_demand;
        // console.log(encoded);

        if(search_query == "" & high_demand){
          $('#search-occupation').focus();
        } else {
          location.href = encoded ;
        }

      }
  });
