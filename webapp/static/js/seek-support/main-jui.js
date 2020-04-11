var selected_value = "";
var search_type_flag = "p";
var redirect_urls = {}
var request_urls = {};
// request_urls["c"] = "/courses/fetch_data/";
request_urls["p"] = "/occupations/fetch_data/"; // volunteers
request_urls["i"] = "/providers/fetch_data/"; // goods

request_urls["s"] = "/suburbs/fetch_suburbs/"; // address search


redirect_urls["p"] = "/volunteers/finder/";
redirect_urls["i"] = "/essentials/finder/";

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

function adjust_width(elem) {
  $('.ui-autocomplete').css('width', $(elem).width() - 20 + "px");

  if($(window).width() < 769){
    // $('.ui-autocomplete').css('width', $("#volunteer-query").width() + 20 + "px");
    $('.ui-autocomplete').css('left', 80 + "px");
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
      // if(item.category){
  		// 	if ( item.category != currentCategory && search_type_flag == "p") {
  		// 		ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
  		// 		currentCategory = item.category;
  		// 	}
      // }
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
    //setTimeout(function() { submit_form(); }, 500);
    console.log( message );
  }

  $("#volunteer-query").catcomplete({
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
      // log(ui);
    },
    open: function(){
        adjust_width($("#volunteer-query"));
    }
  });


  $("#product-query").catcomplete({
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
      // log(ui);
    },
    open: function(){
        adjust_width($("#product-query"));
    }
  });

  // on focus load data
  $("#volunteer-query").focus(function(){
    //reset result list's pageindex when focus on
    window.pageIndex = 0;
    $(this).catcomplete("search");
    search_type_flag = 'p';
  });

  $("#product-query").focus(function(){
    //reset result list's pageindex when focus on
    window.pageIndex = 0;
    $(this).catcomplete("search");
    search_type_flag = 'i';
  });

});


function submit_form(){
  // console.log("submit_form");
  var queryBuilder = "";
  var search_query = "";
  var encoded = "";

  switch(search_type_flag) {
    case "p":
      search_query = $("#volunteer-query").val();
      queryBuilder += "?q=" + encodeURIComponent(search_query);
      queryBuilder += "&category=" + encodeURIComponent($("#volunteer-category").val());
      queryBuilder += "&location=" + encodeURIComponent($("#volunteer-location").val());
      break;
    case "i":
      search_query = $("#product-query").val();
      queryBuilder += "?q=" + encodeURIComponent(search_query);
      queryBuilder += "&category=" + encodeURIComponent($("#product-category").val());
      queryBuilder += "&location=" + encodeURIComponent($("#product-location").val());
      break;
    default:
      break;
  }
  encoded = redirect_urls[search_type_flag] + queryBuilder;

  console.log("perform search", search_type_flag, encoded);
  if(search_query == ""){
    $('#volunteer-query').focus();
    // $("#error-get-started").html('<a class="text-danger small">Please enter keyword to search!</a>');
    $("#error-get-started").find(".alert").html('Please enter keyword to search!');
    $("#error-get-started").removeClass("d-none");
  } else {
    location.href = encoded;
  }
}

$(document).ready(function () {

  // $('#volunteer-query').on('keyup', function(){
  //   if($('#volunteer-query').val().length > 0){
  //     $("#error-get-started").addClass("d-none");
  //   }
  // });
  //
  // $('#product-query').on('keyup', function(){
  //   if($('#product-query').val().length > 0){
  //     $("#error-get-started").addClass("d-none");
  //   }
  // });

  $( "#btn-volunteer-search").click(function() {
    search_type_flag = 'p';
    submit_form();
  });

  $( "#btn-product-search").click(function() {
    search_type_flag = 'i';
    submit_form();
  });

  $('#volunteer-query').keypress(function(event){
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      submit_form();
    }
  });

  $("#volunteer-location").catcomplete({
    // minLength: 0,
    source: function( request, response ) {
      $.ajax({
        url: request_urls["s"],
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
      // log(ui);
    },
    open: function(){
        adjust_width($("#volunteer-location"));
    }
  });


  $("#product-location").catcomplete({
    // minLength: 0,
    source: function( request, response ) {
      $.ajax({
        url: request_urls["s"],
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
      // log(ui);
    },
    open: function(){
        adjust_width($("#product-location"));
    }
  });


});
