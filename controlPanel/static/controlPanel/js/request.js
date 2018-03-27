'use strict'

// functions to download and upload a typeform
function get_form(form_label){
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', server + form_label + "/");
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('Authorization', 'Token ' + token);
    xhr.onload = () => {
      if(xhr.status === 200)
      {
        resolve(JSON.parse(xhr.responseText));
      }
      else
      {
        reject(Error(xhr.responseText));
      }
    };
    xhr.onerror = () => reject(Error(xhr.responseText));
    xhr.send();
  });
}

function upload_general_informations(){
  const new_form_label = document.getElementById("form-label").value;
  const new_summary = document.getElementById("summary").value;
  const data = JSON.stringify({"name": new_form_label, "description" : new_summary});
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', server +  "modify/" + previous_form_label + "/");
    xhr.setRequestHeader('Authorization', 'Token ' + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
      if(xhr.status === 200){
        previous_form_label = new_form_label;
        resolve();
      }else{
        alert(Error(xhr.responseText));
        reject(Error(xhr.responseText));
      }
    };
    xhr.onerror = () => reject(Error(xhr.responseText));
    xhr.send(data);
  })
}

function upload_form(){
  const data = to_json_main();
  console.log(data);
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', server + previous_form_label + "/");
    xhr.setRequestHeader('Authorization', 'Token ' + token);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
      if(xhr.status === 200){
        resolve();
      }else{
        reject(Error(xhr.responseText));
      }
    };
    xhr.onerror = () => reject(Error(xhr.responseText));
    xhr.send(data);
  })
}


function to_form_with_conditionnal_questions(form){
  var new_form = new Array();

  // First, we keep only non-sub questions
  for(var i = 0; i < form.length; i++){
    const question = form[i];
    if(!question.isSub){
      question.subs = new Array()
      new_form.push(question);
    }
  }

  // Then, we add each subquestion to his parent question (tree view)
  for(var i = 0; i < form.length; i++){
    const question = form[i];
    if(question.isSub){
      const parentsPosition = question.parentsQuestionPosition;
      for(var j = 0; j < new_form.length; j++){
        const parentsQuestion = new_form[j];
        if(parentsQuestion.position == parentsPosition){
          parentsQuestion.subs.push(question);
        }
      }
    }
  }

  return new_form;
}
