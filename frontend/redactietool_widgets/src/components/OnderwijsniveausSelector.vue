<template>
  <div 
    v-bind:class="[(!value.length) ? 'niveaus-pull-up' : '']"
    class="field is-horizontal"
  >
    <div class="field-label is-normal">
      <label class="label" v-if="!comboEdit">Onderwijsniveaus</label>
      <label 
        class="label" v-if="comboEdit"></label>
    </div>
    <div 
      class="field-body"
      >
      <div id="onderwijsniveaus_selector" class=""> 
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
              class="niveau-pill is-pulled-left" 
              v-for="niveau in value" 
              :key="niveau.id"
              >
              {{niveau.label}}
            </div>
            <div class="is-clearfix"></div> 
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

  var default_value = []  

  export default {
    name: 'OnderwijsniveausSelector',
    components: {
      Multiselect 
    },
    props: {
      comboEdit: Boolean,
      metadata: Object
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
          if(this.metadata.item_onderwijsniveaus){
            var onderwijsniveaus = this.metadata.item_onderwijsniveaus;
            var item = {};
            var option_item = {};

            // do fallback, in case only old string values are present
            if( onderwijsniveaus['show_legacy'] ){
              console.log("legacy fallback voor onderwijsniveaus (lom_context)...");
              if(this.metadata.item_onderwijsniveaus_legacy){
                var values = this.metadata.item_onderwijsniveaus_legacy;
                for(var k in values){
                  item['definition'] = values[k]['value'];
                  
                  //get id corresponding to def
                  for( var i in this.options ){
                    option_item = this.options[i];
                    if( item['definition'] == option_item['definition'] ){
                      this.value.push({
                        'id': option_item['id'],
                        'label': option_item['label'],
                        'definition': option_item['definition'],
                        'collection': option_item['collection'],
                        'child_count': option_item['child_count'],
                        'parent_id': option_item['parent_id']
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
                    this.value.push({
                      'id': option_item['id'],
                      'label': option_item['label'],
                      'definition': option_item['definition'],
                      'collection': option_item['collection'],
                      'child_count': option_item['child_count'],
                      'parent_id': option_item['parent_id']
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
        this.$root.$emit("metadata_edited", "true");
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
    overflow-y: auto;
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
    margin-right: 8px;
    padding: 0px 8px 0px 8px;
    margin-bottom: 5px;
  }

  .inline-niveau-wrapper {
    margin-top: -8px;
    margin-bottom: 0px;
  }

  @media screen and (min-width: 769px){
    .niveaus-pull-up {
      margin-bottom: -22px !important;
    }
  }

</style>
