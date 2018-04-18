$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});


$( document ).ready(function() {
  var swiper = new Swiper('.swiper1', {
    slidesPerView: 1.4,
    spaceBetween: 10,
    centeredSlides: true,
    pagination: {
      el: '.swiper-pagination1',
      clickable: true,
    },
      breakpoints: {
        1024: {
          slidesPerView: 1.4,
          spaceBetween:10,
        },
        990: {
          slidesPerView: 1.1,
          spaceBetween: 10,
        },
        800: {
          slidesPerView: 1.1,
          spaceBetween: 5,
        },
        320: {
          slidesPerView: 1.1,
          spaceBetween: 5,
        }
      }
  });
    
    
      
    var swiper2 = new Swiper('.swiper2', {
    slidesPerView: 1.2,
    spaceBetween: 10,
    centeredSlides: true,
    pagination: {
      el: '.swiper-pagination2',
      clickable: true,
    },
      breakpoints: {
        1024: {
          slidesPerView: 2,
          spaceBetween:13,
        },
        800: {
          slidesPerView: 2,
          spaceBetween: 13,
          centeredSlides: true,
        },
        640: {
          slidesPerView: 1.2,
          spaceBetween: 5,
        },
        320: {
          slidesPerView: 1.2,
          spaceBetween: 5,
    
        }
      }
  });

});