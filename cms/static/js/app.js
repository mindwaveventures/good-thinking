$(".nav a").on("click", function() {
  $(".nav").find(".active").removeClass("active");
  $(this).parent().addClass("active");
});

var gtstressresultswiper;
$(document).ready(function() {
  var gtbrowsertopicswiper = new Swiper('.gt-browser-topic-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
    clickable: true,
    slideToClickedSlide: true,
    touchReleaseOnEdges: true,
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
    slideToClickedSlide: true,
    touchReleaseOnEdges: true,
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
        spaceBetween: 10,
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
    slideToClickedSlide: true,
    touchReleaseOnEdges: true,
    pagination: {
      el: '.gt-swiper-pagination-stress-browser',
      clickable: true,
    },
    breakpoints: {
      1024: {
        slidesPerView: 2,
        spaceBetween: 13,
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

  var gtswiperselfassessment = new Swiper('.gt-swiper-self-assessment', {
    slidesPerView: 1.4,
    spaceBetween: 10,
    centeredSlides: true,
    touchReleaseOnEdges: true,
    slideToClickedSlide: true,
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
        spaceBetween: 10,
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

  gtstressresultswiper = new Swiper('.gt-stress-result-swiper', {
  slidesPerView: 4,
  spaceBetween: 10,
  centeredSlides: true,
  longSwipesRatio:0.1,
  touchReleaseOnEdges: true,
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
// to get resource count on load
GetResourceCount();
// to get result block
$('.result_block').clone().appendTo(".other_resource");
});


// to change resource count value in template
GetResourceCount = function() {
if ($(window).width() <= 991) {
  $("#resource_count").html(gtstressresultswiper.slides?gtstressresultswiper.slides.length:0);
} else {
  $("#resource_count").html($('.get_resource_count').length);
}
}

// request resources based on user's answer
GetQueryResults = function(slug) {
  var url = '/results/' + slug + '/' + '?';

  $("input:checkbox[name=1]:checked").each(function() {
    url += 'q1' + '=' + $(this).val() + '&'
  });
  $("input:checkbox[name=2]:checked").each(function() {
    url += 'q2' + '=' + $(this).val() + '&'
  });
  $("input:checkbox[name=3]:checked").each(function() {
    url += 'q3' + '=' + $(this).val() + '&'
  });
  url = url.slice(0, -1);
  window.location.href = url;

}

function inViewport($el) {
  var elH = $el.outerHeight(),
    H = $(window).height(),
    r = $el[0].getBoundingClientRect(),
    t = r.top,
    b = r.bottom;
  return Math.max(0, t > 0 ? Math.min(elH, H - t) : Math.min(b, H));
}

$(window).on("scroll resize", function() {
  var visibleFooterHeight = inViewport($('#gtFooter'));
  $(".gt-footer-results").css("bottom", visibleFooterHeight + 'px');
});

var HttpClient = function() {
  this.get = function(aUrl, aCallback) {
    var anHttpRequest = new XMLHttpRequest();
    anHttpRequest.onreadystatechange = function() {
      if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
        aCallback(anHttpRequest.responseText);
    }

    anHttpRequest.open("GET", aUrl, true);
    anHttpRequest.send(null);
  }
}

// to remove resource from result page
var pathname = window.location.pathname.split( '/' );
var search_url = window.location.search?window.location.search+'&':'?';
var json_url = '/get_json_data/'+search_url+'slug='+pathname[2] +'&' + 'resource_id=';
RemoveResource = function(resource, resource_id) {
  var resource_data = '';
  var mobile_resource_data = '';
  var client = new HttpClient();
  if (json_url[json_url.length -1]=="=")
  {
   json_url += resource_id;
  } else {
   json_url +=   "," + resource_id ;
 }

  // to get resources from server
  client.get(json_url, function(response) {
    var resources = jQuery.parseJSON(response).resources;
    var mobile_resources = jQuery.parseJSON(response).mobile_resources;

    $(document).ready(function() {
      // to remove special characters from array in desktop view
      resources.forEach(function(e) {
        resource_data += e;
      });

      // desktop view
      $('.gt-highlights-stress-row').replaceWith('<div class="gt-highlights-stress-row"><div class="row other_resource">' + resource_data + '</div></div>');
      $('.result_block').clone().appendTo(".other_resource");


      // mobile view
      var current_index = gtstressresultswiper.activeIndex;
      gtstressresultswiper.removeAllSlides();
      gtstressresultswiper.appendSlide(mobile_resources);
      gtstressresultswiper.slideTo(current_index, 0);
      if ($(window).width() <= 991) {$(window).scrollTop(0);}

      // to get index for each block
      IndexCount();
    });

      // to change resource count in template
      GetResourceCount();
  });
}

// to get index value for resource block in results page
IndexCount = function() {
  // desktop view
  $(".gt-highlights-stress-row").each(function() {
    $(this).find(".gt-number").each(function(e) {
      $(".gt-number").eq(e).html('#'+(e + 1));
    });
  });
  // mobile view
  $(".mobile_resources").each(function() {
    $(this).find(".gt-number").each(function(e) {
      $(".gt-number").eq(e+($('.get_resource_count').length)).html('#'+(e + 1));
    });
  });
}

$(".gt-para-topics p").on('mousedown pointerdown', function (e){
    e.stopPropagation();
});
