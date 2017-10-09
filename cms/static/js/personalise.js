var personaliseDiv = document.getElementById('elm-personalise');

if (personaliseDiv) {
  var height = getHeight();
  var issue_tags = getTags('q1')
  var reason_tags = getTags('q2')
  var content_tags = getTags('q3')
  var issue_label = document.getElementById('q1_label').innerHTML;
  var reason_label = document.getElementById('q2_label').innerHTML;
  var content_label = document.getElementById('q3_label').innerHTML;

  var selected_tags = selectedTags(getQuery('q1', 'q2', 'q3'));

  var app = Elm.Main.embed(personaliseDiv, {
    issue_tags: issue_tags,
    content_tags: content_tags,
    reason_tags: reason_tags,
    issue_label: issue_label,
    reason_label: reason_label,
    content_label: content_label,
    selected_tags: selected_tags,
    order: getOrder(),
    search: getQuery('q').q[0] || "",
    page: getPage(),
    height: height + 10 // A little extra space needed so tags don't get cut off
  });

  function getTags(name) {
    return Array.prototype.map.call(personaliseDiv.querySelectorAll("input[name='" + name + "']"), function(el){
      return el.value;
    });
  }

  function getQuery() {
    var qs = window.location.href.split("?")[1];
    var query = {};

    Array.prototype.forEach.call(arguments, function(a) {
      query[a] = [];
      var reg = new RegExp("(?:^" + a + "|&" + a + ")=([^&#]+)", "g")
      var arr;
      var splitreg = /(?:%20|\+)/g;

      while ((myArray = reg.exec(qs)) !== null) {
        query[a].push(myArray[1].replace(splitreg, ' '));
      }
    });

    if(window.location.href.split('/').length === 6) {
      query['q1'] = [window.location.href.split('/')[4].replace(/-/g, " ")];
    };

    return query;
  }

  function selectedTags(queryObj) {
    var selected = JSON.parse(localStorage.getItem('selected_tags_' + getPage())) || [];

    for (var type in queryObj) {
      tags = queryObj[type].map(function(el) {
        return {tag_type: type, name: el};
      });
      selected = selected.concat(tags);
    }
    return selected;
  }

  app.ports.listeners.subscribe(function(res) {
    requestAnimationFrame(function() {
      likeListeners();
      feedbackLoopListener();
      swipeListeners();
      analyticsListeners();
      mobileProsAndCons();
    });
  });

  app.ports.selectTag.subscribe(function(tag) {
    var selectedTags = JSON.parse(localStorage.getItem('selected_tags_' + getPage())) || [];

    for (var i = 0; i < selectedTags.length; i++) {
      if (selectedTags[i].tag_type === tag.tag_type && selectedTags[i].name === tag.name) {
        selectedTags.splice(i, 1);
        break;
      } else if (i === selectedTags.length - 1) {
        selectedTags.push(tag);
        break;
      }
    }

    updateUrl(tag);

    localStorage.setItem('selected_tags_' + getPage(), JSON.stringify(selectedTags));
    app.ports.updateTags.send(selectedTags);
  });

  app.ports.changeOrder.subscribe(function(order) {
    localStorage.setItem('ldmw_resource_order', order);
  });

  function swipe(el, callback){
    var swipedir;
    var startX;
    var startY;
    var distX;
    var distY;
    var threshold = 50;
    var restraint = 100;

    el.addEventListener('touchstart', function(e){
      var touchobj = e.changedTouches[0];
      swipedir = 'none';
      startX = touchobj.pageX;
      startY = touchobj.pageY;

    }, false);

    el.addEventListener('touchend', function(e){
      var touchobj = e.changedTouches[0]
      distX = touchobj.pageX - startX;
      distY = touchobj.pageY - startY;

      if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint) {
        swipedir = (distX < 0) ? 'left' : 'right';
      }

      callback(swipedir);
    }, false);
  }

  function swipeListeners() {
    selectAll('.tag-card').forEach(function(el) {
      swipe(el , function(swipedir){
        app.ports.swipe.send(swipedir);
      });
    });

    selectAll('.tip-card').forEach(function(el) {
      swipe(el , function(swipedir){
        app.ports.tipSwipe.send(swipedir);
      });
    });

    var nextButtons = selectAll('.tip-next');
    var prevButtons = selectAll('.tip-previous');

    nextButtons.forEach(function(el, i) {
      if (i === nextButtons.length - 1) {
        el.style.display = "none";
      } else {
        el.addEventListener('click', function(e) {
          app.ports.tipSwipe.send("left");
        });
      }
    });

    prevButtons.forEach(function(el, i) {
      if (i === 0 && prevButtons.length > 1) {
        el.style.display = "none";
      } else {
        el.addEventListener('click', function(e) {
          app.ports.tipSwipe.send("right");
        });
      }
    });
  }

  function getPage() {
    var page = window.location.href.split('/')[3];
    if (!page || page.indexOf('?') > -1) {
      page = 'home';
    }
    return page;
  }

  function getOrder() {
    return (
      window.location.href.split("order=")[1]
      || localStorage.getItem('ldmw_resource_order')
      || "relevance"
    );
  }

  function updateUrl(tag) {
    var jointTag = tag.name.replace(/\s/g, '%20').replace(/'/g, '%27');
    var baseUrl = window.location.origin + '/' + window.location.pathname.split('/')[1] + '/';
    var prefix;
    var querystring = "";
    var tags = {};

    ['q1', 'q2', 'q3'].forEach(function(el) {
      tags[el] = getTagsOfType(el);
    });

    if (
      tags.q1.length === 0 && !tagSelected(tag) &&
      tags.q2.length === 0 && tags.q3.length === 0 && tag.tag_type === 'q1'
    ) {
      /* No tags are selected & this is an issue tag - make friendly url */
      querystring = tag.name.replace(/\s/g, '-').replace(/'/g, '%27');
    } else if (tags.q1.length === 1 && tagSelected(tag) && tags.q2.length === 0 && tags.q3.length === 0) {
      /* Currently one issue tag selected, and has been deselected - remove friendly url*/
      querystring = "";
    } else {
      /* Multiple tags selected - build query string with parameters */

      /* Build query with already selected tags,
      do not include new tag if it was already selected */
      for (var type in tags) {
        tags[type].forEach(function(el) {
          if (tag.tag_type !== type || jointTag !== el || !tagSelected({tag_type: type, name: el})) {
            prefix = querystring === "" ?  "?" : "&";
            querystring += prefix + type + "=" + el;
          }
        });
      }

      /* Add newly selected tag */
      if (!tagSelected(tag)) {
        prefix = querystring === "" ?  "?" : "&";
        querystring += prefix + tag.tag_type + "=" + tag.name;
      }
    }

    history.replaceState(null, null, baseUrl + querystring);
  }

  function getTagsOfType(type) {
    var singleIssueReg = new RegExp('https*:\/\/[^\/]+\/[^\/]+\/([^\/?]+)\/*');
    var reg = new RegExp(type + "=([^&#]+)", "g");
    var res;
    var matches = [];
    var singleIssue = window.location.href.match(singleIssueReg);

    if (type === "q1" && singleIssue) {
      matches.push(singleIssue[1].replace(/-/g, ' '));
    }

    while ((res = reg.exec(window.location.href)) !== null) {
      matches.push(res[1]);
    }

    return matches;
  }

  function tagSelected(tag) {
    var jointTag = tag.name.replace(/\s/g, '%20').replace(/'/g, '%27');
    var hyphenTag = tag.name.replace(/\s/g, '-').replace(/'/g, '%27');
    var reg = new RegExp(tag.tag_type + "=" + jointTag + "(&|$)");
    var singleIssueReg = new RegExp('https*:\/\/[^\/]+\/[^\/]+\/' + hyphenTag + '\/*');

    var selectedTags = JSON.parse(localStorage.getItem('selected_tags_' + getPage())) || [];

    for (var i = 0; i < selectedTags.length; i++) {
      if (selectedTags[i].tag_type === tag.tag_type && selectedTags[i].name == tag.name) {
        return true;
      }
    }

    return reg.test(window.location.href) || singleIssueReg.test(window.location.href);
  }

  function getHeight() {
    return Math.max.apply(null, selectAll('.filter-block .tag-container').map(function(el) {
      return el.clientHeight;
    }));
  }

  swipeListeners();
}
