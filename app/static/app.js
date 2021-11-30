// Author: Walter Schreppers
// Animate buttons and handle top menu events.
function execute(btn, label){
  btn.form.submit(); 
  btn.disabled=true; 
  btn.value=label;
}

function loginSubmit(btn){
  execute(btn, "Authenticeren..."); 
}

// original version
// function pidSubmit(btn){
//   execute(btn, 'Zoeken...');
// }

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

// #logout_btn
function logoutClicked(ref){
  ref.className += ' disabled';
}

// #new_upload_btn
function newUploadClicked(ref){
  ref.className += ' disabled';
}

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

// generic add item for productie section
function addPrdItem(item_list_id, item_input_id){
  var item_input = document.getElementById(item_input_id);
  var item_clone = item_input.cloneNode(true);
  var item_list = document.getElementById(item_list_id);
  item_list.append(item_clone);
  return false;
}

// generic delete production section item
function deletePrdItem(del_btn){
  del_btn.parentNode.parentNode.remove();
  return false;
}

// TODO: deprecate these next 3 methods by by putting the call directly in view
function addMaker(ev){
  return addPrdItem('prd_makers', 'prd_maker_input');
}

function addBijdrager(ev){
  return addPrdItem('prd_bijdragers', 'prd_bijdrager_input');
}

function addPublisher(ev){
  return addPrdItem('prd_publishers', 'prd_publisher_input')
}

// end of to be deprecated methods

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

function collapseEmptyTextarea(area_id){
  var ta = document.getElementById(area_id);
  if( ta && ta.innerHTML.length == 0){
    ta.parentNode.parentNode.style.display="none";
    console.log("found empty area", area_id, "collapsing, TODO: change folded/unfolded icon...");
  }
}

// document on-ready handler
// handles burger menu and collapsing of empty items in Inhoud section
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

  // Inhoud section hide unused/empty textarea's for current item
  collapseEmptyTextarea("originele_hoofdbeschrijving");
  collapseEmptyTextarea("originele_uitgebreide_hoofdbeschrijving");
  collapseEmptyTextarea("ondertitels");
  collapseEmptyTextarea("programma_omschrijving");
  collapseEmptyTextarea("cast");
  collapseEmptyTextarea("transcriptie");

  
  // This below stuff might come in handy later...
  //// TODO: catch navigation event..
  // showNavigationWarning();

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
  
  //TODO: slim select for multi select component
  //new SlimSelect({
  //  select: '#multiple'
  //})
});

