var selected_value = "";
var search_type_flag = "s";
var redirect_urls = {}
var request_urls = {};
// request_urls["c"] = "/courses/fetch_data/";
request_urls["s"] = "/suburbs/fetch_data/";

var request_placeholder = {};
request_placeholder["p"] = "Search courses by professions";
request_placeholder["i"] = "Search for course providers";

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

  var existing_left = $('.ui-autocomplete').css('left');
  existing_left = existing_left.replace("px", "");

  var int_existing_left =  parseInt(existing_left);
  $('.ui-autocomplete').css('left', int_existing_left + 25 + "px");

  if($(window).width() < 769){
    // $('.ui-autocomplete').css('width', $("#jui-autocomplete").width() + 20 + "px");
    $('.ui-autocomplete').css('left', int_existing_left + 30 + "px");
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
			if ( item.category != currentCategory && search_type_flag == "p") {
				ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
				currentCategory = item.category;
			}
			li = that._renderItemData( ul, item );
			if ( item.category ) {
				li.attr( "aria-label", item.category + " : " + item.label );
			}
		});
	}
});

var the_table = {};

function create_datatable(){
  console.log("create_datatable");
  if ($.fn.DataTable.isDataTable('#institutes-datatable')) {
    the_table.destroy();
  }

  the_table = $("#institutes-datatable").DataTable({
    "columnDefs": [ {
           "targets": 'no-sort',
           "orderable": false,
     } ]
  });

    the_table.on('search.dt', function() {
      //number of filtered rows
      // console.log(the_table.rows( { filter : 'applied'} ).nodes().length);
      //filtered rows data as arrays
      // console.log(the_table.rows( { filter : 'applied'} ).data());

      setTimeout(function(){
        console.log($("#institutes-datatable tbody tr").length);

        reinit_map_using_table();
      }, 800);

      $(".sub-header-summary").hide();
  });
}

$(document).ready(function () {

  function log( message ) {
    console.log( message );
  }

  $("#jui-autocomplete").catcomplete({
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
          response(data.results);
        }
      });
    },
    select: function( event, ui ) {
      log(ui);
      setTimeout(function(){
        submit_form();
      }, 500);
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
  var encoded = "/suburbs/?q=" + encodeURIComponent(search_query);


  if(search_query == ""){
    $('#jui-autocomplete').focus();
  } else {
    location.href = encoded;
  }
}

$(document).ready(function () {

  $('.search_options').on('change', function(){
      // console.log($(this).val());
      search_type_flag = $(this).val();

      $("#jui-autocomplete").attr("placeholder", request_placeholder[search_type_flag]);

      setTimeout(function() { $('#jui-autocomplete').focus(); }, 500);
  });

  $( "#btn-search-institutes").click(function() {
    submit_form();
  });

  $('#jui-autocomplete').keypress(function(event){
    console.log("#jui-autocomplete keypress");
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if(keycode == '13'){
      setTimeout(function(){
        submit_form();
      }, 500);
    }
  });
});
