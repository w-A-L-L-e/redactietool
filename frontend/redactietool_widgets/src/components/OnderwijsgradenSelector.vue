<template>
  <div id="onderwijsgraden_selector"> 
    <multiselect v-model="value" 
      placeholder="Selecteer onderwijsgraden" 
      label="label" 
      track-by="id" 
      :options="options"
      :multiple="true" 
      :taggable="false" 
      :searchable="false"
      @input="updateValue">
       
      <template slot="noResult">Onderwijsgraad niet gevonden</template>

    </multiselect>
    <textarea name="lom1_onderwijsgraden" v-model="json_value" id="onderwijsgraden_json_value"></textarea>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  // todo: mapping in mediahaven voor onderwijsgraden?
  var default_value = []  

  export default {
    name: 'OnderwijsgradenSelector',
    components: {
      Multiselect 
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
      axios
        .get(redactie_api_url+'/onderwijsgraden')
        .then(res => {
          // populate all possible options
          this.options = res.data;

          // set selected options for this specific item
          // do fallback, in case only old string values are present
          var value_div = document.getElementById("item_onderwijsgraden");
          if(value_div){
            var onderwijsgraden = JSON.parse(value_div.innerText);
            var item = {};
            var option_item = {};

            if(value_div && onderwijsgraden['show_legacy'] ){
              console.log("legacy fallback voor onderwijsniveaus (lom_typicalagerange)...");
              var value_div_legacy = document.getElementById("item_onderwijsgraden_legacy");
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
                      break;
                    }
                  }
                  default_value.push( item );
                }
              }
            }
            else{
              console.log("loading new onderwijsgraden from (lom_onderwijsgraad)...");
              for(var o in onderwijsgraden){
                item['id'] = onderwijsgraden[o]['value'];
                //get label and definition
                for(var j in this.options ){
                  option_item = this.options[j];
                  if( item['id'] == option_item['id'] ){
                    item['label'] = option_item['label'];
                    item['definition'] = option_item['definition'];
                    break;
                  }
                }
                default_value.push(item);
              }
            }
          }

        });
    },
    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
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
</style>
