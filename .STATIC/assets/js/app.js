$(".nav a").on("click", function(){
   $(".nav").find(".active").removeClass("active");
   $(this).parent().addClass("active");
});


$( document ).ready(function() {
 var gtbrowsertopicswiper = new Swiper('.gt-browser-topic-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
     touchReleaseOnEdges: true,
     slideToClickedSlide: true,
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
    slideToClickedSlide: true,
    centeredSlides: true,
    pagination: {
      el: '.gt-stress-q-swiper-pagination',
      clickable: true,
    },
        navigation: {
      nextEl: '.gt-arrow-rt',
      prevEl: '.gt-arrow-lt',
            nextEl: '.gt-cta-next',
      prevEl: '.gt-cta-prev',
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
    slideToClickedSlide: true,
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
    slideToClickedSlide: true,
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


    var gtswiperselfassessment = new Swiper('.gt-swiper-self-assessment', {
    slidesPerView: 1.4,
    spaceBetween: 10,
    slideToClickedSlide: true,
    centeredSlides: true,
    pagination: {
      el: '.gt-self-assessment-swiper-pagination',
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

    
});


function inViewport($el) {
    var elH = $el.outerHeight(),
        H   = $(window).height(),
        r   = $el[0].getBoundingClientRect(), t=r.top, b=r.bottom;
    return Math.max(0, t>0? Math.min(elH, H-t) : Math.min(b, H));
}

$(window).on("scroll resize", function(){
  //console.log( inViewport($('#gtFooter')) ); // n px in viewport
    var visibleFooterHeight = inViewport($('#gtFooter'));
    $(".gt-footer-results").css("bottom", visibleFooterHeight+'px');
});

$(".gt-para-topics p").on('mousedown pointerdown', function (e){
    e.stopPropagation();
});


$('#badge').click(function() {
    $('#badge-open').show(0);
    $('#badge').hide(0);
    
});

$('.gt-right').click(function() {
    $('#badge-open').hide(0);
    $('#badge').show(0);
    
});