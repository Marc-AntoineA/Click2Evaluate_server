'use strict'

function to_json_main(){
  const form = document.getElementById("form");
  const form_label = document.getElementById("form-label").value;
  var position = 0;

  const dom_questions = form.children;

  var questions = []
  var position = 0;
  for (var i = 0; i < dom_questions.length; i++){
    const dom_q = dom_questions[i];

    var q = {};
    // Position
    q.position = position;

    // Label
    const label_box = dom_q.children[1];
    q.label = label_box.children[1].value;

    // obligatory and type_question
    const toolbar_box = label_box.nextElementSibling;
    q.type_question = toolbar_box.children[1].value;
    q.obligatory = toolbar_box.children[3].checked;

    // type_data
    if(q.type_question == "text" || q.type_question == "inline"){
      q.type_data = "";
    }

    if(q.type_question == "number"){
      const type_data_box = toolbar_box.nextElementSibling;
      const minimum = type_data_box.children[1].value;
      const maximum = type_data_box.children[3].value;
      q.type_data = minimum + ";" + maximum;
    }

    if(q.type_question == "select" || q.type_question == "selectOne"){
      const type_data_box = toolbar_box.nextElementSibling.children[1];
      const dom_choices = type_data_box.children;
      var choices = [];

      for(var j = 0; j < dom_choices.length; j++){
        const dom_c = dom_choices[j];
        const answer_box = dom_c.children[1];
        choices.push(answer_box.children[1].value);

        const conditional_box = answer_box.nextElementSibling;
        const isSub = conditional_box.children[1].checked;

        if(isSub){
          var qq = {};

          const label_box = conditional_box.nextElementSibling;
          qq.label = label_box.children[1].value;
          qq.position = position + j + 1;
          qq.parentsQuestionPosition = position;
          qq.parentsQuestionsValue = j;
          qq.isSub = true;

          const type_question_box_sub = label_box.nextElementSibling;
          qq.type_question = type_question_box_sub.children[1].value;
          qq.obligatory = type_question_box_sub.children[3].checked;

          if(qq.type_question == "number"){
            const type_data_box_sub = type_question_box_sub.nextElementSibling;
            const minimum = type_data_box_sub.children[1].value;
            const maximum = type_data_box_sub.children[3].value;
            qq.type_data = minimum + ";" + maximum;
          }

          if(qq.type_question == "text" || qq.type_question == "inline"){
            qq.type_data = "";
          }

          if(qq.type_question == "select" || qq.type_question == "selectOne"){
            const type_data_box_sub = type_question_box_sub.nextElementSibling.children[1];
            const dom_sub_choices = type_data_box_sub.children;
            var choices_sub = [];
            for(var k = 0; k < dom_sub_choices; k++){
              const label_answer_sub_sub = dom_sub_choices[k].children[1];
              choices_sub.push(label_answer_sub_sub.children[1].value);
            }
            qq.type_data = choices_sub.join(";");
          }
          qq.typeForm = form_label;
          questions.push(qq);
        }
      }
      q.type_data = choices.join(';');
      position = position + dom_choices.length;
    }

    q.isSub = false;
    q.parentsQuestionsValue = 0;
    q.parentsQuestionPosition = 0;

    //console.log(q);
    q.typeForm = form_label;
    questions.push(q);

    position = position + 1;
  }
  return JSON.stringify(questions);
}
