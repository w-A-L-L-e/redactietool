<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label" v-if="!comboEdit">Onderwijsgraden</label>
      <label class="label" v-if="comboEdit"></label>
    </div>
    <div class="field-body">
      <div id="onderwijsgraden_selector"> 

        <span v-if="!comboEdit">
          <multiselect v-model="value" 
            placeholder="Selecteer onderwijsgraden" 
            label="label" 
            track-by="id" 
            :options="graden_filtered"
            :multiple="true" 
            :show-labels="false"
            :hide-selected="true"
            :taggable="false" 
            :searchable="false"
            :loading="loading"
            @input="updateValue" @remove="removeGraad">
             
            <template slot="noResult">Onderwijsgraad niet gevonden</template>
            <template slot="noOptions">
              Selecteer secundair of lager in onderwijsniveaus
            </template>
          </multiselect>
        </span>

        <div v-if="comboEdit && value.length" class="inline-graden-wrapper">
          <div class="graden-inline-title">Onderwijsgraden</div>
          <div class="inline-graden-list">
            <div 
              class="graden-pill is-pulled-left" 
              v-for="graad in value" 
              :key="graad.id"
              >
              {{graad.label}}
            </div>
            <div class="is-clearfix"></div>
          </div>
        </div>

        <textarea name="lom1_onderwijsgraden" v-model="json_value" id="onderwijsgraden_json_value"></textarea>
      </div>
    </div>
  </div>

</template>

<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  var default_value = []  

  export default {
    name: 'OnderwijsgradenSelector',
    components: {
      Multiselect 
    },
    props: {
      comboEdit: Boolean
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { 
            id: "loading...", 
            label: "Onderwijsgraden inladen...", 
            definition: "Onderwijsgraden inladen..."
          },
        ],
        niveaus: [],
        graden_filtered: [],
        loading: false
      }
    },
    mounted: function() {
      this.$root.$on('niveaus_changed', data => {
        this.niveaus = data;
        this.filterGraden();
      });

      this.$root.$on('onderwijs_changed', data => {
        this.niveaus = data['niveaus'];
        this.value = data['graden']
        this.json_value = JSON.stringify(this.value);
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
        return; // do not load on other redactietool pages
      }
      this.loading = true;
      axios
        .get(redactie_api_url+'/onderwijsgraden')
        .then(res => {
          // populate all possible options
          this.options = res.data;
          this.$root.$emit('graden_options_loaded', this.options);

          // set selected options for this specific item
          this.value = [];

          var value_div = document.getElementById("item_onderwijsgraden");
          if(value_div){
            var onderwijsgraden = JSON.parse(value_div.innerText);
            var option_item = {};

            // do fallback, in case only old string values are present
            if(value_div && onderwijsgraden['show_legacy'] ){
              console.log("legacy fallback voor onderwijsgraden (lom_typicalagerange)...");
              var value_div_legacy = document.getElementById("item_onderwijsgraden_legacy");
              if(value_div_legacy){
                var values = JSON.parse(value_div_legacy.innerText);
                var item = {};
                for(var k in values){
                  var definition = values[k]['value'];
                  item['definition'] = definition;
                  
                  //get id corresponding to def
                  for( var i in this.options ){
                    option_item = this.options[i];
                    if( item['definition'] == option_item['definition'] ){
                      item['id'] = option_item['id'];
                      item['label'] = option_item['label']
                      this.value.push( {
                        id: item['id'],
                        label: item['label'],
                        definition: item['definition']
                      });
                      break;
                    }
                  }
                }
              }
            }
            else{
              console.log("loading new onderwijsgraden from (lom_onderwijsgraad)...");
              for(var o in onderwijsgraden){
                var item_id = onderwijsgraden[o]['value'];
                //get label and definition
                for(var j in this.options ){
                  option_item = this.options[j];
                  if( item_id == option_item['id'] ){
                    this.value.push({
                      'id': item_id,
                      'label': option_item['label'],
                      'definition': option_item['definition']
                    });
                    break;
                  }
                }

              }
            }
            this.filterGraden();
            this.json_value = JSON.stringify(this.value);
            this.$root.$emit('graden_changed', this.value);
          }
          this.loading = false;

        });
    },
    methods: {
      removeGraad(graad){
        // todo give this warning if vakken are selected: 
        // “Opgelet: indien je deze waarde verwijdert, zijn mogelijks een aantal vakken niet meer relevant
        console.log("removed graad, check vakken values and give warning here=", graad);
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
        this.$root.$emit('graden_changed', value);
      },
      filterGraden(){
        // check niveau and only show related graden
        // TODO: ask miel for a call to do this without hardcoding
        // We need the parent id on niveaus or something...
        var showLager = false;
        var showSecundair = false;
        for(var n in this.niveaus){
          var niv = this.niveaus[n];
          if(niv.label.includes("Secundair")) showSecundair = true;
          if(niv.label.includes("Lager")) showLager = true;
        }

        this.graden_filtered = [];
        for(var i in this.options){
          var graad = this.options[i];
          if(
              (showSecundair && graad.label.includes("Secundair")) ||
              (showLager && graad.label.includes("Lager"))
            ){

            this.graden_filtered.push(graad);
          }
        }
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #onderwijsgraden_selector{
    min-width: 30em;
  }

  #onderwijsgraden_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .graden-inline-title{
    font-weight: bold;
    margin-bottom: 5px;
    color: #363636;
  }

  .inline-graden-list{
    /*
    max-height: 150px;
    overflow-y: auto;
    */
  }

  .graden-pill{
    border-radius: 5px;
    border: 1px solid #9cafbd;
    background-color: #edeff2;
    color: #2b414f;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 8px;
    padding: 0px 8px 0px 8px;
    margin-bottom: 5px;
  }

  .inline-graden-wrapper{
    margin-top: -8px;
  }

</style>
