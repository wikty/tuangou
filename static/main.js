jQuery(function($){
  var pos = $('#pageheader').offset();
  pos.top -= 100;
  pos.left += 100;
  $('<h1>团购搜</h1>').insertBefore('#pageheader').offset(pos);

  $('#search').autocomplete({
			source: '{{ keywords_url }}',
			minLength: 2,
			select: function(event, ui) {  
            	//$(".result").remove();
            	//$("#search").before("<div class='result'></div>");  
            	//$(".result").html(ui.item.value);  
            	//$(ui.item).addClass('selected');
              //alert(ui.item)
        	}
		})
});