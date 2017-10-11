selectAll('.e24answers').forEach(function(e24) {
  e24.addEventListener('click', function(e) {
    selectAll('.e24answers').forEach(function(f) {
      if (f.name === e.target.name && f.type !== e.target.type) { // If the input element is from the same question but of a different type
        if (f.type === "radio" || f.type === "checkbox") f.checked = false; // clear checked
        if (f.type === "text") f.value = ""; // empty text
      }
    });
  });
})
