$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});


$( document ).ready(function() {
  var swiper = new Swiper('.swiper5', {
    slidesPerView: 4,
    spaceBetween: 10,
    pagination: {
      el: '.swiper-pagination5',
      clickable: true,
    },
      breakpoints: {
        1024: {
          slidesPerView: 4,
          spaceBetween: 10,
        },
        1000: {
          slidesPerView: 1.1,
          spaceBetween: 5,
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

});