<template>
  <div id="onderwijsgraden_selector"> 
    <multiselect v-model="value" 
      placeholder="Selecteer onderwijsgraden" 
      label="label" 
      track-by="id" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">

       
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
          var value_div = document.getElementById("item_onderwijsgraden");
          if(value_div){
            var values = JSON.parse(value_div.innerText);
            for(var k in values){
              var definition = values[k]['value'];
              
              //get id corresponding to def
              var item_id = "";
              var item_label = "";
              for( var i in this.options ){
                var item = this.options[i];
                if( item['definition'] == definition ){
                  item_id = item['id'];
                  item_label = item['label'];
                  break;
                }
              }
              default_value.push(
                {
                  'id': item_id,
                  'label': item_label,
                  'definition': definition
                }
              );
            }
          }
          this.json_value = JSON.stringify(default_value);
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
