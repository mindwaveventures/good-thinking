function feedbackLoopListener() {
  selectAll('.resource-link').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var resource_id = get_resource_id(e.target);
      add_visited(resource_id);
      window.location.reload();
    });
  });

  selectAll('.remove_visited').forEach(function (el) {
    el.addEventListener('click', function(e) {
      var resource_id = get_resource_id(e.target);
      remove_visited(resource_id);
      delete_visited(resource_id);
    });
  });
}

function add_visited(resource_id) {
  if (get_feedback_left_resources().indexOf(resource_id) > -1) {
    // if feedback is already left, we don't want to
    // include this resource in the feedback loop
    return;
  }
  if (document.cookie.indexOf('ldmw_visited_resources') === -1) {
    document.cookie = 'ldmw_visited_resources=' + resource_id;
  } else {
    var visited_resources = get_visited_resources();
    if (visited_resources.indexOf(resource_id) === -1) {
      document.cookie = 'ldmw_visited_resources=' + visited_resources.join() + ',' + resource_id;
    }
  }
}

function add_to_feedback_left_resources(resource_id) {
  if (document.cookie.indexOf('ldmw_feedback_left_resources') === -1) {
    document.cookie = 'ldmw_feedback_left_resources=' + resource_id;
  } else {
    var feedback_left_resources = get_feedback_left_resources();
    if (feedback_left_resources.indexOf(resource_id) === -1) {
      document.cookie = 'ldmw_feedback_left_resources=' + feedback_left_resources.join() + ',' + resource_id;
    }
  }
}

function get_resource_id(node) {
  if(node.id.indexOf('resource_') > -1 || node.id.indexOf('visited_') > -1) {
    return node.id.split('_')[1];
  }

  if(!node.parentNode) {
    console.log('Could not find resource_id');
    return;
  }

  return get_resource_id(node.parentNode);
}

function get_feedback_left_resources () {
  var resources =  document.cookie.match(/ldmw_feedback_left_resources=([^;]+)(;|$)/)
  if (resources) {
    return resources[1].split(',');
  } else {
    return [];
  }
}

function get_visited_resources () {
  var resources =  document.cookie.match(/ldmw_visited_resources=([^;]+)(;|$)/)
  if (resources) {
    return resources[1].split(',');
  } else {
    return [];
  }
}

function remove_visited(id) {
  var visited_resources = get_visited_resources().filter(function (el) {
    return el && el !== id;
  });
  if (visited_resources.length > 0) {
    document.cookie = 'ldmw_visited_resources=' + visited_resources.join();
  } else {
    delete_cookie('ldmw_visited_resources');
  }
}

function delete_visited(id) {
  select('#visited_' + id).outerHTML = "";
  var visited_resources = get_visited_resources().filter(function (el) {
    return el !== id;
  });
  if (visited_resources.length === 0) {
    select('#visited_resources').outerHTML = "";
  }
  add_to_feedback_left_resources(id);
}

var delete_cookie = function(name) {
  document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};
