<template>
  <div id="vakken_selector">

    <a class="button is-link is-small vakken-suggest-button" 
      v-on:click="toggleSuggesties" 
    >
      {{suggestie_btn_label}}
    </a>

    <!-- possibly add this if needed
      open-direction="top"
    -->
    <multiselect v-model="value" 
      tag-placeholder="Selecteer vakken" 
      placeholder="Selecteer vakken" 
      label="label" 
      track-by="id" 
      :options="options" 
      :option-height="104" 
      :show-labels="false"
      :blockKeys="['Delete']"
      :hide-selected="true"
      :multiple="true"
      :loading="vakken_loading"
      :taggable="false" @input="updateValue"
      >

      <template slot="noResult">Vak niet gevonden</template>

      <!--
      custom template styling 
      <template 
        slot="singleLabel" 
        slot-scope="props">
          <span class="option__desc">
            <span class="option__title">
              {{ props.option.label}}
            </span>
            <span class="option_small">
              {{props.option.definition}}
            </span>
          </span>
      </template>

      <template 
        slot="option" 
        slot-scope="props">
          <div class="option__desc">
            <span class="option__title">{{ props.option.label}}</span>
            <span class="option__small">{{ props.option.definition}}</span>
          </div>
      </template>
      -->

    </multiselect>

    <div class="inline-suggesties" v-if="showInlineSuggesties()">
      <div class="inline-suggesties-title">Suggesties</div>

      <div v-if="loading">
        <button class="button is-loading">Loading</button>
      </div>

      <div v-if="!loading" class="inline-suggesties-list">
        <div v-for="(row, index) in suggesties_filtered" :key="'vak'+index">
          <div v-for="vak in row" :key="vak.id"  
                class="inline-suggestie-pill is-pulled-left"
                v-bind:class="[vakIsSelected(vak) ? 'inline-suggestie-selected' : '']"
                v-on:click="toggleVakSelect(vak)">
            {{vak.label}}
          </div>
          <div class="is-clearfix"></div>
        </div>
      </div>
    </div>

    <div class="vakken-suggesties" v-bind:class="[show_vakken_suggesties ? 'show' : 'hide']">

      <div class="modal is-active" id='vakken_modal'>
        <div class="modal-background"></div>
        <div class="modal-card">

          <header class="modal-card-head">
            <p class="modal-card-title">Vakken</p>

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

            <div class="vak-search">
              <div class="field has-addons">
                <div class="control">
                  <input class="input" 
                    type="text"
                    placeholder="Zoek vak"
                    v-on:keydown.enter="zoekVakken($event)"
                    v-model="vakken_search">
                </div>
                <div class="control">
                  <a class="button is-info" v-on:click="zoekVakken($event)">
                    Zoek
                  </a>
                </div>
              </div>
            </div>

          </header>

          <section class="modal-card-body">

            <h3 v-if="suggesties_filtered.length" class="subtitle vakken-title">
              Suggesties
            </h3>

            <div class="columns"  v-for="(row, index) in suggesties_filtered" :key="'vak'+index">
              <div class="column is-one-fifth" v-for="vak in row" :key="vak.id">
                <div class="tile is-ancestor">
                  <div class="tile is-vertical mr-2 mt-2" >
                    <div class="card" 
                      v-on:click="toggleVakSelect(vak)"
                      v-bind:class="[vakIsSelected(vak) ? 'vak-selected' : '']"
                      v-on:mouseover="changeToprowTooltip($event)"
                      >
                      <header class="card-header">
                        <p v-if="show_definitions || !show_tooltips" 
                          class="card-header-title">
                          {{vak.label}}
                        </p>

                        <p v-if="show_tooltips" 
                          class="card-header-title is-primary has-tooltip-arrow has-tooltip-multiline" 
                          :data-tooltip="vak.definition">
                          {{vak.label}}
                        </p>

                      </header>
                      <div class="card-content" v-if="show_definitions">
                          {{vak.definition}} 
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            
            <h3 v-if="suggesties_filtered.length" class="subtitle vakken-title">Overige vakken</h3>

            <div v-if="hogerOfVolwassenOnderwijs()">
              <div class="notification is-info is-light">
              Aan de opgegeven onderwijsniveaus zijn geen vakken gelinkt, wil je toch een vak toevoegen op dit item, selecteer dan kleuter, lager of secundair onderwijs.
              </div>
            </div>

            <h3 v-if="overige_vakken.length && !suggesties_filtered.length && !hogerOfVolwassenOnderwijs()" 
                class="subtitle vakken-title">
              Geen suggesties beschikbaar, volgende vakken zijn mogelijk.
            </h3>

            <div v-if="loading" class="modal-loader">
              <!--progress class="progress is-large is-info" max="100">60%</progress-->
              <button class="button is-loading">Loading</button>
            </div>

            <div v-if="!hogerOfVolwassenOnderwijs()">
              <div class="columns"  v-for="(row2, index2) in overige_filtered" :key="'sug'+index2">
                <div class="column is-one-fifth" v-for="ovak in row2" :key="ovak.id">
                  <div class="tile is-ancestor">
                    <div class="tile is-vertical mr-2 mt-2" >
                      <div class="card" 
                        v-on:click="toggleVakSelect(ovak)"
                        v-bind:class="[vakIsSelected(ovak) ? 'vak-selected' : '']"
                        v-on:mouseover="changeToprowTooltip($event)"
                      >
                        <header class="card-header">
                          <p v-if="show_definitions || !show_tooltips" 
                            class="card-header-title">
                            {{ovak.label}}
                          </p>

                          <p v-if="show_tooltips" 
                            class="card-header-title is-primary has-tooltip-arrow has-tooltip-multiline" 
                            :data-tooltip="ovak.definition">
                            {{ovak.label}}
                          </p>
                        </header>
                        <div class="card-content" v-if="show_definitions">
                            {{ovak.definition}} 
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </section>
          <footer class="modal-card-foot">
            <a class="button is-link close-themas-button" 
              v-on:click="toggleSuggesties($event)">
                Sluiten
            </a>
            <!-- button class="button" onClick="modalCancelClicked();">Annuleren</button -->
          </footer>
        </div>
      </div>

      </div>

    <textarea name="vakken" v-model="json_value" id="vakken_json_value"></textarea>
</div>
</template>

 
<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  //example of default value filled in voor vakken in metadata:
  // var default_value = [{ name: 'Vak 1', code: 'vak1' }]
  var default_value = [];

  export default {
    name: 'VakkenSelector',
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
        options: [],
        show_vakken_suggesties: false,
        suggestie_btn_label: "Toon suggesties voor vakken",
        vakken_suggesties: [],
        suggesties_filtered: [],
        overige_vakken: [],
        overige_filtered: [],
        niveaus: [],
        graden: [],
        themas: [],
        vakken_search: "",
        vakken_prev_search: "",
        show_definitions: false,
        show_tooltips: false,
        loading: false,
        vakken_loading: true
      }
    },
    mounted: function() {
      this.$root.$on('themas_changed', data => {
        // console.log('themas_changed event');
        this.themas = data;
        this.updateSuggestions();
      });

      this.$root.$on('onderwijs_changed', data => {
        this.niveaus = data['niveaus'];
        this.graden = data['graden']
        this.updateSuggestions();
      });

      // these are only emitted in case of comboEnabled=false 
      // aka with the 2 seperate selectors
      this.$root.$on('niveaus_changed', data => {
        this.niveaus = data;
        this.updateSuggestions();
      });

      this.$root.$on('graden_changed', data => {
        this.graden = data;
        this.updateSuggestions();
      });
    },
    created: function() { 
      // smart way to use mocked data during development
      // after deploy in flask this uses a different url on deployed pod
      var redactie_api_url = 'http://localhost:5000';
      var redactie_api_div = document.getElementById('redactie_api_url');
      if( redactie_api_div ){
        redactie_api_url = redactie_api_div.innerText;
      }
      else{ // only load if redactie_api_url div is present
        return;
      }

      this.loading = true;
      axios
        .get(redactie_api_url+'/vakken')
        .then(res => {
          this.options = [];
          for(var i in res.data){
            var vak = res.data[i];
            this.options.push({
              'id': vak.id,
              'label': this.truncateLabel(vak.label),
              'definition': vak.definition
            })
          }
          this.loading = false;
          this.vakken_loading = false;
          this.loadSavedVakken();
        })
    },
    methods: {
      loadSavedVakken(){
        if(this.metadata.item_vakken){
          var vakken = this.metadata.item_vakken;
          this.value = [];
          for(var l in vakken){
            var vak_id = vakken[l]['value'];
            var vak_label = '';
            var vak_def = '';

            // lookup language name
            for( var o in this.options){
              var entry = this.options[o];
              if( entry['id'] == vak_id ){
                vak_label = entry['label'];
                vak_def = entry['definition'];
                break;
              }
            }
            if( vak_label.length>0 ){
              this.value.push(
                {
                  'id': vak_id, 
                  'label': vak_label, 
                  'definition': vak_def
                }
              );
            }
          }
        }
        this.json_value = JSON.stringify(this.value);
        this.$root.$emit('vakken_changed', this.value);
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
        this.$root.$emit('vakken_changed', value);
        this.$root.$emit("metadata_edited", "true");
      },
      vakIsSelected(vak){
        for( var i in this.value ){
          var selected_vak = this.value[i];
          if(vak.id == selected_vak.id) return true;
        }
        return false;
      },
      updateOverigeVakken(suggest_map){
        this.overige_vakken = [];
        var row2 = [];

        for(var vak_index in this.options ){
          var ovak = this.options[vak_index];
          if(suggest_map[ovak.id] == undefined){ 
            // row2.push(ovak);
            // fix duplicate entries 
            row2.push(Object.assign({}, ovak));
          }

          if(row2.length>=5){
            this.overige_vakken.push(row2);
            row2=[];
          }
        }
        if(row2.length>0){
          this.overige_vakken.push(row2);
        }

        this.overige_filtered = JSON.parse(JSON.stringify(this.overige_vakken)); 
      },
      updateSuggestions(){
        var redactie_api_url = 'http://localhost:5000';
        var redactie_api_div = document.getElementById('redactie_api_url');
        if( redactie_api_div ){
          redactie_api_url = redactie_api_div.innerText;
        }
        else{
          return;
        }

        var post_data = {
          'graden': this.graden,
          'themas': this.themas
        }

        if(
            post_data['graden'].length==0 || 
            post_data['themas'].length==0 ||
            this.hogerOfVolwassenOnderwijs()
          ){
          this.vakken_suggesties = []; //clear suggestions
          this.suggesties_filtered = [];
          this.updateOverigeVakken({});
          return;
        }

        this.loading = true;
        axios
          .post(redactie_api_url+'/vakken_suggest', post_data)
          .then(res => {
            this.vakken_suggesties = [];
            var row = [];
            var suggest_map = {};
            for( var vak_index in res.data){
              var vak = res.data[vak_index];
              vak.label = this.truncateLabel(vak.label);
              suggest_map[vak.id] = vak; 
              row.push(Object.assign({}, vak));
              if(row.length>=5){
                this.vakken_suggesties.push(row);
                row=[];
              }
            }
            if(row.length>0){
              this.vakken_suggesties.push(row);
            }
            this.loading = false;
            this.suggesties_filtered = JSON.parse(JSON.stringify(this.vakken_suggesties)); 
            this.updateOverigeVakken(suggest_map);
          })
      },
      toggleSuggesties(event){
        event.preventDefault;
        this.show_vakken_suggesties = !this.show_vakken_suggesties;
        if( this.show_vakken_suggesties ){
          this.suggestie_btn_label = "Verberg suggesties voor vakken";
        }
        else{
          this.suggestie_btn_label = "Toon suggesties voor vakken";
          this.$root.$emit('vakken_changed', this.value);
        }
        
        this.updateSuggestions();
      },
      toggleVakSelect: function(vak){
        var unselect = false;

        for(var o in this.value){
          var okw = this.value[o];
          if(okw.id == vak.id){
            unselect = true;
            this.value.splice(o,1); // remove selection
            break;
          } 
        }

        if(!unselect){
          const new_vak = {
            id: vak.id,
            label: vak.label,
            definition: vak.definition
          };
          // this.options.push(new_vak); //only needed for entirely new vak (create)
          this.value.push(new_vak);
        }
        
        this.json_value = JSON.stringify(this.value);
        this.$root.$emit('vakken_changed', this.value);
        this.$root.$emit("metadata_edited", "true");
      },
      zoek(search_str, src_rows){
        var result = [];
        var row = [];
        for( var ri in src_rows ){
          var src_row = src_rows[ri];
          for( var index in src_row){
            var vak = src_row[index];
            // make searching case insensitive
            var search_lower = search_str.toLowerCase();
            var label = vak.label.toLowerCase();
            var definition = vak.definition.toLowerCase();

            if(label.includes(search_lower) || definition.includes(search_lower)){
              row.push(Object.assign({}, vak));
            }
            if(row.length>=5){
              result.push(JSON.parse(JSON.stringify(row)));
              row=[];
            }
          }
          
        }

        if(row.length>0){
          result.push(JSON.parse(JSON.stringify(row)));
        }
        return result;
      },
      zoekVakken(event){
        this.suggesties_filtered = this.zoek(this.vakken_search, this.vakken_suggesties);
        this.overige_filtered = this.zoek(this.vakken_search, this.overige_vakken);

        this.vakken_prev_search = this.vakken_search;
        this.vakken_search = ""; //clear for next search
        event.preventDefault();
      },
      changeToprowTooltip(event){
        // attempt to make top row tooltip show on bottom
        // console.log(event);
        var pos = event.clientY; //pageY doesnt work right

        if(pos<200){
          event.target.classList.add('has-tooltip-bottom')
        }
        else{
          event.target.classList.remove('has-tooltip-bottom')
        }
        return true;
      },
      truncateLabel(text) {
        var length=45;
        var suffix='...';
        if (text.length > length) {
          return text.substring(0, length) + suffix;
        } 
        else{
          return text;
        }
      },
      hogerOfVolwassenOnderwijs(){
        for(var i in this.niveaus){
          var niv = this.niveaus[i];
          if(niv.id.includes('kleuter')) return false;
          if(niv.id.includes('lager')) return false;
          if(niv.id.includes('secundair')) return false;
        }

        // enkel hoger, volwassen of geen niveaus geselecteerd
        return true;
      },
      toggleTooltips(){
        this.show_definitions = false;
      },
      toggleBeschrijvingen(){
        this.show_tooltips = false;
      },
      showInlineSuggesties(){
        if( !this.suggesties_filtered.length ) return false;
        //algernate if we hide suggests: also return false if all suggestions are selected
        return true;
      }

    },
    filters: {
      truncate: function (text, length, suffix) {
        if (text.length > length) {
          return text.substring(0, length) + suffix;
        } 
        else{
          return text;
        }
      }
    }
  }
</script>

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #vakken_selector{
    min-width: 25em;
  }
  #vakken_json_value{
    margin-top: 20px;
    margin-bottom: 20px;
    display: flex;
    width: 80%;
    height: 100px;
    display: none;
  }
  .vakken-suggest-button{
    display: inline-block;
    margin-bottom: 10px;
  }
  .vakken-suggesties {
    height: 410px;
    overflow-y: scroll;
    overflow-x: hidden;
    border: 1px solid #e8e8e8;
    padding: 5px;
    border-radius: 5px;
    width: 45em;
    padding-left: 12px;
    padding-right: 15px;
  }
  .tile {
    margin-right: -30px;
    margin-left: 0px;
  }
  
  .vak-warning-pill{
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
  }
  
  .vakken-title{
    margin-left: -10px !important;
    padding-bottom: 10px !important;
    margin-top: 0px !important;
    margin-bottom: 5px !important;
    color: #222;
  }

  /* use for custom template
  .multiselect__element{
    max-width: 50em;
  }

  .multiselect__content{
    max-width: 50em;
  }

  .option__title{
    overflow-wrap: anywhere;
    max-width: 50em;
  }
  .option__small {
    overflow-wrap: anywhere;
    max-width: 50em;
  }*/

  .card{
    cursor: pointer;
  }

  header.card-header{
    background-color: #edeff2;
    color: #2b414f;
  }
  .vak-selected header.card-header{
    background: #3e8ed0;
  }
  .vak-selected .card-header-title{
    color: #fff;
  }
  .vak-selected .card-content {
    border: 1px solid #9cafbd;
  }

  .show{
    display: block;
  }
  
  .hide{
    display: hidden;
  }

  .inline-suggesties{
    margin-top: 10px;
  }

  .inline-suggesties-list{
    max-height: 150px;
    overflow-y: auto;
  }

  .inline-suggesties-title{
    font-weight: bold;
    margin-bottom: 5px;
    color: #363636;
  }
  .inline-suggestie-pill {
    border-radius: 5px;
    border: 1px solid #9cafbd;
    background-color: #eff5fb;
    color: #296fa8;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 8px;
    padding: 0px 8px 0px 8px;
    margin-bottom: 5px;
    cursor: pointer;
  }
  .inline-suggestie-selected{
    background-color: #93b6d3;
    border: 1px solid #9cafbd;
    color: #fff;
  }

  .modal-loader {
    text-align: center;
    height: 54px;
    margin-top: -52px;
  }

  #vakken_modal .modal-content {
    width: 900px;
  }

  @media screen and (min-width: 769px){
    #vakken_modal .modal-content, #vakken_modal .modal-card {
      margin: 0 auto;
      max-height: calc(100vh - 40px);
      width: calc(100vw - 50px);
    }
  }
  #vakken_modal .modal-card-head, #vakken_modal .modal-card-foot{
    padding-top: 5px;
    padding-bottom: 5px;
  }

</style>
