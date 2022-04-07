<template>
<div id="thema_selector">

  <a class="button is-link is-small toon-themas-button" 
      v-on:click="toggleThemas" 
    >
      {{show_themas_label}}
  </a>

  <multiselect v-model="value" 
    tag-placeholder="Voeg nieuw thema toe" 
    placeholder="Selecteer thema's" 
    label="label" 
    track-by="id" 
    :options="options" 
    :option-height="104" 
    :show-labels="false"
    :blockKeys="['Delete']"
    :hide-selected="true"
    :multiple="true"
    :loading="loading"
    :taggable="false" @input="updateValue"
  >

    <template slot="noResult">Thema niet gevonden</template>

  </multiselect>

  <div class="thema-cards" v-bind:class="[show_thema_cards ? 'show' : 'hide']">

    <div class="modal is-active" id="thema_modal">
      <div class="modal-background"></div>
      <div class="modal-card" id="thema_modal_card">
        <header class="modal-card-head">
          <p class="modal-card-title">Thema's</p>

          <label class="checkbox thema-show-def-selector">
            <input
              type="checkbox"
              v-model="show_tooltips"
              v-on:click="toggleTooltips()"
            >
            Tooltips
          </label>

          <label class="checkbox thema-show-def-selector">
            <input
              type="checkbox"
              v-model="show_definitions"
              v-on:click="toggleBeschrijvingen()"
            >
            Beschrijvingen
          </label>

          <div class="thema-search">
            <div class="field has-addons">
              <div class="control">
                <input class="input" 
                  type="text"
                  placeholder="Zoek thema"
                  v-on:keydown.enter="zoekThemas($event)"
                  v-model="thema_search">
              </div>
              <div class="control">
                <a class="button is-info" v-on:click="zoekThemas($event)">
                  Zoek
                </a>
              </div>
            </div>
          </div>
        </header>

        <section class="modal-card-body">
          <div class="thema-warning-pill"
                v-bind:class="[show_already_added_warning ? 'show' : 'hide']">
            Thema werd al toegevoegd
          </div>

          <div v-if="!thema_cards.length" class="notification is-info is-light">
            Geen themas gevonden met de zoekterm "{{ thema_prev_search }}".
          </div>

          <div class="columns"  v-for="(row, index) in thema_cards" :key="index">
            <div class="column is-one-fifth" v-for="thema in row" :key="thema.id">
              <div class="tile is-ancestor">
                <div class="tile is-vertical mr-2 mt-2" >
                  <div class="card" 
                    v-on:click="toggleThemaSelect(thema)"
                    v-on:mouseover="changeToprowTooltip($event)"
                    v-bind:class="[themaIsSelected(thema) ? 'thema-selected' : '']"
                    >

                    <header class="card-header">
                      <p v-if="show_definitions || !show_tooltips" 
                        class="card-header-title">
                        {{thema.label}}
                      </p>

                      <p v-if="show_tooltips" 
                        class="card-header-title is-primary
                        has-tooltip-arrow has-tooltip-multiline" 
                        :data-tooltip="thema.definition">
                        {{thema.label}}
                      </p>
                    </header>

                    <div class="card-content" v-if="show_definitions">
                        {{thema.definition}} 
                    </div>

                  </div>
                </div>
              </div>

            </div>
          </div>
        </section>

        <footer class="modal-card-foot">
          <a class="button is-link close-themas-button" 
            v-on:click="toggleThemas($event)">
              Sluiten
          </a>
        </footer>
      </div>
    </div>

  </div>

  <textarea name="themas" v-model="json_value" id="thema_json_value"></textarea>

</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  var default_value = []; 

  export default {
    name: 'ThemaSelector',
    components: {
      Multiselect 
    },
    props: {
      metadata: Object
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { 
            id: "", 
            label: "Themas inladen...", 
            definition: "Themas inladen..."
          },
        ],
        thema_cards: [],
        show_thema_cards: false,
        show_already_added_warning: false,
        show_themas_label: "Toon themas",
        thema_search: "",
        thema_prev_search: "",
        show_definitions: false,
        show_tooltips: true,
        loading: true
      }
    },
    created: function() { 
      // smart way to use mocked data during development
      // after deploy in flask this uses a different url on deployed pod
      var redactie_api_url = 'http://localhost:5000';
      var redactie_api_div = document.getElementById('redactie_api_url');
      if( redactie_api_div ){
        redactie_api_url = redactie_api_div.innerText;
      }
      else{
        return;
      }
      axios
        .get(redactie_api_url+'/themas')
        .then(res => {
          this.options = [];
          //only add non-empty labels
          for(var o in res.data){
            var thema = res.data[o];
            if(thema.label.length>1){
              this.options.push({
                'id': thema.id,
                'label': this.truncateLabel(thema.label),
                'definition': thema.definition
              });
            }
          }
          this.loadSavedThemas();
        })
    },
    methods: {
      loadSavedThemas(){
        if(this.metadata.item_themas){
          var themas = this.metadata.item_themas;
          this.value = [];
          for(var l in themas){
            var thema_id = themas[l]['value'];
            var thema_label = '';
            var thema_def = '';

            // lookup language name
            for( var o in this.options){
              var entry = this.options[o];
              if( entry['id'] == thema_id ){
                thema_label = entry['label'];
                thema_def = entry['definition'];
                break;
              }
            }
            if( thema_label.length>0 ){
              this.value.push(
                {
                  'id': thema_id, 
                  'label': thema_label, 
                  'definition': thema_def
                }
              );
            }
          }
        }
        this.loading = false;
        this.json_value = JSON.stringify(this.value);
        this.$root.$emit('themas_changed', this.value);
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
        this.$root.$emit('themas_changed', value);
        this.$root.$emit("metadata_edited", "true");
      },
      zoekThemas(event){
        this.thema_cards = [];
        var row = [];
        for( var thema_index in this.options){
          var thema = this.options[thema_index];
          // make searching case insensitive
          var search_lower = this.thema_search.toLowerCase();
          var thema_label = thema.label.toLowerCase();
          var thema_definition = thema.definition.toLowerCase();

          if(thema_label.includes(search_lower) || thema_definition.includes(search_lower)){
            row.push(Object.assign({}, thema));
          }
          if(row.length==5){
            this.thema_cards.push(JSON.parse(JSON.stringify(row)));
            row=[];
          }
        }
        if(row.length>0){
          this.thema_cards.push(JSON.parse(JSON.stringify(row)));
        }
        this.thema_prev_search = this.thema_search;
        this.thema_search = ""; //clear for next search
        event.preventDefault();
      },
      themaIsSelected(thema){
        for( var i in this.value ){
          var selected_thema = this.value[i];
          if(thema.id == selected_thema.id) return true;
        }
        return false;
      },
      toggleThemas(event){
        event.preventDefault;
        this.show_thema_cards = !this.show_thema_cards;
        if( this.show_thema_cards ){
          this.show_themas_label = "Verberg themas";
        }
        else{
          // upon closing thema modal we emit the changed selections
          this.show_themas_label = "Toon themas";
          this.thema_cards = [];
          this.$root.$emit('themas_changed', this.value);
          return;
        }

        this.thema_cards = [];
        var row = [];
        for( var thema_index in this.options){
          row.push(this.options[thema_index]);
          if(row.length==5){
            this.thema_cards.push(row);
            row=[];
          }
        }
        if(row.length>0){
          this.thema_cards.push(row);
        }
      },
      toggleThemaSelect: function(thema){
        var unselect = false;

        for(var o in this.value){
          var okw = this.value[o];
          if(okw.id == thema.id){
            unselect = true;
            this.value.splice(o,1); // remove selection
            this.json_value = JSON.stringify(this.value);
            break;
          } 
        }

        if(!unselect){
          const new_thema = {
            id: thema.id,
            label: thema.label,
            definition: thema.definition
          };
          this.value.push(new_thema);
          this.json_value = JSON.stringify(this.value);
          // this works but hammers the suggest lib on each card selection
          // this.$root.$emit('themas_changed', this.value);
          this.$root.$emit("metadata_edited", "true");
        }
      },
      changeToprowTooltip(event){
        var btnY = event.clientY;
        var modalTop = document.getElementById("thema_modal_card").getBoundingClientRect().top
        var pos = btnY - modalTop;

        // make top rows tooltip position bottom so it isn't hidden outside dialog
        if(pos<200){
          event.target.classList.add('has-tooltip-bottom')
        }
        else{
          event.target.classList.remove('has-tooltip-bottom')
        }
        return true;
      },
      truncateLabel: function (text) {
        var length=45;
        var suffix='...';
        if (text.length > length) {
          return text.substring(0, length) + suffix;
        } 
        else{
          return text;
        }
      },
      toggleTooltips(){
        this.show_definitions = false;
      },
      toggleBeschrijvingen(){
        this.show_tooltips = false;
      },
    },
    filters: {
      truncate: function (text, length, suffix) {
        if (text.length > length) {
          return text.substring(0, length) + suffix;
        } 
        else{
          return text;
        }
      },
    }

  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #thema_selector{
    min-width: 25em;
  }

  #thema_json_value{
    /*display: flex;*/
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
    display: none;
  }

  .toon-themas-button {
    margin-bottom: 10px;
  }

  .close-themas-button{
    margin-left: auto;
    margin-right: auto;
  }

  .thema-cards {
    height: 370px;
    overflow-y: scroll;
    overflow-x: hidden;
    border: 1px solid #e8e8e8;
    padding: 5px;
    border-radius: 5px;
    width: 55em;
    padding-left: 12px;
    padding-right: 15px;
  }
  .tile {
    margin-right: -30px;
    margin-left: 0px;
  }
  
  .card-header-title {
    height: 50px;
    overflow-y: scroll;
    overflow-wrap: anywhere;
    font-size: 14px;
    padding: 4px 15px;
  }
  .card-content {
    overflow-wrap: anywhere;
    font-size: 12px;
    padding: 4px 10px;
    height: 120px;
    overflow-y: scroll;
  }
  
  .show{
    display: block;
  }
  .hide{
    display: hidden;
  }

  .thema-show-def-selector {
    float: right;
    display: inline-block;
    margin-top: 5px;
    margin-right: 20px;
  }
  .thema-search {
    float: right;
    display: inline-block;
    margin-top: 10px;
    margin-bottom: 5px;
  }
  .thema-warning-pill{
    border-radius: 5px;
    background: #ff6a6a;
    color: #eee;
    display: inline-block;
    float: right;
    text-overflow: ellipsis;
    padding: 2px 8px 2px 13px;
    margin-bottom: 5px;
    width: 15em;
    margin-top: 10px;
    margin-right: 10px;
  }
 
  .card{
    cursor: pointer;
  }

  header.card-header{
    background-color: #edeff2;
    color: #2b414f;
  }
  .thema-selected header.card-header{
    background: #3e8ed0;
  }
  .thema-selected .card-header-title{
    color: #fff;
  }
  .thema-selected .card-content {
    border: 1px solid #9cafbd;
  }

    
  .hide{
    display: none;
  }
  .show{
    display: block;
  }

  #thema_modal .modal-content {
    width: 900px;
  }

  @media screen and (min-width: 769px){
    #thema_modal .modal-content, #thema_modal .modal-card {
      margin: 0 auto;
      max-height: calc(100vh - 40px);
      width: calc(100vw - 50px);
    }
  }

  #thema_modal .modal-card-head, #thema_modal .modal-card-foot{
    padding-top: 5px;
    padding-bottom: 5px;
  }

  /* delay en fade-in op tooltips zodat tijdens snel editen de tooltips niet zo veel storen */
  [data-tooltip]:not([disabled]):hover:before {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.3s;
    transition-delay: 0.8s;
    transition-property: opacity;
  }

  [data-tooltip]:not([disabled]):hover:after{
    visibility: visible;
    opacity: 1;
    transition: opacity 0.3s;
    transition-delay: 0.8s;
    transition-property: opacity;
  }

</style>
