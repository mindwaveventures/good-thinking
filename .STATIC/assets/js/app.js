$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});


$( document ).ready(function() {
 var gtbrowsertopicswiper = new Swiper('.gt-browser-topic-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
      clickable: true,
    pagination: {
      el: '.gt-swiper-pagination-browser-topic',
      clickable: true,
    },
      breakpoints: {
        1024: {
          slidesPerView: 4,
          spaceBetween: 10,
        },
        990: {
          slidesPerView: 2.6,
          spaceBetween: 10,
        },
        800: {
          slidesPerView: 1.21,
          spaceBetween: 5,
        },
        320: {
          slidesPerView: 1.1,
          spaceBetween: 5,
        }
      }
  });
      
    var gtswiperstressq = new Swiper('.gt-swiper-stress-q', {
    slidesPerView: 1.4,
    spaceBetween: 10,
    centeredSlides: true,
    pagination: {
      el: '.gt-stress-q-swiper-pagination',
      clickable: true,
    },
        navigation: {
      nextEl: '.gt-arrow-rt',
      prevEl: '.gt-arrow-lt',
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
    
    
     var gtswiperstressbrowser = new Swiper('.gt-swiper-stress-browser', {
    slidesPerView: 1.2,
    spaceBetween: 10,
    centeredSlides: true,
    pagination: {
      el: '.gt-swiper-pagination-stress-browser',
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
    
     var gtstressresultswiper = new Swiper('.gt-stress-result-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
      allowSlidePrev:1,
    pagination: {
      el: '.gt-swiper-pagination-stress-result',
      clickable: true,
    },
           navigation: {
      nextEl: '.gt-arrow-block',
      prevEl: '',
    },
      breakpoints: {
        1024: {
          slidesPerView: 4,
          spaceBetween: 10,
        },
        1000: {
          slidesPerView: 1.1,
          spaceBetween: 10,
        },
        800: {
          slidesPerView: 1.1,
          spaceBetween: 10,
        },
        320: {
          slidesPerView: 1.1,
          spaceBetween: 10,
        }
      }
  });


    
    
});