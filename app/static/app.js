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

function pidSubmit(btn){
  execute(btn, 'Zoeken...');
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
   
  //// close it automagically like this
  //setTimeout(function(){
  //  closeModalAlert();
  //}, 3000);


  //TODO: slim select for multi select component
  //new SlimSelect({
  //  select: '#multiple'
  //})
});

