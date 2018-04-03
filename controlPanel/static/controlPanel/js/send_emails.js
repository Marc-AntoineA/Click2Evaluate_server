// Function to send emails with client webmail

// To make breaklines in a mail, use : %0D%0A
// src. http://www.cubetoon.com/2008/how-to-enter-line-break-into-mailto-body-command/

const subject_general = "[Éval'Ponts][Relance] Il vous reste des cours à évaluer !";
const body_general = "Bonjour, %0D%0AIl semblerait que vous n'ayez pas encore évalué\
 tous vos cours du semestre : les premières commissions d'évaluation se réunissent\
 bientôt et vos camarades doivent disposer de vos réponses pour faire leur synthèse,\
 dans l'objectif d'améliorer les cours dispensés à l'École des Ponts.%0D%0A\
 Nous vous remercions de prendre quelques minutes pour les évaluer, en vous rendant sur\
 click2evaluate.ma-augé.fr ou en téléchargeant l'application sur []%0D%0A\
 Cordialement,%0D%0A\
 L'équipe du S2iP";

function subject_course(name, date){
  const today = new Date();
  const day_left = Math.floor((date - today)/(3600*1000*24));
  return "[Éval'Ponts][Relance]"
    + "[" + name + "]"
    + "[J - " + day_left + "]"
    + " Évaluez votre cours sur Éval'Ponts !";
}

function body_course(name, date){
  return "Bonjour,%0D%0AIl semblerait que vous n'ayez pas encore évalué le cours : "
  + name
  + "%0D%0AN'oubliez pas de le faire avant le "
  + date.toLocaleDateString()
  + " . Cela permettra à vos camarades de disposer de vos réponses pour faire leur, \
  synthèse, dans l'objectif d'améliorer les cours dispensés à l'École des Ponts.%0D%0A\
Nous vous remercions de prendre quelques minutes pour les évaluer, en vous rendant sur\
click2evaluate.ma-augé.fr ou en téléchargeant l'application sur ....%0D%0A"
  + "%0D%0ACordialement,%0D%0A L'équipe du S2iP";
}

// Retur a link mailto to open emails. If name or date is not provided, send
// a general email (subject_general and body_general) else send a particular link
// with subject_course and body_course.
// The students emails are bcc (blind copy). They can't see each other
function send_email(emails, name, date){
  if(typeof(name) === 'undefined' || typeof(date) === 'undefined'){
    const link = "mailto:"
            +"?bcc=" + emails
            +"&subject=" + subject_general
            +"&body=" + body_general;
    window.location.href = link;
  }else{
    // date is a string
    const real_date = new Date(date);
    const link = "mailto:"
            +"?bcc=" + emails
            +"&subject=" + subject_course(name, real_date)
            +"&body=" + body_course(name, real_date);
    window.location.href = link;
  }
}
