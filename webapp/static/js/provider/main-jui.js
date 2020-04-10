var selected_value = "";
var search_type_flag = "i";
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
request_help["p"] = "eg: Civil, Nursing, Electrical, etc.";
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

  // if($(window).width() < 769){
  //   // $('.ui-autocomplete').css('width', $("#jui-autocomplete").width() + 20 + "px");
  //   $('.ui-autocomplete').css('left', 80 + "px");
  // } else {
    var existing_left = $('.ui-autocomplete').css("left");
    existing_left = existing_left.replace("px");
    $('.ui-autocomplete').css('left', parseInt(existing_left) + 30 + "px");
  // }
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
      var is_regional = 0;
      if($('#show-regional').is(':checked')) {
        is_regional = 1;
      }
      console.log("is_regional " + is_regional);

      $.ajax({
        url: request_urls[search_type_flag],
        dataType: "json",
        type: 'POST',
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          search: request.term,
          is_regional: is_regional
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
  $("#jui-autocomplete").focus(function(){
    //reset result list's pageindex when focus on
    window.pageIndex = 0;
    $(this).catcomplete("search");
  });

});


function submit_form(){
  // console.log("submit_form");
  var data = $("#jui-autocomplete").val();
  var search_query = "";
  if(data.length > 0){
    console.log(data);
    search_query = data;
  }

  var data_category = $('#category_filter').val();
  var encoded = "/courses/?course_filter=" + encodeURIComponent(search_query);

  switch(search_type_flag) {
    case "p":
      encoded = redirect_urls[search_type_flag] + "?q=" + encodeURIComponent(search_query);
      break;
    case "i":
      encoded = redirect_urls[search_type_flag] + "?q=" + encodeURIComponent(search_query);
      break;
    default:
      break;
  }
  console.log("perform search", search_type_flag, encoded);
  if(search_query == ""){
    if(data_category == ""){
      $('#jui-autocomplete').focus();
      $("#error-get-started").find(".alert").html('Please enter keyword to search or select suburb!');
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

  $('#jui-autocomplete').on('keyup', function(){
    if($('#jui-autocomplete').val().length > 0){
      $("#error-get-started").addClass("d-none");
    }
  });

  $('#show-regional').on('change', function(){
      setTimeout(function() { $('#jui-autocomplete').focus(); }, 500);

      $("#error-get-started").addClass("d-none");
  });

  $( "#btn-search-institutes").click(function() {
    submit_form();
  });

  $('#jui-autocomplete').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      submit_form();
    }
  });
});
