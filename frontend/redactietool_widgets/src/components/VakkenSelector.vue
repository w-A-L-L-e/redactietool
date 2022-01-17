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

      <h3 class="subtitle">Suggesties voor vakken</h3>
      <div class="columns"  v-for="(row, index) in vakken_suggesties" :key="'vak'+index">
        <div class="column is-one-quarter" v-for="vak in row" :key="vak.id">
          <div class="tile is-ancestor">
            <div class="tile is-vertical mr-2 mt-2" >
              <div class="card" >
                <header class="card-header">
                  <p class="card-header-title">
                    {{vak.label}}
                  </p>
                </header>
                <div class="card-content">
                    {{vak.definition}} 
                </div>
                <footer class="card-footer">
                  <a v-on:click="addVakSuggestie(vak)" 
                  class="card-footer-item">Selecteer</a>
                </footer>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h3 class="subtitle">Overige vakken</h3>
      <div class="columns"  v-for="(row2, index2) in overige_vakken" :key="'sug'+index2">
        <div class="column is-one-quarter" v-for="ovak in row2" :key="ovak.id">
          <div class="tile is-ancestor">
            <div class="tile is-vertical mr-2 mt-2" >
              <div class="card" >
                <header class="card-header">
                  <p class="card-header-title">
                    {{ovak.label}}
                  </p>
                </header>
                <div class="card-content">
                    {{ovak.definition}} 
                </div>
                <footer class="card-footer">
                  <a v-on:click="addVakSuggestie(ovak)" 
                  class="card-footer-item">Selecteer</a>
                </footer>
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
        vakken_suggesties:[
          [
            {
              id: "2",
              label: "Suggesties vakken inladen...",
              definition: "Suggesties vakken definitions inladen..."
            }
          ]
        ],
        overige_vakken:[
          [
            {
              id: "3",
              label: "Overige vakken inladen...",
              definition: "Overige vakken definitions inladen..."
            }
          ]
        ]

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
      toggleSuggesties(){
        this.show_vakken_suggesties = !this.show_vakken_suggesties;
        if( this.show_vakken_suggesties ){
          this.suggestie_btn_label = "Verberg suggesties voor vakken";
          console.log("make axios call here...")
        }
        else{
          this.suggestie_btn_label = "Toon suggesties voor vakken";
        }

        var redactie_api_url = 'http://localhost:5000';
        var redactie_api_div = document.getElementById('redactie_api_url');
        if( redactie_api_div ){
          redactie_api_url = redactie_api_div.innerText;
        }
        else{
          return;
        }

        // todo make post call here with some params
        axios
          .get(redactie_api_url+'/vakken')
          .then(res => {
            this.vakken_suggesties = [];
            var row = [];
            var suggest_map = {};
            for( var vak_index in res.data){
              if(vak_index>5) break; //simulate suggestions by only taking first 6
              var vak = res.data[vak_index];
              suggest_map[vak.id] = vak; 
              row.push(vak);
              if(row.length==4){
                this.vakken_suggesties.push(row);
                row=[];
              }
            }
            if(row.length>0){
              this.vakken_suggesties.push(row);
            }
            
            console.log("suggest_map=", suggest_map);

            //nu fetch van alle overige vakken, zijn alle vakken - de suggestions
            axios
              .get(redactie_api_url+'/vakken')
              .then(res2 => {
                this.overige_vakken = [];
                var row2 = [];
                for( var vak_index in res2.data){
                  var ovak = res2.data[vak_index];
                  if(suggest_map[ovak.id] == undefined) row2.push(ovak);

                  if(row2.length>=4){
                    this.overige_vakken.push(row2);
                    row2=[];
                  }
                }
                if(row2.length>0){
                  this.overige_vakken.push(row2);
                }
              })
          })

      },
      addVakSuggestie: function(vak){
        var already_added = false;

        for(var o in this.value){
          var okw = this.value[o];
          if(okw.id == vak.id){
            already_added = true;
            break;
          } 
        }

        if(!already_added){
          const new_vak = {
            id: vak.id,
            label: vak.label,
            definition: vak.definition
          };
          this.options.push(new_vak);
          this.value.push(new_vak);
          this.json_value = JSON.stringify(this.value);
        }
        else{
          this.show_already_added_warning = true;
          setTimeout(()=>{
            this.show_already_added_warning = false;
          }, 3000);
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
    height: 370px;
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
  
  .vakken-suggesties h3 {
    margin-bottom: 5px !important;
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
  .show{
    display: block;
  }
  .hide{
    display: hidden;
  }
</style>
