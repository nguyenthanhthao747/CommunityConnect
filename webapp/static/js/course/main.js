$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $('#category_filter').select2({
      placeholder: {
        id: '-1', // the value of the option
        text: 'Select Suburb'
      },
      allowClear: true,
    });

    $('#search-courses').select2({
      dropdownCssClass : 'bigdrop',
      placeholder: {
        id: '-1', // the value of the option
        text: 'Start typing for courses'
      },
      // minimumInputLength: 1,
      allowClear: true,
      ajax: {
        type: 'POST',
        dataType: "json",
        url: function (params) {
          return "/courses/fetch_details/";
        },
        data: function (params) {
          var queryParameters = {
            "csrfmiddlewaretoken": csrfmiddlewaretoken,
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

    $('#search-courses, #category_filter').on('select2:select', function (e) {
      submit_form();
    });
    var clear_form = false;
    $('#search-courses').on('select2:unselecting', function (e) {
      clear_form = true;
      submit_form();
    });

    $( "#btn-search-courses").click(function() {
      submit_form();
    });

    $("#gov-subsidized").change(function() {
      setTimeout(function(){ submit_form(); }, 600);
    });

    $("#apprenticeship").change(function() {
      submit_form();
    });

    $("#traineeship").change(function() {
      submit_form();
    });

    function submit_form(){
      console.log("submit_form");

      var data = $('#search-courses').select2('data');
      var search_query = "";
      if(data.length > 0){
        console.log(data);
        search_query = data[0].text;
      }

      var category_selected = $("#category_filter").val();
      var category_filter = "";

      if(category_selected !== ""){
        category_filter = "&cf=" + encodeURIComponent(category_selected)
      }

      var search_gov = "";
      if($("#gov-subsidized").is(':checked')) {
          search_gov = "&subsidized=1";
      }

      var search_appre = "";
      if($("#apprenticeship").is(':checked')) {
          search_appre = "&apprenticeship=1";
      }

      var search_trainee = "";
      if($("#traineeship").is(':checked')) {
          search_trainee = "&traineeship=1";
      }

      var encoded = "/courses/?q=" + encodeURIComponent(search_query) + search_gov + search_appre + search_trainee + category_filter;
      // console.log(encoded);

      if(search_query == "" & search_gov == "" & search_appre == "" & search_trainee == ""){
        $('#search-courses').focus();

        if (clear_form){
          encoded = "/courses/";
          location.href = encoded ;
        }
      } else {
          location.href = encoded ;
      }
    }
});
