// ============================== App JavaScript ===============================
// Author: Walter Schreppers
//
//  File: app/static/app.js
//
// Animate submit buttons and handle fixed bulma menu events.
//
// Handle collapsing of sections and adding/removing items
// in productie section metadata form. 
//
// future work: we might split this up in seperate js files and
// have some minification done in our precompile assets makefile target.


// ============================== SUBTITLE FORMS ===============================
function execute(btn, label){
  btn.form.submit(); 
  btn.disabled=true; 
  btn.value=label;
}

function loginSubmit(btn){
  execute(btn, "Authenticeren..."); 
  btn.form.submit();
  btn.disabled=true;
  btn.classList.add('is-loading')
}

function pidSubmitForSubtitles(btn){
  hf = document.getElementById('redirect_subtitles');
  hf.value = 'yes';
  execute(btn, 'Item opzoeken...');
}

function pidSubmitForMetadata(btn){
  hf = document.getElementById('redirect_subtitles');
  hf.value = 'no';
  execute(btn, 'Item opzoeken...');
}

function uploadSubmit(btn){
  execute(btn, 'Opladen...');

  // also disable anuleren link
  cancel_btn = document.getElementById('upload_cancel');
  if( cancel_btn ){ 
    cancel_btn.className += ' disabled';
    cancel_btn.href = "#disabled";
  }
}

function uploadCancel(ref){
  console.log("uploadCancel clicked!")
  ref.className += ' disabled';
}

function previewSubmit(btn){
  execute(btn, 'Versturen...')

  //disable wissen button
  cancel_btn = document.getElementById('preview_cancel');
  if( cancel_btn ){ 
    cancel_btn.className += ' disabled';
    cancel_btn.href = "#disabled";
  }
}

function previewCancel(ref){
  ref.className += ' disabled';
}

function confirmSubmit(btn){
  execute(btn, 'Versturen...');

  cancel_btn = document.getElementById('confirm_cancel')
  if(cancel_btn){
    cancel_btn.disabled=true;
  }
}

function confirmCancel(btn){
  execute(btn, 'Wissen...');

  repl_btn = document.getElementById('confirm_submit')
  if(repl_btn){
    repl_btn.disabled=true;
  }
}


// ============================ LOGIN/LOGOUT FORMS =============================
function logoutClicked(ref){
  // #logout_btn
  ref.className += ' disabled';
}

function newUploadClicked(ref){
  // #new_upload_btn
  ref.className += ' disabled';
}


// ============================= MODAL DIALOG ==================================
function showNavigationWarning(){
  //v1
  //showModalAlert(
  //    "Waarschuwing",
  //    "Opgelet: je bewerkingen zijn niet opgeslagen. Ben je zeker dat je deze pagina wil verlaten?"
  //);

  //v2.1
  showModalAlert(
      "Ben je zeker dat je deze pagina wilt verlaten?",
      "Opgelet: je bewerkingen worden niet bewaard wanneer je deze pagina verlaat."
  );

}

function flashModalWarning(){
  showModalAlert(
      "Sync is misgelopen",
      "Deze alert gaat na 3 seconden automatisch dicht..."
  );

  setTimeout(function(){
    closeModalAlert();
  }, 3000);
}


// =========================== METADATA EDIT FORM =============================
// add item method for 'productie' section
function addPrdItem(item_list_id, item_input_id){
  var item_input = document.getElementById(item_input_id);
  var item_clone = item_input.cloneNode(true);
  var item_list = document.getElementById(item_list_id);
  item_list.append(item_clone);
  return false;
}

// delete item method for 'productie' section item
function deletePrdItem(del_btn){
  del_btn.parentNode.parentNode.remove();
  return false;
}

function sectionToggle(section_div_id){
  var form_section = document.getElementById(section_div_id);

  var close_icon_wrapper = document.getElementById(section_div_id + "_icon");
  var folded_icon = close_icon_wrapper.getElementsByClassName("icon-folded")[0];
  var unfolded_icon = close_icon_wrapper.getElementsByClassName("icon-unfolded")[0];

  if(form_section.style.display == 'none'){
    // form_section.style.display="flex"
    form_section.style.display="block";
    unfolded_icon.style.display="block";
    folded_icon.style.display="none";
  }
  else{
    form_section.style.display="none";
    unfolded_icon.style.display="none";
    folded_icon.style.display="block";
  }
}

function collapseEmptyTextarea(area_id, uncollapsable=false){
  var ta = document.getElementById(area_id);
  if( ta && ta.innerHTML.length == 0){
    if(uncollapsable){
      ta.parentNode.parentNode.style.display="none";
      console.log("found empty area", area_id, "TODO: change folded/unfolded icon...");
    }
    else{
      ta.parentNode.parentNode.parentNode.style.display="none";
    }
  }
}

// Inhoud section hide unused/empty textarea's for current item
function collapseEmptyTextareas(){
  // when passing 'true' we show a collapse/uncollapse icon and 
  // keep the heading in our section around the textarea when its collapsed
  // collapseEmptyTextarea("originele_hoofdbeschrijving", true);
  collapseEmptyTextarea("originele_hoofdbeschrijving");
  collapseEmptyTextarea("originele_uitgebreide_hoofdbeschrijving");
  collapseEmptyTextarea("ondertitels");
  collapseEmptyTextarea("programma_beschrijving");
  collapseEmptyTextarea("cast");
  collapseEmptyTextarea("transcriptie");
}


function hideTitleInput(input_id){
  var input_field = document.getElementById(input_id);
  if( input_field ){
    var input_box = input_field.getElementsByTagName("input")[0];
    if( input_box && input_box.value.length == 0){
      //console.log("hiding field", input_id);
      input_field.style.display = "none";
    }
  }
}

function hideEmptyTitles(){
  hideTitleInput("titel_serie");
  hideTitleInput("titel_episode")
  hideTitleInput("titel_aflevering");
  hideTitleInput("titel_alternatief");
  hideTitleInput("titel_programma");
  hideTitleInput("titel_serienummer");
  hideTitleInput("titel_seizoen");
  hideTitleInput("titel_nummer");
  hideTitleInput("titel_archief");
  hideTitleInput("titel_deelarchief");
  hideTitleInput("titel_reeks");
  hideTitleInput("titel_deelreeks");
  hideTitleInput("titel_registratie");
}

function showTitleInput(input_id){
  var input_field = document.getElementById(input_id);
  if( input_field ){
    input_field.style.display = "flex";
  }
}

function showEmptyTitles(){
  showTitleInput("titel_serie");
  showTitleInput("titel_episode")
  showTitleInput("titel_aflevering");
  showTitleInput("titel_alternatief");
  showTitleInput("titel_programma");
  showTitleInput("titel_serienummer");
  showTitleInput("titel_seizoen");
  showTitleInput("titel_nummer");
  showTitleInput("titel_archief");
  showTitleInput("titel_deelarchief");
  showTitleInput("titel_reeks");
  showTitleInput("titel_deelreeks");
  showTitleInput("titel_registratie");
}

function closeSavedAlert(){
  var alert_box = document.getElementById("data_saved_alert_box");
  if(alert_box){
    alert_box.style.display = "none";
  }
}

function autoCloseSavedAlert(){
  setTimeout(function(){
    closeSavedAlert();
  }, 4000); 
}

function addUnloadHooks(){
  // some vanilla onbeforeunload for our custom alert box, this needs some further work and state:
  // when we add this listener we get the browser default popups.
  // window.addEventListener('beforeunload', function (e) {
  //   console.log("EVENT: beforeunload detected!");
  //   // Cancel the event
  //   e.preventDefault(); // If you prevent default behavior in Mozilla Firefox prompt will always be shown
  //   // Chrome requires returnValue to be set
  //   e.returnValue = '';

  //         //possibly do something like this, not sure yet:
  //         // setInterval(function(){
  //         //    if modalCancelled return false;
  //         //    if modalConfirmed return true;
  //         // }, 800);

  //   // the absence of a returnValue property on the event will guarantee the browser unload happens
  //   delete e['returnValue'];
  // });
  //
  // Found an interesting jquery/bootstrap based module that matches more what is described
  // in ticket DEV-1794:
  // https://github.com/NightOwl888/jquery.dirtyforms.dialogs.bootstrap.dist. 
  // -> I need to test this out first and refactor or rewrite some of the modal_dialog.js code to 
  // do something similar for bulma instead.
  // That will however also introduce jquery into the mix, making our js dependencies around 86k larger.
}


// ====================================== DOCUMENT READY EVENT ========================================
// document on-ready handler
// handles burger menu and collapsing of
// empty items in Inhoud section
document.addEventListener('DOMContentLoaded', () => {
  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

  // Check if there are any navbar burgers
  if ($navbarBurgers.length > 0) {

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {

        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');

      });
    });
  }

  collapseEmptyTextareas();
  hideEmptyTitles();
  autoCloseSavedAlert();
  
  // showNavigationWarning();
  // flashModalWarning();
  // showModalAlert("hello", "world");

  // beforeunload confirm/cancel example
  // addUnloadHooks();

  // TODO: slim select for multi select component
  // new SlimSelect({
  //   select: '#multiple'
  // })
});

