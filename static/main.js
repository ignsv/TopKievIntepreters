
$(function(){
	$(window).scroll(function() {
		if ($(window).width() <= '768'){
			var top = $(document).scrollTop();
			if (top < 48) $(".flashes-wrapper").css({top: '0px', position: 'absolute'});
			else $(".flashes-wrapper").css({top: '0px', position: 'fixed'});
		}
	});

});

$( window ).load(function() {
	if ($(window).width() <= '768'){
		$('.cover').unbind('mouseenter mouseleave');
		var top = $(document).scrollTop();
		if (top < 48) $(".flashes-wrapper").css({top: '0px', position: 'absolute'});
		else $(".flashes-wrapper").css({top: '0px', position: 'fixed'});
	}
	if ($(window).width() > '768'){
		$(".cover").hover(function(e) { 
			$(this).css("background-color",e.type === "mouseenter"?"transparent":"rgba(7, 72, 91, 0.5)");
			$(this).children(".xcover").css("visibility",e.type === "mouseenter"?"visible":"hidden");
			$(this).children(".xcover").css("opacity",e.type === "mouseenter"?"1":"0");
			$(this).children("h3").css("display",e.type === "mouseenter"?"none":"block") ;
		})
	}
})

$( window ).resize(function() {
	if ($(window).width() <= '768'){
		$('.cover').unbind('mouseenter mouseleave');
	}
	if ($(window).width() > '768'){
		$(".cover").hover(function(e) { 
			$(this).css("background-color",e.type === "mouseenter"?"transparent":"rgba(7, 72, 91, 0.5)");
			$(this).children(".xcover").css("visibility",e.type === "mouseenter"?"visible":"hidden");
			$(this).children(".xcover").css("opacity",e.type === "mouseenter"?"1":"0");
			$(this).children("h3").css("display",e.type === "mouseenter"?"none":"block") ;
		})
	}
});

$(document).ready(function(){
	/*
	$('ul[data-type="background"]').each(function(){
		var $bgobj = $(this); // создаем объект
		$(window).scroll(function() {
			var yPos = -($(window).scrollTop() / $bgobj.data('speed')); // вычисляем коэффициент 
			// Присваиваем значение background-position
			var coords = 'center '+ yPos + 'px';
			// Создаем эффект Parallax Scrolling
			$bgobj.css({ backgroundPosition: coords });
		});
	});
*/
	$('#services-nav').click(function(){
		$("#services-ul").css({opacity: '1'});
	});

	scrollDuration=350;
	$('.top').click(function(event) {
		event.preventDefault();
			$('html, body').animate({
				scrollTop: 0}, scrollDuration);
	});

	$(document.body).on('click','.flashes-close', function(event) {
		$(".flashes-wrapper").css("display", "none");	
	});
	
	$(".cover").click(function(event) {
		$(".cover").css("background", "rgba(7, 72, 91, 0.5)");
		$(".xcover").css({visibility: 'hidden', opacity: '0'});
		$(".cover").children("h3").css("display", "block");
		$(this).css("background", "transparent");
		$(this).children(".xcover").css({visibility: 'visible', opacity: '1'});
		$(this).children("h3").css("display", "none");
			
	});

});

$(function(){
	$('#top-nav').slicknav();
});