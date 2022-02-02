<template>
  <div class="field is-horizontal">
    <div class="field-label is-normal">
      <label class="label" v-if="!comboEdit">Onderwijsniveaus</label>
      <label class="label" v-if="comboEdit"></label>
    </div>
    <div class="field-body">
      <div id="onderwijsniveaus_selector"> 
        <span v-if="!comboEdit">
          <multiselect v-model="value" 
            placeholder="Selecteer onderwijsniveaus" 
            label="label" 
            track-by="id" 
            :options="options"
            :multiple="true" 
            :show-labels="false"
            :hide-selected="true"
            :searchable="false"
            :taggable="false"
            @input="updateValue">

            <template slot="noResult">Onderwijsniveau niet gevonden</template>

          </multiselect>
        </span>

        <div v-if="comboEdit && value.length" class="inline-niveau-wrapper">
          <div class="niveau-inline-title">Onderwijsniveaus</div>
          <div class="inline-niveau-list">
            <div 
              class="niveau-pill" 
              v-for="niveau in value" 
              :key="niveau.id"
              >
              {{niveau.label}}
            </div>
          </div>
        </div>
        
        <textarea name="lom1_onderwijsniveaus" v-model="json_value" id="onderwijsniveaus_json_value"></textarea>
      </div>
    </div>
  </div>
</template>


<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  // todo: load in this from mam or jinja view and what is the mapping?
  var default_value = []  

  export default {
    name: 'OnderwijsniveausSelector',
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
            id: "", 
            label: "Onderwijsniveaus inladen...", 
            definition: "Onderwijsniveaus inladen..."
          },
        ]
      }
    },
    mounted: function() {
      this.$root.$on('onderwijs_changed', data => {
        this.value = data['niveaus']
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
        return;
      }

      axios
        .get(redactie_api_url+'/onderwijsniveaus')
        .then(res => {
          this.options = res.data;
          this.$root.$emit('niveau_options_loaded', this.options);

          // set selected options for this specific item
          this.value = [];

          var value_div = document.getElementById("item_onderwijsniveaus");
          if(value_div){
            var onderwijsniveaus = JSON.parse(value_div.innerText);
            var item = {};
            var option_item = {};

            // do fallback, in case only old string values are present
            if( onderwijsniveaus['show_legacy'] ){
              console.log("legacy fallback voor onderwijsniveaus (lom_context)...");
              var value_div_legacy = document.getElementById("item_onderwijsniveaus_legacy");
              if(value_div_legacy){
                var values = JSON.parse(value_div_legacy.innerText);
                for(var k in values){
                  item['definition'] = values[k]['value'];
                  
                  //get id corresponding to def
                  for( var i in this.options ){
                    option_item = this.options[i];
                    if( item['definition'] == option_item['definition'] ){
                      item['id'] = option_item['id'];
                      item['label'] = option_item['label']
                      this.value.push({
                        'id': item['id'],
                        'label': item['label'],
                        'definition': item['definition']
                      });
                      break;
                    }
                  }
                }
              }
            }
            else{
              console.log("loading new onderwijsniveaus from (lom_onderwijsniveau)...");
              for(var o in onderwijsniveaus){
                item['id'] = onderwijsniveaus[o]['value'];
                //get label and definition
                for(var j in this.options ){
                  option_item = this.options[j];
                  if( item['id'] == option_item['id'] ){
                    item['label'] = option_item['label'];
                    item['definition'] = option_item['definition'];
                    this.value.push({
                      'id': item['id'],
                      'label': item['label'],
                      'definition': item['definition']
                    });
                    break;
                  }
                }
              }
            }

            this.json_value = JSON.stringify(this.value)
            this.$root.$emit('niveaus_changed', this.value);
          }
        });
    },

    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
        this.$root.$emit('niveaus_changed', value);
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #onderwijsniveaus_selector{
    min-width: 30em;
  }

  #onderwijsniveaus_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
  }

  .niveau-inline-title{
    font-weight: bold;
    margin-bottom: 5px;
    color: #363636;
  }

  .inline-niveau-list{
    /*
    max-height: 150px;
    overflow-y: scroll;
    */
  }

  .niveau-pill{
    border-radius: 5px;
    border: 1px solid #9cafbd;
    background-color: #edeff2;
    color: #2b414f;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 10px;
    padding: 1px 8px 1px 8px;
    margin-bottom: 5px;
    /* cursor: pointer; */
  }

  .inline-niveau-wrapper {
    margin-top: -8px;
    margin-bottom: 12px;
  }

</style>
