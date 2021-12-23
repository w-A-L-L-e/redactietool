<template>
  <div id="trefwoorden_selector">
    <multiselect v-model="value" 
      tag-placeholder="Maak nieuw trefwoord aan" 
      placeholder="Zoek of voeg een nieuw trefwoord toe" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addVak" @input="updateValue">
    </multiselect>
    <textarea name="trefwoorden" v-model="json_value" id="trefwoorden_json_value"></textarea>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  //example of default value filled in voor trefwoorden in metadata:
  var default_value = [{ name: 'Trefwoord 1', code: 'trefwoord1' }]

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
          { name: 'Trefwoord 1', code: 'vak1' },
          { name: 'Trefwoord 2', code: 'vak2' },
          { name: 'Trefwoord 3', code: 'vak3' },
          { name: 'Trefwoord 4', code: 'vak4' },
          { name: 'Trefwoord 5', code: 'vak5' },
          // TODO: populate this using a div in the flask view coming from 
          // our suggest library (aka knowledge graph).
        ]
      }
    },
    methods: {
      addVak(newVak) {
        const vak = {
          name: newVak,
          code: newVak.substring(0, 2) + Math.floor((Math.random() * 10000000))
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
