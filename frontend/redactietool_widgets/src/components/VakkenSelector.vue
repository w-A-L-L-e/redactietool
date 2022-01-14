<template>
  <div id="vakken_selector">
    <multiselect v-model="value" 
      tag-placeholder="Kies vakken" 
      placeholder="Zoek of voeg een nieuw vak toe" 
      label="definition" 
      track-by="id" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addVak" @input="updateValue">
    </multiselect>
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
            id: "", 
            label: "Vakken inladen...", 
            definition: "Vakken inladen..."
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
        .get(redactie_api_url+'/vakken')
        .then(res => {
          this.options = res.data;
        })
    },
    methods: {
      addVak(newVak) {
        var newVakDefinition = newVak; //TODO: also allow adding definition 
        // TODO: ID needs to be computed somehow, or returned from an add call!

        const vak = {
          label: newVak,
          definition: newVakDefinition,
          id: newVak.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(vak)
        this.value.push(vak)
        this.json_value = JSON.stringify(this.value)
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
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
</style>
