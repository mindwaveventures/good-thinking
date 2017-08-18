function feedbackLoopListener() {
  selectAll('.resource-link').forEach(function (el) {
    el.addEventListener('click', function (e) {
      var resource_id = get_resource_id(e.target);
      if (document.cookie.indexOf('ldmw_visited_resources') === -1) {
        document.cookie = 'ldmw_visited_resources=' + resource_id;
      } else {
        var visited_resources = get_visited_resources();
        if (visited_resources.indexOf(resource_id) === -1) {
          document.cookie = 'ldmw_visited_resources=' + visited_resources.join() + ',' + resource_id;
        }
      }
    });
  });

  selectAll('.remove_visited').forEach(function (el) {
    el.addEventListener('click', function(e) {
      var id = get_resource_id(e.target);
      remove_visited(id);
      delete_visited(id);
    });
  });
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

function get_visited_resources () {
  var resources =  document.cookie.match(/ldmw_visited_resources=([^;]+);/)
  if (resources) {
    return resources[1].split(',');
  } else {
    return [];
  }
}

function remove_visited(id) {
  visited_resources = get_visited_resources().filter(function (el) {
    return el !== id;
  });
  if (visited_resources.length > 0) {
    document.cookie = 'ldmw_visited_resources=' + visited_resources.join();
  } else {
    delete_cookie('ldmw_visited_resources');
  }
}

function delete_visited(id) {
  select('#visited_' + id).outerHTML = "";
  visited_resources = get_visited_resources().filter(function (el) {
    return el !== id;
  });
  if (visited_resources.length === 0) {
    select('#visited_resources').outerHTML = "";
  }
}

var delete_cookie = function(name) {
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
};
