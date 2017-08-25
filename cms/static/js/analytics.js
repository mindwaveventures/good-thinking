function analyticsListeners() {
  selectAll(".share").forEach(function(el) {
    addAnalytics(el, {event: "Share", variable: "shared"});
  });

  selectAll([".resource-like", ".resource-dislike"]).forEach(function(el) {
    if (el.classList.contains("like")) {
      addAnalytics(el, {event: "Like", variable: "liked", location: "resource"});
    } else {
      addAnalytics(el, {event: "Dislike", variable: "disliked", location: "resource"});
    }
  });

  selectAll([".loop-like", ".loop-dislike"]).forEach(function(el) {
    if (el.classList.contains("like")) {
      addAnalytics(el, {event: "Like", variable: "liked", location: "feedback loop"});
    } else {
      addAnalytics(el, {event: "Dislike", variable: "disliked", location: "feedback loop"});
    }
  });

  selectAll(".resource-feedback").forEach(function(el) {
    addAnalytics(el, {event: "ResourceFeedback", variable: "reviewed", action: "submit", location: "resource"});
  });

  selectAll(".loop-feedback").forEach(function(el) {
    addAnalytics(el, {event: "ResourceFeedback", variable: "reviewed", action: "submit", location: "feedback loop"});
  });
}

// Adds event listener that pushes to the data layer on click
// Expects target to have a data attribute containing the url
// of the resource it's linked to
/* Options : {
  event - Google Tag Manager event you want to trigger * required *,
  variable - Name of the variable to define on Google Tag Manager * required *,
  action - DOM event you want to track * defaults to click *,
  location - Location of event (feedback loop, resource etc.) * optional *
}
*/
function addAnalytics(el, opts) {
  if (el) {
    el.addEventListener(opts.action || "click", function(e) {
      var variableData = {};

      variableData[opts.variable] = e.target.getAttribute("data-url");

      if (opts.location) {
        variableData['location'] = opts.location;
      }

      dataLayer.push(variableData);
      dataLayer.push({"event": opts.event});
    });
  }
}

analyticsListeners();
