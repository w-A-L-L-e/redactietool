<template>
  <div id="vakken_selector">
    <multiselect v-model="value" 
      id="vakken_multiselect"
      tag-placeholder="Kies vakken" 
      placeholder="Zoek vak" 
      label="label" 
      track-by="id" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">

      <template slot="noResult">Vak niet gevonden</template>

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

    </multiselect>

    <a class="button is-link is-small vakken-suggest-button" 
      v-on:click="toggleSuggesties" 
    >
      {{suggestie_btn_label}}
    </a>

    <div class="vak-warning-pill" v-bind:class="[show_already_added_warning ? 'show' : 'hide']">
    Vak werd al toegevoegd
  </div>

    <div class="vakken-suggesties" v-bind:class="[show_vakken_suggesties ? 'show' : 'hide']">

      <h3 class="subtitle vakken-title">Suggesties voor vakken</h3>

      <div v-if="!vakken_suggesties.length" class="notification is-info is-light">
        Geen suggesties gevonden. Probeer andere themas of onderwijsgraden te selecteren.
      </div>

      <div class="columns"  v-for="(row, index) in vakken_suggesties" :key="'vak'+index">
        <div class="column is-one-quarter" v-for="vak in row" :key="vak.id">
          <div class="tile is-ancestor">
            <div class="tile is-vertical mr-2 mt-2" >
              <div class="card" 
                v-on:click="toggleVakSelect(vak)"
                v-bind:class="[vakIsSelected(vak) ? 'vak-selected' : '']"
                >
                <header class="card-header">
                  <p class="card-header-title">
                    {{vak.label}}
                  </p>
                </header>
                <div class="card-content">
                    {{vak.definition}} 
                </div>
                <!--footer class="card-footer">
                  <a v-on:click="toggleVakSelect(vak)" 
                  class="card-footer-item">Selecteer</a>
                </footer-->
              </div>
            </div>
          </div>
        </div>
      </div>

      <h3 class="subtitle vakken-title">Overige vakken</h3>
      <div class="columns"  v-for="(row2, index2) in overige_vakken" :key="'sug'+index2">
        <div class="column is-one-quarter" v-for="ovak in row2" :key="ovak.id">
          <div class="tile is-ancestor">
            <div class="tile is-vertical mr-2 mt-2" >
              <div class="card" 
                v-on:click="toggleVakSelect(ovak)"
                v-bind:class="[vakIsSelected(ovak) ? 'vak-selected' : '']"
              >
                <header class="card-header">
                  <p class="card-header-title">
                    {{ovak.label}}
                  </p>
                </header>
                <div class="card-content">
                    {{ovak.definition}} 
                </div>
                <!--footer class="card-footer">
                  <a v-on:click="toggleVakSelect(ovak)" 
                  class="card-footer-item">Selecteer</a>
                </footer-->
              </div>
            </div>
          </div>
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
    props: {},
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { 
            id: "1", 
            label: "Vakken inladen...", 
            definition: "Vakken inladen..."
          },
        ],
        show_vakken_suggesties: false,
        show_already_added_warning: false,
        suggestie_btn_label: "Toon suggesties voor vakken",
        vakken_suggesties:[],
        overige_vakken:[],
        graden: [],
        themas: []
      }
    },
    mounted: function() {
      this.$root.$on('graden_changed', data => {
        console.log('graden changed data=', data);
        this.graden = data;
        this.updateSuggestions();
      });

      this.$root.$on('themas_changed', data => {
        console.log('themas changed data=',data);
        this.themas = data;
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
      else{
        return;
      }

      // only load if redactie_api_url div is present
      axios
        .get(redactie_api_url+'/vakken')
        .then(res => {
          this.options = res.data;
        })
    },
    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
      },
      vakIsSelected(vak){
        for( var i in this.value ){
          var selected_vak = this.value[i];
          if(vak.id == selected_vak.id) return true;
        }
        return false;
      },
      updateOverigeVakken(redactie_api_url, suggest_map){
        //nu fetch van alle overige vakken, zijn alle vakken - de suggestions
        axios
          .get(redactie_api_url+'/vakken')
          .then(res2 => {
            this.overige_vakken = [];
            var row2 = [];
            for( var vak_index in res2.data){
              var ovak = res2.data[vak_index];
              if(suggest_map[ovak.id] == undefined){ 
                // row2.push(ovak);
                // fix duplicate entries 
                row2.push(Object.assign({}, ovak));
              }

              if(row2.length>=4){
                this.overige_vakken.push(row2);
                row2=[];
              }
            }
            if(row2.length>0){
              this.overige_vakken.push(row2);
            }
          })
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

        if(!this.show_vakken_suggesties){
          console.log("Vakken suggestions is closed, not loading...");
          return;
        }

        var post_data = {
          'graden': this.graden,
          'themas': this.themas
        }

        if(post_data['graden'].length==0 || post_data['themas'].length==0 ){
          this.vakken_suggesties = []; //clear suggestions
          this.updateOverigeVakken(redactie_api_url, {});
          return;
        }

        axios
          .post(redactie_api_url+'/vakken_suggest', post_data)
          .then(res => {
            this.vakken_suggesties = [];
            var row = [];
            var suggest_map = {};
            for( var vak_index in res.data){
              //if(vak_index>5) break; //simulate suggestions by only taking first 6
              var vak = res.data[vak_index];
              suggest_map[vak.id] = vak; 
              row.push(Object.assign({}, vak));
              if(row.length==4){
                this.vakken_suggesties.push(row);
                row=[];
              }
            }
            if(row.length>0){
              this.vakken_suggesties.push(row);
            }
            
            console.log("suggest_map=", suggest_map);
            this.updateOverigeVakken(redactie_api_url, suggest_map);
          })
      },
      toggleSuggesties(){
        this.show_vakken_suggesties = !this.show_vakken_suggesties;
        if( this.show_vakken_suggesties ){
          this.suggestie_btn_label = "Verberg suggesties voor vakken";
          console.log("make axios call here...")
        }
        else{
          this.suggestie_btn_label = "Toon suggesties voor vakken";
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
            this.json_value = JSON.stringify(this.value);
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
          this.json_value = JSON.stringify(this.value);
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
    min-width: 30em;
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
    margin-top: 10px;
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

   /*
  .card-footer-item{
    padding: 0.2em;
    background-color: #3e8ed0;
    color: #fff;
  }
  .card-footer-item:hover{
    padding: 0.2em;
    background-color: #3488be;
    color: #fff;
  }*/


  .show{
    display: block;
  }
  
  .hide{
    display: hidden;
  }
</style>
