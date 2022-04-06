function updateScroll(){
  var element = document.getElementById("chat");
  element.scrollTop = element.scrollHeight;
}
updateScroll();
$("#sendmessage").on("submit",function(event){
event.preventDefault();
var message = $("#messagebox").val();$("#chat").html($("#chat").html()+'<li class="me"> <div class="entete"> <h2>You</h2> <span class="status blue"></span> </div> <div class="triangle"></div> <div class="message">'+message+'</div> </li>');
updateScroll();
$("#messagebox").val("");
$.ajax({
    type:"POST",
    url:"/chat/",
    data:{
      message:message,
      csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
    },
    
    success:function(result){
      $("#chat").html($("#chat").html()+'<li class="you"> <div class="entete"> <span class="status green"></span> <h2>Deppy</h2> <h3></h3> </div> <div class="triangle"></div> <div class="message">'+result+' </div> </li>');
      updateScroll();
      $("#messagebox").val("");
    }
});


});

$("#logoutbtn").on("click",function(event){
  event.preventDefault();
  $.ajax({
    type:"POST",
    url:"/logout/",
    data:{
      action:"logout",
      csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val(),
    },
    
    success:function(result){
      if(result=="logoutsuccessful"){
        window.location.reload();
      }else{
        alert("error");
      }
    }
});

})




$('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#mainListDiv").toggleClass("show_list");
    $("#mainListDiv").fadeIn();

});

// Input Lock
$('textarea').blur(function () {
    $('#hire textarea').each(function () {
        $this = $(this);
        if ( this.value != '' ) {
          $this.addClass('focused');
          $('textarea + label + span').css({'opacity': 1});
        }
        else {
          $this.removeClass('focused');
          $('textarea + label + span').css({'opacity': 0});
        }
    });
});

$('#hire .field:first-child input').blur(function () {
    $('#hire .field:first-child input').each(function () {
        $this = $(this);
        if ( this.value != '' ) {
          $this.addClass('focused');
          $('.field:first-child input + label + span').css({'opacity': 1});
        }
        else {
          $this.removeClass('focused');
          $('.field:first-child input + label + span').css({'opacity': 0});
        }
    });
});

$('#hire .field:nth-child(2) input').blur(function () {
    $('#hire .field:nth-child(2) input').each(function () {
        $this = $(this);
        if ( this.value != '' ) {
          $this.addClass('focused');
          $('.field:nth-child(2) input + label + span').css({'opacity': 1});
        }
        else {
          $this.removeClass('focused');
          $('.field:nth-child(2) input + label + span').css({'opacity': 0});
        }
    });
});
