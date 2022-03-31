// Author: Walter Schreppers
// We might put this in a class or prototype later on
// for now this is easy enough to use in our redactietool.

function getModalDialog(){
  return document.getElementById('modal_dlg');
}

function closeModalAlert(){
  getModalDialog().classList.remove('is-active')
}

function showModalAlert(title, content){
  var modal_dlg = getModalDialog();
  
  var modal_title = modal_dlg.getElementsByClassName('modal-card-title')[0];
  // modal_title.innerHTML = title; // allows raw html, use with caution
  modal_title.innerText = title;
  
  var modal_content = modal_dlg.getElementsByClassName('modal-card-body')[0];
  // modal_content.innerHTML = content; // allows raw html, use with caution
  modal_content.innerText = content;

  // show customized modal dialog
  modal_dlg.classList.add('is-active');
}

function getModalCloseBtn(){
  return getModalDialog().getElementsByClassName("delete")[0]
}

function getModalCancelBtn(){
  return getModalDialog().getElementsByClassName("button")[1]
}

function getModalSaveBtn(){
  return getModalDialog().getElementsByClassName("is-success")[0]
}

function modalCloseClicked(){
  console.log("modal close clicked");
  closeModalAlert();
}

function modalSaveClicked(){
  console.log("modal save button clicked");
  closeModalAlert();
}

function modalCancelClicked(){
  console.log("modal cancel button clicked");
  closeModalAlert();
}

// Demo usage:
//  var modal_btn = document.getElementById('modal_btn');
//  modal_btn.addEventListener('click', () => {
//    showModalAlert(
//      "Waarschuwing titel",
//      "Hier de boodschap die je wilt tonen"
//    ); 
//  });
//
//  // events to close the modal dialog
//  var modal_close_btn = getModalCloseBtn();
//  modal_close_btn.addEventListener('click', () => {
//    modalCloseClicked();
//  });
//
//  var modal_save_btn = getModalSaveBtn();
//  modal_save_btn.addEventListener('click', () => {
//    modalSaveClicked();
//  });
//
//
//  var modal_cancel_btn = getModalCancelBtn();
//  modal_cancel_btn.addEventListener('click', () => {
//    modalCancelClicked();
//  });
//
