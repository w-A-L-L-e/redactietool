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


function addMaker(ev){
  var mkr_input = document.getElementById("prd_maker_input");
  var mkr_clone = mkr_input.cloneNode(true)
  var mkr_list = document.getElementById("prd_makers");
  mkr_list.append(mkr_clone)
  return false;
}

function addBijdrager(ev){
  var bdr_input = document.getElementById("prd_bijdrager_input");
  var bdr_clone = bdr_input.cloneNode(true)
  var bdr_list = document.getElementById("prd_bijdragers");
  bdr_list.append(bdr_clone)
  return false;
}

function addPublisher(ev){
  var bdr_input = document.getElementById("prd_publisher_input");
  var bdr_clone = bdr_input.cloneNode(true)
  var bdr_list = document.getElementById("prd_publishers");
  bdr_list.append(bdr_clone)
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


// vanilla script for burger toggle from bulma.io example
// alternate versions for jquery etc can also be found here:
// https://bulma.io/documentation/components/navbar/
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

