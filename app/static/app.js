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


// ============================ LOGIN/LOGOUT FORMS =============================
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

function logoutClicked(ref){
  // #logout_btn
  ref.className += ' disabled';
}

function newUploadClicked(ref){
  // #new_upload_btn
  ref.className += ' disabled';
}

function clearButtonLoadingState(){
  // TODO: put all buttons back in original state 
  // this is similar to hideEmptyTitles but instead we modify
  // a class and/or replace the button.value back
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


// ============================== SUBTITLE FORMS ===============================
function pidSubmitForSubtitles(btn){
  hf = document.getElementById('redirect_subtitles');
  hf.value = 'yes';
  window.localStorage.removeItem("productie_section_opened");
  execute(btn, 'Item opzoeken...');
}

function pidSubmitForMetadata(btn){
  hf = document.getElementById('redirect_subtitles');
  hf.value = 'no';
  window.localStorage.removeItem("productie_section_opened");
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


// ============================ METADATA EDIT FORM =============================
// add item method for 'productie' section
function addPrdItem(item_list_id, item_fields_id){
  var item_fields = document.getElementById(item_fields_id);
  if(!item_fields){
    console.log("ERROR in addPrdItem: could not find item_fields_id=", item_fields_id);
    return false;
  }

  var item_list = document.getElementById(item_list_id);
  if(!item_list){
    console.log("ERROR in addPrdItem: could not find item_list_id=", item_list_id);
    return false;
  }

  // add unique ids to _input_ and _value_ fields in cloned element
  var new_id = 1;
  var item_inputs = item_list.getElementsByTagName("input");
  if(item_inputs.length){
    var last_id = item_inputs[item_inputs.length-1].id
    if(last_id.includes("_value_")){
      new_id = parseInt(last_id.replace(item_fields_id+'_value_', ''))+1
    }
  }

  var fields_clone = item_fields.cloneNode(true);
  //fields_clone.style.display = 'flex';
  fields_clone.id = fields_clone.id+"_"+new_id;
  fields_clone.getElementsByTagName("select")[0].name = item_fields_id+"_attribute_"+new_id
  fields_clone.getElementsByTagName("select")[0].id = item_fields_id+"_attribute_"+new_id
  fields_clone.getElementsByTagName("input")[0].name = item_fields_id+"_value_"+new_id
  fields_clone.getElementsByTagName("input")[0].id = item_fields_id+"_value_"+new_id

  // now append our cloned fields with unique name+id
  console.log("adding item_fields=", fields_clone);
  item_list.append(fields_clone);
  return false;
}

// delete item method for 'productie' section item
function deletePrdItem(del_btn){
  del_btn.parentNode.parentNode.remove();
  return false;
}

function closeSection(section_div_id){
  var form_section = document.getElementById(section_div_id);
  if(!form_section) return;
  var close_icon_wrapper = document.getElementById(section_div_id + "_icon");
  var folded_icon = close_icon_wrapper.getElementsByClassName("icon-folded")[0];
  var unfolded_icon = close_icon_wrapper.getElementsByClassName("icon-unfolded")[0];

  form_section.style.display="none";
  unfolded_icon.style.display="none";
  folded_icon.style.display="block";
}

function openSection(section_div_id){
  var form_section = document.getElementById(section_div_id);
  if(!form_section) return;
  var close_icon_wrapper = document.getElementById(section_div_id + "_icon");
  var folded_icon = close_icon_wrapper.getElementsByClassName("icon-folded")[0];
  var unfolded_icon = close_icon_wrapper.getElementsByClassName("icon-unfolded")[0];

  form_section.style.display="block";
  unfolded_icon.style.display="block";
  folded_icon.style.display="none";
}

function sectionToggle(section_div_id){
  var form_section = document.getElementById(section_div_id);
  if(!form_section) return;
 
  if(form_section.style.display == 'none'){
    if(section_div_id=="productie_section"){
      window.localStorage.setItem("productie_section_opened", "true");
    }
    openSection(section_div_id);
  }
  else{
    if(section_div_id=="productie_section"){
      window.localStorage.removeItem("productie_section_opened");
    }

    closeSection(section_div_id);
  }
}

function updateProductionSection(){
  // use localstorage to keep state of opened production section
  if(window.localStorage.getItem("productie_section_opened") == "true"){
    openSection("productio_section");
  }
  else{
    closeSection("productie_section");
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

function closeAlert(){
  var alert_box = document.getElementById("alert_box");
  if(alert_box){
    alert_box.style.display = "none";
  }
}

function autoCloseAlert(){
  setTimeout(function(){
    closeAlert();
  }, 4000); 
}

function refreshKeyframeImage(img_id){
  console.log("can be added later if mediahaven changes the previewImageUrl on keyframe change...");
  // we need to reload the background image url by finding flowplayer's id and then going down
  // in dom and update background tag.
}

function injectApiUrl(url_div_id){
  var api_url_div = document.getElementById('redactie_api_url');
  if(api_url_div){
    api_url_div.innerText = window.location.protocol+'//'+window.location.host;
  }
  else{
    console.log("Warning could not inject api url into div=", url_div_id);
  }
}

function checkPageSaved(){
  //window.addEventListener('beforeunload', function (e) {
  //  // Cancel the event as stated by the standard.
  //  e.preventDefault();
  //  // Chrome requires returnValue to be set.
  //  e.returnValue = '';


    // event.preventDefault();
    // return event.returnValue = "Ben je zeker?";
  //  console.log("HIER EEN CUSTOM DIALOG!!!")
  //});

  window.onbeforeunload = (event) => {
    console.log("HIER EEN CUSTOM DIALOG!!!")
    if (false) {
      return "";
    }
  };
}


// =========================== DOCUMENT READY EVENT ============================
// Handle burger menu open/close on all pages.
// Handle collapsing and hiding of inputs, textareas 
// and notifications on the metadata edit form
// Handle any other resetting of state on pageload if necessary
document.addEventListener('DOMContentLoaded', () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll('.navbar-burger'), 0
  );

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
  autoCloseAlert();
  clearButtonLoadingState();
  updateProductionSection();
  
  // For demo, show modal dialogs
  // ============================
  // showNavigationWarning();
  // flashModalWarning();
  // showModalAlert("hello", "world");
});

