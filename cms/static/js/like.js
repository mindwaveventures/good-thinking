if (isNotIE8()) {
  function likeListeners() {
    selectAll([".like-form", ".dislike-form", ".resource-feedback"]).forEach(function(el) {
      el.addEventListener("submit", formListener);
    });

    selectAll([".share-buttons > button"]).forEach(function(el) {
      el.addEventListener("click", function(e) {
        shareListener(e, el);
      });
    });
  };

  function formListener(e) {
    if (FormData) {
      e.preventDefault();
      makePhoenixFormRequest("POST", e.target, function(err, res) {
        var response = JSON.parse(res);
        var resource = select("#resource_" + response.id);
        var visited_resource = select("#visited_" + response.id);

        if (visited_resource) {
          visited_resource.innerHTML = response.visited_result;
          visited_resource.addEventListener("submit", formListener);
        }

        if (resource) {
          resource.innerHTML = response.result;
          resource.addEventListener("submit", formListener);
        }

        if (response.feedback) {
          remove_visited(response.id)
        }

        feedbackLoopListener();

        addAnalytics(select("button[name='like']", resource), {event: "Like", variable: "liked", location: "resource"});
        addAnalytics(select("button[name='dislike']", resource), {event: "Dislike", variable: "disliked", location: "resource"});
        addAnalytics(select(".share", resource), {event: "Share", variable: "shared"});
        addAnalytics(select(".resource-feedback", resource), {event: "ResourceFeedback", variable: "reviewed", location: "resource"});
        addAnalytics(select(".loop-like", visited_resource), {event: "Like", variable: "liked", location: "feedback loop"});
        addAnalytics(select(".loop-dislike", visited_resource), {event: "Dislike", variable: "disliked", location: "feedback loop"});
        addAnalytics(select(".loop-feedback", visited_resource), {event: "ResourceFeedback", variable: "reviewed", location: "feedback loop"});
        handle_ios();
      });
    }
  };
}

function handle_ios_likes (like) {
  selectAll("button[name='" + like + "']").forEach(function (el) {
    if (el.className.indexOf(like + '_no_hover') === -1) {
      toggleClasses(el, [like, like + '_no_hover'])
    }
  });
}

function handle_ios () {
  if (navigator.platform && /iPad|iPhone|iPod/.test(navigator.platform)) {
    ['like', 'dislike'].forEach(handle_ios_likes);
  }
}

function shareListener(e, el) {
  var alert = select(".share-alert",  select("#resource_" + getResourceId(el)));
  alert.innerHTML = "Sorry, this feature is not yet available"

  setTimeout(function() {
    alert.innerHTML = "";
  }, 3000)
}

handle_ios();
likeListeners();
