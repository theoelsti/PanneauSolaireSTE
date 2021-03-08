// C le script pour le flou et tout tavu
$(document).ready(function(){

    $("#buttonToPanel").on("click", function() {
        window.location.href = '#welcomePanel';

    });
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    // $(window).scroll(function() {
    //     if(isMobile){

       
    //     var scrollTop = $(this).scrollTop();
    //     $('#top').css({
    //       opacity: function() {
    //         var elementHeight = $(this).height();
    //         return 0 + (elementHeight - scrollTop) / elementHeight;
    //       }
    //     });
    //     $('#panel').css({
    //         opacity: function() {
    //           var elementHeight = $('#meteoChart').height();
    //           return 1 - (elementHeight - scrollTop) / elementHeight;
    //         }
    //       });
    //     }
    //   });

})        

