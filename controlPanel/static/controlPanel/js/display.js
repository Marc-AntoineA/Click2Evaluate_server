'use strict'

// arrow-up, add, delete
function layout_toolbar_up(){
  var toolbar = document.createElement("DIV");
  toolbar.className = "toolbar toolbar-up";

  var move_up_button = document.createElement("BUTTON");
  var icon_arrow_up = document.createElement("IMG");
  icon_arrow_up.src = DJANGO_STATIC_URL + "icons/arrow-up.png";
  icon_arrow_up.className = "icon";
  icon_arrow_up.setAttribute("data-toggle", "tooltip");
  icon_arrow_up.setAttribute("title", "Déplacer cette question vers le haut");
  move_up_button.setAttribute("onclick", "event_move_question(this, true)");
  move_up_button.appendChild(icon_arrow_up);
  toolbar.appendChild(move_up_button);

  var add_button = document.createElement("BUTTON");
  var icon_add = document.createElement("IMG");
  icon_add.src = DJANGO_STATIC_URL + "icons/add.png";
  icon_add.className = "icon";
  add_button.setAttribute("onclick", "event_add_question(this, true, false)");
  add_button.appendChild(icon_add);
  toolbar.appendChild(add_button);

  var delete_button = document.createElement("BUTTON");
  var icon_delete = document.createElement("IMG");
  icon_delete.src = DJANGO_STATIC_URL + "icons/delete.png";
  icon_delete.className = "icon";
  delete_button.setAttribute("onclick", "event_delete_question(this)");
  delete_button.appendChild(icon_delete);
  toolbar.appendChild(delete_button);

  return toolbar;
}

function layout_toolbar_down(){
  var toolbar = document.createElement("DIV");
  toolbar.className = "toolbar toolbar-down";

  var move_up_button = document.createElement("BUTTON");
  var icon_arrow_up = document.createElement("IMG");
  icon_arrow_up.src = DJANGO_STATIC_URL + "icons/arrow-down.png";
  icon_arrow_up.className = "icon";
  move_up_button.appendChild(icon_arrow_up);
  move_up_button.setAttribute("onclick", "event_move_question(this, false)");
  toolbar.appendChild(move_up_button);

  var add_button = document.createElement("BUTTON");
  var icon_add = document.createElement("IMG");
  icon_add.src = DJANGO_STATIC_URL + "icons/add.png";
  icon_add.className = "icon";
  add_button.setAttribute("onclick", "event_add_question(this, false, false)");
  add_button.appendChild(icon_add);
  toolbar.appendChild(add_button);

  var delete_button = document.createElement("BUTTON");
  var icon_delete = document.createElement("IMG");
  icon_delete.src = DJANGO_STATIC_URL + "icons/delete.png";
  icon_delete.className = "icon";
  delete_button.setAttribute("onclick", "event_delete_question(this)");
  delete_button.appendChild(icon_delete);
  toolbar.appendChild(delete_button);

  return toolbar;
}

function layout_label_question(label_str, sub = false){
  var legend = document.createElement("LABEL");
  legend.className = "legend";
  legend.innerHTML = "Intitulé de la question"

  var label = document.createElement("INPUT");
  if(sub){
    label.className = "label sub-label"
  }else{
    label.className = "label";
  }
  label.value = label_str;

  var container = document.createElement("DIV");
  container.appendChild(legend);
  container.appendChild(label);

  return container;
}

function layout_middle_toolbar(obligatory_bool, type_question, isSub){
    var toolbar = document.createElement("DIV");
    toolbar.className = "toolbar";

    var legend = document.createElement("LABEL");
    legend.className = "legend";
    legend.innerHTML = "Type de la question";

    var select = document.createElement("SELECT");
    select.name = "type_question";
    if(isSub){
      select.setAttribute("oninput", "event_type_question(this, 5)");
    }else{
      select.setAttribute("oninput", "event_type_question(this, 3)");
    }

    select.size = "1";
    //-- Values
      var option1 = document.createElement("OPTION");
      option1.value = "selectOne";
      option1.innerHTML = "Question à choix unique";
      if(type_question == "selectOne"){
        option1.selected = "selected";
      }
      select.appendChild(option1);

      var option2 = document.createElement("OPTION");
      option2.value = "select";
      if(type_question == "select"){
        option2.selected = "selected";
      }
      option2.innerHTML = "Question à choix multiples";
      select.appendChild(option2);

      var option3 = document.createElement("OPTION");
      option3.value = "number";
      if(type_question == "number"){
        option3.selected = "selected";
      }
      option3.innerHTML = "Nombre";
      select.appendChild(option3);

      var option4 = document.createElement("OPTION");
      option4.value = "text";
      if(type_question == "text"){
        option4.selected = "selected";
      }
      option4.innerHTML = "Texte libre";
      select.appendChild(option4);

      var option5 = document.createElement("OPTION");
      option5.value = "inline";
      if(type_question == "inline"){
        option5.selected = "selected";
      }
      option5.innerHTML = "Texte court";
      select.appendChild(option5);

    var obligatory_label = document.createElement("LABEL");
    obligatory_label.className = "legend margin-left";
    obligatory_label.innerHTML = "Question obligatoire ? ";

    var checkbox = document.createElement("INPUT");
    checkbox.id = "obligatory";
    checkbox.className = "obligatory";
    checkbox.type = "checkbox";
    checkbox.setAttribute("onclick", "event_obligatory(this)");

    if(obligatory_bool){
      checkbox.checked = "checked";
    }

    toolbar.appendChild(legend);
    toolbar.appendChild(select);
    toolbar.appendChild(obligatory_label);
    toolbar.appendChild(checkbox);

    return toolbar;
}

function layout_question(questions, id){
  const question = questions[id];

  var question_box = document.createElement("DIV");
  question_box.className = "question-box";
  if(question.obligatory){
    question_box.classList.add("question-box-obligatory");
  }
  question_box.id = id;

  const toolbar_up_box = layout_toolbar_up();
  const label_box = layout_label_question(question.label);
  const toolbar_middle_box = layout_middle_toolbar(
    question.obligatory, question.type_question, question.isSub);
  const toolbar_down_box = layout_toolbar_down();
  question_box.appendChild(toolbar_up_box);
  question_box.appendChild(label_box);
  question_box.appendChild(toolbar_middle_box);
  var type_data_box = layout_type_data(question.type_question, question.type_data, question.subs);
  type_data_box.id = "type-data";
  question_box.appendChild(type_data_box);

  question_box.appendChild(toolbar_down_box);
  return question_box;
}

function layout_type_data(type_question, type_data, subs){
  if(type_question == "number"){

    if(type_data == ""){
      return layout_number(0, 100);
    }else{
      const type_data_s = type_data.split(";");
      return layout_number(type_data_s[0], type_data_s[1]);
    }
  }

  if (type_question == "select" ||
        type_question == "selectOne"){
    var form_type_data_box;
    if(type_data == ""){
      form_type_data_box = layout_choices([], []);

    }else{
      const choices = type_data.split(";");
      form_type_data_box = layout_choices(choices, subs);
    }
    const type_data_box = document.createElement("DIV");
    const add_button_choice = layout_add_button_choice();
    type_data_box.appendChild(add_button_choice);
    type_data_box.appendChild(form_type_data_box);
    return type_data_box;
  }

  const type_data_box = document.createElement("DIV");
  type_data_box.className = "type-data";
  return type_data_box;
}

function layout_number(minimum, maximum){
  var container = document.createElement("DIV");
  container.className = "type-data";

  var label_inf = document.createElement("LABEL");
  label_inf.className = "legend";
  label_inf.innerHTML = "Minimum :";

  var input_inf = document.createElement("INPUT");
  input_inf.id = "min";
  input_inf.type = "number";
  input_inf.value = minimum;

  var label_sup = document.createElement("LABEL");
  label_sup.className = "legend";
  label_sup.innerHTML = "Maximum : ";

  var input_sup = document.createElement("INPUT");
  input_sup.id = "max";
  input_sup.type = "number";
  input_sup.value = maximum;

  container.appendChild(label_inf);
  container.appendChild(input_inf);
  container.appendChild(label_sup);
  container.appendChild(input_sup);

  return container;
}

function layout_choices(choices, subs){
  var container = document.createElement("DIV");
  container.className = "type-data";
  for(var i = 0; i < choices.length; i++){
    const choice_box = layout_choice(choices, subs, i, true);
    container.appendChild(choice_box);
  }

  return container;
}

function layout_choice_sub(choices){
  var container = document.createElement("DIV");
  container.className = "type-data";

  var list = document.createElement("UL");
  for(var i = 0; i < choices.length; i++){
    var item = document.createElement("LI");
    item.innerHTML = choices[i];
    list.appendChild(item);
  }

  container.appendChild(list);
  return container;
}

function layout_toolbar_choice(conditional_bool){
  var toolbar = document.createElement("DIV");
  toolbar.className = "toolbar";

  var move_up_button = document.createElement("BUTTON");
  var icon_arrow_up = document.createElement("IMG");
  icon_arrow_up.src = DJANGO_STATIC_URL + "/icons/arrow-up.png";
  icon_arrow_up.className = "icon";
  move_up_button.appendChild(icon_arrow_up);
  move_up_button.setAttribute("onclick", "event_move_question(this, true)");
  toolbar.appendChild(move_up_button);

  var move_down_button = document.createElement("BUTTON");
  var icon_arrow_down = document.createElement("IMG");
  icon_arrow_down.src = DJANGO_STATIC_URL + "icons/arrow-down.png";
  icon_arrow_down.className = "icon";
  move_down_button.setAttribute("onclick", "event_move_question(this, false)");
  move_down_button.appendChild(icon_arrow_down);
  toolbar.appendChild(move_down_button);

  var add_button = document.createElement("BUTTON");
  var icon_add = document.createElement("IMG");
  icon_add.src = DJANGO_STATIC_URL + "icons/add.png";
  icon_add.className = "icon";
  add_button.setAttribute("onclick", "event_add_question(this, false, true)");
  add_button.appendChild(icon_add);
  toolbar.appendChild(add_button);

  var delete_button = document.createElement("BUTTON");
  var icon_delete = document.createElement("IMG");
  icon_delete.src = DJANGO_STATIC_URL + "icons/delete.png";
  icon_delete.className = "icon";
  delete_button.setAttribute("onclick", "event_delete_question(this)");
  delete_button.appendChild(icon_delete);
  toolbar.appendChild(delete_button);

  return toolbar;
}

function layout_choice_label(label){
    var container = document.createElement("DIV");

    var label_answer = document.createElement("LABEL");
    label_answer.className = "legend";
    label_answer.innerHTML = "Réponse possible : "
    container.appendChild(label_answer);

    var input_answer = document.createElement("INPUT");
    input_answer.type = "text";
    input_answer.className = "label sub-label";
    input_answer.value = label;
    container.appendChild(input_answer);

    return container;
}

function layout_choice(choices, subs, i, cond_enable){
    const choice = choices[i];
    var container = document.createElement("DIV");
    container.className = "question-box choice";

    const toolbar_up_box = layout_toolbar_choice();
    const choice_label_box = layout_choice_label(choice);
    container.appendChild(toolbar_up_box);
    container.appendChild(choice_label_box);


    var j = 0;
    while(j < subs.length && subs[j].parentsQuestionsValue != i){
      j++;
    }
    if(j < subs.length){
      const conditional_block = layout_conditional_question(true);
      const conditional_question = subs[j];
      const question_label_box = layout_label_question(conditional_question.label, true);
      const type_question_box = layout_middle_toolbar(conditional_question.obligatory,
        conditional_question.type_question, conditional_question.isSub);
      const type_data_box = layout_type_data(conditional_question.type_question, "", []);
      if (conditional_question.obligatory){
        container.classList.add("question-box-obligatory");
      }
      if(cond_enable){
        container.appendChild(conditional_block);
      }
      container.appendChild(question_label_box);
      container.appendChild(type_question_box);
      container.appendChild(type_data_box);
    }else{
      const conditional_block = layout_conditional_question(false);
      if(cond_enable){
      container.appendChild(conditional_block);
      }
    }
    return container;
}

function layout_conditional_question(conditional_bool){
  var container = document.createElement("DIV");

  var conditional_label = document.createElement("LABEL");
  conditional_label.className = "legend";
  conditional_label.innerHTML = "Question conditionnelle ? ";
  container.appendChild(conditional_label);

  var checkbox = document.createElement("INPUT");
  checkbox.id = "conditional";
  checkbox.className = "conditional";
  checkbox.type = "checkbox";
  if(conditional_bool){
    checkbox.checked = "checked";
  }
  checkbox.setAttribute("onclick", "event_conditional(this)");
  container.appendChild(checkbox);

  return container;
}

function layout_add_button_choice(){
  var container = document.createElement("DIV");
  container.className = "toolbar";

  var add_button = document.createElement("BUTTON");
  var icon_add = document.createElement("IMG");
  icon_add.src = DJANGO_STATIC_URL + "icons/add.png";
  icon_add.className = "icon";
  add_button.setAttribute("onclick", "event_add_choice(this)");
  add_button.appendChild(icon_add);
  container.appendChild(add_button);

  return container;
}
