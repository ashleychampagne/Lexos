$(function() {
	$(".navbaroption").click(function() {
		$(this).next("input").click();
	});

	function displayFileName(ev) {
		var files = ev.target.files || ev.dataTransfer.files;

		for (var i = 0, file; file = files[i]; i++) {
			var label = $("#"+ev.target.id).parent().find("#"+ev.target.id+"bttnlabel");
			label.html(file.name);
			label.css('color', '#00B226');
			$("#usecache"+ev.target.id).attr('disabled', 'disabled');
		}
	}

	$("#swfileselect").change(displayFileName);
	$("#lemfileselect").change(displayFileName);
	$("#consfileselect").change(displayFileName);
	$("#scfileselect").change(displayFileName);

	$(".bttnfilelabels").click( function() {
		var filetype = $(this).attr('id').replace('bttnlabel', '');
		if ($("#usecache"+filetype).attr('disabled') != 'disabled') {
			$(this).css('color', '#FF0000');
			$(this).text($(this).text().replace('(using stored)', ''));
			$("#usecache"+filetype).attr('disabled', 'disabled');
		}
	});

	//-----------------------------------------------------
	var timeToToggle = 300;
	$("#stopwords").click( function() {
		$("#stopwordinput").slideToggle(timeToToggle);
	});
	$("#prettystopwordsupload").click( function() {
		$("#swfileselect").click();
	});
	//-----------------------------------------------------
	$("#lemmas").click( function() {
		$("#lemmainput").slideToggle(timeToToggle);
	});
	$("#prettylemmasupload").click( function() {
		$("#lemfileselect").click();
	});
	//-----------------------------------------------------
	$("#consolidations").click( function() {
		$("#consolidationsinput").slideToggle(timeToToggle);
	});
	$("#prettyconsolidationsupload").click( function() {
		$("#consfileselect").click();
	});
	//-----------------------------------------------------
	$("#specialchars").click( function() {
		$("#specialcharsinput").slideToggle(timeToToggle);
	});
	$("#prettyspecialcharsupload").click( function() {
		$("#scfileselect").click();
	});
});



$(function() {
	var timeToToggle = 100;
	$("#punctbox").click( function() {
		if ($(this).children('input').is(':checked')) {
			$("#aposhyph").fadeOut(timeToToggle);
		}
		else {
			$("#aposhyph").fadeIn(timeToToggle);
		}
	});
});

$(function() {
	$(document).tooltip({
		position:{
			relative: true,
			at: "center top-500", // location on the mouse
								  // Negative horizontal is left, negative vertical is up 
			my: "center bottom",  // location on the tooltip popup window
			collision: "fit"
		}
	});
});