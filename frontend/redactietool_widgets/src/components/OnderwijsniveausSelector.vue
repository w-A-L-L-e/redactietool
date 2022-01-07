<template>
  <div id="onderwijsniveaus_selector"> 
    <multiselect v-model="value" 
      placeholder="Selecteer onderwijsniveaus" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="lom1_beoogde_eindgebruiker" v-model="json_value" id="onderwijsniveaus_json_value"></textarea>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

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
          //todo make axios request here...
          { name: "Kleuteronderwijs", code: "Kleuteronderwijs"},
          { name: "Lager onderwijs", code: "Lager onderwijs"},
          { name: "Secundair onderwijs", code: "Secundair onderwijs"},
          { name: "Volwassenenonderwijs", code: "Volwassenenonderwijs"},
          { name: "Hoger onderwijs", code: "Hoger onderwijs"},
        ]
      }
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
