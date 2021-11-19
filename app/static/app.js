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

function openModalDialog(btn_id, dialog_id){
  // button to open the modal dialog
  var modal_btn = document.getElementById(btn_id);
  var modal_dlg = document.getElementById(dialog_id);

  if(!modal_btn){
    console.log('modal dialog not present on page...');
    return;
  }

  //add onclick event listener
  modal_btn.addEventListener('click', () => {
    modal_dlg.classList.add('is-active');
    // and use classList.remove for the other buttons to close again... 
  });
}

// vanilla js for burger toggle
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

  openModalDialog('modal_btn', 'modal_dlg');

  //TODO: slim select for multi select component
  //new SlimSelect({
  //  select: '#multiple'
  //})
});

// jquery or react versions can be done too, but this will increase the resulting js libraries to be loaded...:
// $(document).ready(function() {
// 
//   // Check for click events on the navbar burger icon
//   $(".navbar-burger").click(function() {
// 
//       // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
//       $(".navbar-burger").toggleClass("is-active");
//       $(".navbar-menu").toggleClass("is-active");
// 
//   });
// });

