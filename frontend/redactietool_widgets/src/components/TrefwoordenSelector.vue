<template>
  <div id="trefwoorden_selector">
    <multiselect v-model="value" 
      tag-placeholder="Maak nieuw trefwoord aan" 
      placeholder="Zoek of voeg een nieuw trefwoord toe" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addTrefwoord" @input="updateValue">
    </multiselect>
    <textarea name="trefwoorden" v-model="json_value" id="trefwoorden_json_value"></textarea>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  var default_value = [];
  var keyword_div = document.getElementById("keywords");
  if(keyword_div){
    var keywords = JSON.parse(keyword_div.innerText);
    for(var k in keywords){
      var keyword = keywords[k]
      var val = {
        'name': keyword['value'],
        'code': keyword['value']
      }
      default_value.push(val);
    }
  }

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
          { name: 'reportage', code: 'reportage' },
          { name: 'Silent Movie', code: 'Silent Movie' },
          { name: 'Belgium', code: 'Belgium' },
          { name: 'France', code: 'France' },
          { name: 'Spain', code: 'Spain' },
          // TODO: populate this using a div in the flask view coming from 
          // our suggest library (aka knowledge graph).
        ]
      }
    },
    methods: {
      addTrefwoord(nieuwTrefwoord) {
        const tw = {
          name: nieuwTrefwoord,
          code: nieuwTrefwoord.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(tw)
        this.value.push(tw)
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
  #trefwoorden_selector{
    min-width: 30em;
  }
  #trefwoorden_json_value{
    margin-top: 20px;
    margin-bottom: 20px;
    display: flex;
    width: 80%;
    height: 100px;
    display: none;
  }
</style>
