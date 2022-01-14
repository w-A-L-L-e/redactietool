<template>
  <div id="onderwijsniveaus_selector"> 
    <multiselect v-model="value" 
      placeholder="Selecteer onderwijsniveaus" 
      label="label" 
      track-by="id" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="lom1_beoogde_eindgebruiker" v-model="json_value" id="onderwijsniveaus_json_value"></textarea>
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
    created: function() { 
      // smart way to use mocked data during development
      // after deploy in flask this uses a different url on deployed pod
      var redactie_api_url = 'http://localhost:5000';
      var redactie_api_div = document.getElementById('redactie_api_url');
      if( redactie_api_div ){
        redactie_api_url = redactie_api_div.innerText;
      }
      axios
        .get(redactie_api_url+'/onderwijsniveaus')
        .then(res => {
          this.options = res.data;
        })
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
  #onderwijsniveaus_selector{
    min-width: 30em;
  }

  #onderwijsniveaus_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
