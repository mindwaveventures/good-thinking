var personaliseDiv = document.getElementById('elm-personalise');

var issue_tags = Array.prototype.map.call(document.getElementsByName("issue"), (el) => el.value)
var content_tags = Array.prototype.map.call(document.getElementsByName("content"), (el) => el.value)
var reason_tags = Array.prototype.map.call(document.getElementsByName("reason"), (el) => el.value)

Elm.Main.embed(personaliseDiv, {
  issue_tags: issue_tags,
  content_tags: content_tags,
  reason_tags: reason_tags
});
