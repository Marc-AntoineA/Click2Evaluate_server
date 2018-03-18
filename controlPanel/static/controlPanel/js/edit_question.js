

function event_obligatory(checkbox){
  // Change the color of the question-box accordingly with the checkbox

  const question_box = checkbox.parentNode.parentNode;
  if(checkbox.checked){
    question_box.classList.add('question-box-obligatory');
  }else{
    question_box.classList.remove('question-box-obligatory');
  }
}

function event_conditional(checkbox){
  // Add or remove the box for a conditional question (label, type_data...)
  const question_box = checkbox.parentNode.parentNode;
  console.log(question_box);
  // true for sub
  if(checkbox.checked){
    const question_label_box = layout_label_question("Votre question", true);
    const type_question_box = layout_middle_toolbar(false,
      "number", true);
    const type_data_box = layout_type_data("number", "", []);
    question_box.appendChild(question_label_box);
    question_box.appendChild(type_question_box);
    question_box.appendChild(type_data_box);
  }else{
    question_box.removeChild(question_box.childNodes[5]);
    question_box.removeChild(question_box.childNodes[4]);
    question_box.removeChild(question_box.childNodes[3]);
    // if the question was obligatory
    question_box.classList.remove('question-box-obligatory');
  }

}

function event_type_question(select_node, position){
  // Change the type of the question. Position is used for conditional questions

  const question_box = select_node.parentNode.parentNode;
  var type_data_box = question_box.children[position];
  const new_type_data_box = layout_type_data(select_node.value, "", []);
  question_box.replaceChild(new_type_data_box, question_box.children[position]);
}

function event_move_question(button, up){
  // Up == True if up, else down

  const question_box = button.parentNode.parentNode;
  const form = question_box.parentNode;
  if (up){
    const previous = question_box.previousElementSibling;
    if(previous){
      form.insertBefore(question_box, previous);
    }
  }else{
    const next = question_box.nextElementSibling;
    if(next){
      form.insertBefore(next, question_box);
    }
  }
}

function event_delete_question(button){
  // Remove a question_box

  const question_box = button.parentNode.parentNode;
  const form = question_box.parentNode;
  form.removeChild(question_box);
}

function event_add_question(button, above, sub){
  // Add a question above if above, else bellow
  const question_box = button.parentNode.parentNode;

  const form = question_box.parentNode;

  var new_question_box;
  if(!sub){
    const blank_questions = [{
      id: 1,
      isSub: false,
      label: "Votre question",
      obligatory: false,
      parentsQuestionsValue: 0,
      parentsQuestionPosition: 0,
      position: "0",
      subs: [],
      type_data: "",
      type_question: "selectOne"
    }];
    new_question_box = layout_question(blank_questions, 0);
  }else{
    console.log(question_box.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode);
    new_question_box = layout_choice(["Votre réponse"],
      [],
      0,
      !question_box.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.classList.contains("question-box"));
  }

  if (above){
    form.insertBefore(new_question_box, question_box);
  }else{
    form.insertBefore(new_question_box, question_box);
    form.insertBefore(new_question_box, question_box);
  }
}

function event_add_choice(button) {
  // Add a blank choice for select and selectOne

  const form = button.parentNode.nextElementSibling;
  const question_box = form.parentNode.parentNode;

  console.log(question_box.parentNode.parentNode.parentNode);
  const new_question_box = layout_choice(["Votre réponse"],
    [],
    0,
    !question_box.parentNode.parentNode.parentNode.classList.contains("question-box"));
  form.appendChild(new_question_box);

}

function event_add_question_end(button) {
  // Add a blank question

  const form = document.getElementById("form");
  const blank_questions = [{
    id: 1,
    isSub: false,
    label: "Votre question",
    obligatory: false,
    parentsQuestionsValue: 0,
    parentsQuestionPosition: 0,
    position: "0",
    subs: [],
    type_data: "",
    type_question: "selectOne"
  }];
  const new_question_box = layout_question(blank_questions, 0);
  form.appendChild(new_question_box);
}
