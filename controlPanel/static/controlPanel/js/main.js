'use strict'



//---------------------------------------
//           MAIN SCRIPT
//---------------------------------------

//1. Get the label of the form
var previous_form_label = document.getElementById("form-label").value;
console.log("form_label ", previous_form_label)
console.log(DJANGO_STATIC_URL);
//2. Get the form
const form_data = get_form(previous_form_label);
form_data.then(form => {
  var new_form = to_form_with_conditionnal_questions(form);


  var container = document.getElementById("form");
  for (var i = 0; i < new_form.length; i++) {
      container.appendChild(layout_question(new_form, i));
  }

  $(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
  });

});

function save(){
  upload_general_informations().then(() => {upload_form();});
}
