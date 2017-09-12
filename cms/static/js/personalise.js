var personaliseDiv = document.getElementById('elm-personalise');

var issue_tags = getTags('issue')
var content_tags = getTags('content')
var reason_tags = getTags('reason')
var issue_label = document.getElementById('issue_label').innerText;
var reason_label = document.getElementById('reason_label').innerText;
var content_label = document.getElementById('content_label').innerText;

var selected_tags = selectedTags(getQuery('issue', 'content', 'reason'));

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
  page: getPage()
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
      query[a].push(myArray[1].split(splitreg).join(' '));
    }
  });

  if(window.location.href.split('/').length == 6) {
    query['issue'] = [window.location.href.split('/')[4].split("-").join(" ")];
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
    proConListeners();
    feedbackLoopListener();
    swipeListeners();
    analyticsListeners();
  });
});

app.ports.selectTag.subscribe(function(tag) {
  var selectedTags = JSON.parse(localStorage.getItem('selected_tags_' + getPage()));

  for (var i = 0; i < selectedTags.length; i++) {
    if (selectedTags[i].tag_type === tag.tag_type && selectedTags[i].name == tag.name) {
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
  var jointTag = tag.name.split(' ').join('%20');
  var reg = new RegExp("&*" + tag.tag_type + "=" + jointTag + "(&|$)");
  var newUrl = window.location.href;
  var prefix;

  if (window.location.href.indexOf('?') > -1) {
    prefix = "&";
  } else {
    prefix = "?";
  }

  if (tagSelected(tag)) {
    newUrl = window.location.href.replace(reg, "&");
  } else {
    newUrl += prefix + tag.tag_type + "=" + tag.name;
  }

  history.replaceState(null, null, newUrl);
}

function tagSelected(tag) {
  var jointTag = tag.name.split(' ').join('%20');
  var reg = new RegExp(tag.tag_type + "=" + jointTag + "(&|$)");

  var selectedTags = JSON.parse(localStorage.getItem('selected_tags_' + getPage()));

  for (var i = 0; i < selectedTags.length; i++) {
    if (selectedTags[i].tag_type === tag.tag_type && selectedTags[i].name == tag.name) {
      return true;
    }
  }

  return reg.test(window.location.href);
}

swipeListeners();
