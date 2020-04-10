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

var last_value = "";
var override_custom = true;
var select_type_courses = {
  containerCssClass: ':all:',
  dropdownCssClass : 'bigdrop',
  placeholder: {
    id: '-1', // the value of the option
    text: 'Start typing for courses'
  },
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
    // console.log("last value", params.term);
    last_value = params.term;
    override_custom = false;

    return {
      id: params.term,
      text: params.term,
      newOption: true
    }
  }
};

var select_type_professions = {
  containerCssClass: ':all:',
  dropdownCssClass : 'bigdrop',
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
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        'search': params.term,
      }

      return queryParameters;
    },
  },
  tags: true,
  createTag: function (params) {
    console.log("last value", params.term);
    last_value = params.term;
    override_custom = false;

    return {
      id: params.term,
      text: params.term,
      newOption: true
    }
  }
};

var search_type_institutions = {
  containerCssClass: ':all:',
  dropdownCssClass : 'bigdrop',
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
        "csrfmiddlewaretoken": csrfmiddlewaretoken,
        'search': params.term,
      }

      return queryParameters;
    },
  },
  tags: true,
  createTag: function (params) {
    console.log("last value", params.term);
    last_value = params.term;
    override_custom = false;

    return {
      id: params.term,
      text: params.term,
      newOption: true
    }
  }
};
var selected_value = "";
function save_data(select2_widget){
  var the_data = select2_widget.select2('data');
  if(the_data.length > 0){
    selected_value = the_data[0].text;
    console.log("value saved", selected_value);
  }

}
function restore_data(){
  console.log("restore value", selected_value);
  $('.js-data-multisource').val(selected_value); // Select the option with a value of '1'
  $('.js-data-multisource').trigger('change');
}

// $(window).resize(function() {
//   $('.js-data-multisource').css('width', "100%");
// });

$(document).ready(function () {
  var select2_widget = $('.js-data-multisource').select2(select_type_courses);

  // select2_widget.on("select2:select", function (e) {
  //   console.log("select2:select");
  //   setTimeout(function(){
  //     override_custom = true;
  //     // submit_form();
  //   }, 500);
  // });

  $(document).on("mousedown", '.js-data-multisource', function(event) {
    console.log("mousedown");
    event.preventDefault();
  });
  $(document).on("blur", '.js-data-multisource', function(event) {
    console.log("blur");
    event.preventDefault();
  });
  $(document).on("focus", '.js-data-multisource', function(event) {
    console.log("focus");
    event.preventDefault();
  });

  $(document).on("keydown", '.select2-search__field', function(event) {

    if (event.keyCode === 13) {
      console.log('keydown', event.keyCode);
        setTimeout(function(){
          // override_custom = true;
          submit_form();
        }, 400);
    }
  });

  select2_widget.on("select2:unselecting", function (e) {
    override_custom = true;
  });
  // select2_widget.on("select2:close", function (e) {
  //   console.log("select2:close");
  //   if (!override_custom){
  //
  //     setTimeout(function(){
  //       console.log("override_custom", last_value);
  //       if(last_value != ""){
  //         $('.js-data-multisource').val(last_value); // Select the option with a value of '1'
  //         $('.js-data-multisource').trigger('change');
  //       }
  //
  //     }, 500);
  //
  //   }
  // });
  var search_type_flag = "c";

    jQuery("#search-type-courses").click(function(e){
      // console.log("#search-type-courses");
      $(".btn-options-filter").text("Courses");
      search_type_flag = "c"; // for courses

      save_data(select2_widget);
      select2_widget.select2("destroy").select2(select_type_courses);
      restore_data();

      e.preventDefault();
    });

    jQuery("#search-type-professions").click(function(e){
      // console.log("#search-type-professions");
      $(".btn-options-filter").text("Professions");
      search_type_flag = "p"; // for professions

      save_data(select2_widget);
      select2_widget.select2("destroy").select2(select_type_professions);
      restore_data();

      e.preventDefault();
    });

    jQuery("#search-type-institutions").click(function(e){
      // console.log("#search-type-institutions");
      $(".btn-options-filter").text("Institutions");
      search_type_flag = "i"; // for institutions

      save_data(select2_widget);
      select2_widget.select2("destroy").select2(search_type_institutions);
      restore_data();

      e.preventDefault();
    });

    $( "#btn-get-started").click(function() {
      submit_form();
    });

    function submit_form(){
      console.log("submit_form");

      var data = select2_widget.select2('data');
      var search_query = "";
      if(data.length > 0){
        console.log(data);
        search_query = data[0].text;
      }
      var encoded = "/courses/?course_filter=" + encodeURIComponent(search_query);

      switch(search_type_flag) {
        case "c":
          encoded = "/courses/?course_filter=" + encodeURIComponent(search_query);
          break;
        case "p":
          encoded = "/occupations/?occupation_filter=" + encodeURIComponent(search_query);
          break;
        case "i":
          encoded = "/providers/?provider_filter=" + encodeURIComponent(search_query);
          break;
        case "s":
          encoded = "/courses/?course_filter=" + encodeURIComponent(search_query);
          break;
        default:
          // code block
      }
      console.log("perform search", search_type_flag, encoded);
      if(search_query == ""){
        $('.js-data-multisource').focus();
      } else {
        location.href = encoded ;
      }
    }
});




  $(function() {
    function log( message ) {
      console.log( message );
    }

    $( "#jui-autocomplete" ).autocomplete({
      source: function( request, response ) {
        $.ajax({
          url: "/courses/fetch_data/",
          dataType: "json",
          type: 'POST',
          data: {
            term: request.term,
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            search: request.term
          },
          success: function( data ) {
            // console.log(data.results);
            response( data.results );
          }
        });
      },
      select: function( event, ui ) {
        log( "Selected: " + ui.item.value + " aka " + ui.item.id );
      },
      open: function(){
          $('.ui-autocomplete').css('width', $("#jui-autocomplete").width() - 20 + "px"); // HERE
      }
    }).focus(function(){
        $(this).autocomplete("search");
    });
  });
