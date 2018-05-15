$(".nav a").on("click", function() {
  $(".nav").find(".active").removeClass("active");
  $(this).parent().addClass("active");
});


$(document).ready(function() {
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

  var gtstressresultswiper = new Swiper('.gt-stress-result-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
    allowSlidePrev: 1,
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

  stress_result_swiper();

});



function stress_result_swiper() {
  var gtstressresultswiper = new Swiper('.gt-stress-result-swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
    allowSlidePrev: 1,
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

  return gtstressresultswiper.slides.length;
}

function GetQueryResults(slug) {

  var query_result = [];
  var url = "";

  $("input:checkbox[name=1]:checked").each(function() {
    query_result.push({
      query: 'q1',
      value: $(this).val()
    });
  });
  $("input:checkbox[name=2]:checked").each(function() {
    query_result.push({
      query: 'q2',
      value: $(this).val()
    });
  });
  $("input:checkbox[name=3]:checked").each(function() {
    query_result.push({
      query: 'q3',
      value: $(this).val()
    });
  });
  query_result.forEach(function(e) {
    url += e.query + "=" + e.value + "&";
  });
  url = url.trim("&");
  window.location.href = '/results/' + slug + '/' + '?' + url;

}

function RemoveResource(resource, screen_size) {
  $('.' + resource).remove();

  if (screen_size == 'mobile') {
    $("#resource_count").html(stress_result_swiper());
  } else {
    $("#resource_count").html($('.get_resource_count').length);
  }
}
