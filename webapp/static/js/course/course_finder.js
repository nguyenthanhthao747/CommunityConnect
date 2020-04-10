function adjust_select2_width(){
  var existing_width = $(".select2-dropdown").css("width");
  existing_width = existing_width.replace("px");

  $(".select2-dropdown").css("left", "20px");
  console.log(parseInt(existing_width) - 50 + "px");
  window.setTimeout(function() {
    $(".select2-dropdown").css("width", parseInt(existing_width) - 50);
  }, 100);
}

$(document).ready(function () {
  $(".menu-occupations").addClass("menu-active");


  var opened_once = false;
  $('#category_filter').on('select2:open', function (e) {
    if(!opened_once){
      opened_once = true;
    }
    adjust_select2_width();
  });

  $('#category_filter').on('change', function (e) {
    submit_form();
  });
  $('#btn-search-courses').on('click', function (e) {
    submit_form();
  });

  $(document).on('keyup', 'input.select2-search__field', function(e) {
    adjust_select2_width();
  });
});

$(document).ready(function () {
  $('#category_filter').select2({
    placeholder: {
      id: '-1', // the value of the option
      text: 'Select Category'
    },
    allowClear: true,
  });

  $( ".btn-toggle-courses" ).click(function() {
    if ($(this).hasClass('exposed')) {

      $(this).html("Click here to show Courses <i class='fa fa-angle-down'></i>");
      $(this).removeClass('exposed');
      $(this).parents(".view-course-wrapper").siblings('.view-course-table').slideUp('slow');

    } else {

      $(this).html("Click here to hide Courses <i class='fa fa-angle-up'></i>");
      $(this).addClass('exposed');
      $(this).parents(".view-course-wrapper").siblings('.view-course-table').slideDown('slow');

    }
  });

});



var selected_value = "";
var search_type_flag = "p";
var redirect_urls = {}
var request_urls = {};
// request_urls["c"] = "/courses/fetch_data/";
request_urls["p"] = "/occupations/fetch_data/";
request_urls["i"] = "/providers/fetch_data/";

redirect_urls["p"] = "/courses/finder/";
redirect_urls["i"] = "/providers/";

var request_placeholder = {};
request_placeholder["p"] = "Search for courses by professions";
request_placeholder["i"] = "Search for course providers";

var request_help = {};
request_help["p"] = "eg: civil, nursing, electrical, etc.";
request_help["i"] = "eg: Skill Training Victoria, TAFE, ICP, etc.";

$.extend($.ui.autocomplete.prototype, {
    _renderMenu: function (ul, items) {
        //remove scroll event to prevent attaching multiple scroll events to one container element
        $(ul).unbind("scroll");

        var self = this;
        self._scrollMenu(ul, items);
    },

    _scrollMenu: function (ul, items) {
        var self = this;
        var maxShow = 10;
        var results = [];
        var pages = Math.ceil(items.length / maxShow);
        results = items.slice(0, maxShow);

        if (pages > 1) {
            $(ul).scroll(function () {
                if (isScrollbarBottom($(ul))) {
                    ++window.pageIndex;
                    if (window.pageIndex >= pages) return;

                    results = items.slice(window.pageIndex * maxShow, window.pageIndex * maxShow + maxShow);

                    //append item to ul
                    $.each(results, function (index, item) {
                        self._renderItem(ul, item);
                    });
                    //refresh menu
                    // console.log(self.menu);
                    // self.menu._destroy();
                    self.menu.refresh();
                    // size and position menu
                    ul.show();
                    // self._resizeMenu();
                    adjust_width();
                    // ul.position($.extend({
                    //     of: self.element
                    // }, self.options.position));
                    if (self.options.autoFocus) {
                        self.menu.next(new $.Event("mouseover"));
                    }
                }
            });
        }

        $.each(results, function (index, item) {
            self._renderItemData(ul, item);
        });
    }
});

function isScrollbarBottom(container) {
     var height = container.outerHeight();
     var scrollHeight = container[0].scrollHeight;
     var scrollTop = container.scrollTop();
     if (scrollTop >= scrollHeight - height) {
         return true;
     }
     return false;
 };

function adjust_width() {
  $('.ui-autocomplete').css('width', $("#jui-autocomplete").width() - 20 + "px");

  if($(window).width() < 769){
    // $('.ui-autocomplete').css('width', $("#jui-autocomplete").width() + 20 + "px");
    $('.ui-autocomplete').css('left', 80 + "px");
  } else {
    var existing_left = $('.ui-autocomplete').css("left");
    existing_left = existing_left.replace("px");
    $('.ui-autocomplete').css('left', parseInt(existing_left) + 30 + "px");
  }
}

$.widget( "custom.catcomplete", $.ui.autocomplete, {
	_create: function() {
		this._super();
		this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
	},
	_renderMenu: function( ul, items ) {
		var that = this,
			currentCategory = "";
		$.each( items, function( index, item ) {
			var li;
      if(item.category){
  			if ( item.category != currentCategory && search_type_flag == "p") {
  				ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
  				currentCategory = item.category;
  			}
      }
      if(item.value ==''){
        $('<li class="ui-state-disabled px-2 text-danger" style="opacity: 1;">'+item.label+'</li>').appendTo(ul);
      } else{
			     li = that._renderItemData( ul, item );
     }
			if ( item.category ) {
				li.attr( "aria-label", item.category + " : " + item.label );
			}
		});
	}
});


$(document).ready(function () {
  function log( message ) {
    setTimeout(function() { submit_form(); }, 500);
    console.log( message );
  }

  $("#jui-autocomplete").catcomplete({
    // minLength: 0,
    source: function( request, response ) {
      $.ajax({
        url: request_urls[search_type_flag],
        dataType: "json",
        type: 'POST',
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          search: request.term
        },
        success: function(data) {
          console.log(data.results);
          if(!data.results.length){

            var result = [
                {
                    label: 'No matches found for "' + request.term + '"',
                    value: ""
                }
            ];
            response(result);
          } else{
            response(data.results);
          }
        }
      });
    },
    select: function( event, ui ) {
      log(ui);
    },
    open: function(){
        adjust_width();
    }
  });
  // .data("uiAutocomplete")._renderItem = function( ul, item ) {
  //   return $("<li></li>")
  //       .data( "item.autocomplete", item )
  //       .append( "<li "+ "class='" + item.value + "'>" + item.label + "</li>" )
  //       .appendTo( ul );
  // };

  // on focus load data
  // $("#jui-autocomplete").focus(function(){
  //   //reset result list's pageindex when focus on
  //   window.pageIndex = 0;
  //   $(this).catcomplete("search");
  // });

});


function submit_form(){
  // console.log("submit_form");
  var data = $("#jui-autocomplete").val();
  var category_filter = "";
  var data_category = $('#category_filter').val();
  if(data_category !== "" && data_category != null){
    category_filter = "&cf=" + encodeURIComponent(data_category)
  }

  var search_query = "";
  if(data.length > 0){
    console.log(data);
    search_query = data;
  }
  var encoded = "/courses/?course_filter=" + encodeURIComponent(search_query);

  switch(search_type_flag) {
    case "p":
      encoded = redirect_urls[search_type_flag] + "?q=" + encodeURIComponent(search_query) + category_filter;
      break;
    default:
      break;
  }
  // console.log("perform search", search_type_flag, encoded);
  // if(search_query == ""){
  //   $('#jui-autocomplete').focus();
  // } else {
  //   location.href = encoded;
  // }


  if(search_query == ""){
    if(data_category == "" || data_category == null){
      $('#jui-autocomplete').focus();
      $("#error-get-started").find(".alert").html('Please enter keyword to search or select category!');
      $("#error-get-started").removeClass("d-none");
    } else {
      encoded_other = redirect_urls[search_type_flag] + "?cf=" + encodeURIComponent(data_category);
      location.href = encoded_other;
    }
  } else {
    if(data_category == "" || data_category == null){
      location.href = encoded;
    } else {
      encoded_other = encoded + "&cf=" + encodeURIComponent(data_category);
      location.href = encoded_other;
    }

  }
}

$(document).ready(function () {

  $('#category_filter').on('change', function(){
    submit_form();
  });

  $( "#apply_filter").click(function() {
    submit_form();
  });

  $('#jui-autocomplete').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      submit_form();
    }
  });
});
