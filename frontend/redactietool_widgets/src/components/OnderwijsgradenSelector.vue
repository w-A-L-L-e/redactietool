<template>
  <div id="onderwijsgraden_selector"> 
    <multiselect v-model="value" 
      placeholder="Selecteer onderwijsgraden" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="lom1_onderwijsgraden" v-model="json_value" id="onderwijsgraden_json_value"></textarea>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  // todo: load in this from mam or jinja view and what is the mapping?
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
            // TODO: request + transform knowledge graph format:
            // {'id': 'https://data.meemoo.be/terms/ond/graad#lager-1ste-graad', 'label': 'Lager 1ste graad', 'definition': 'Lager 1ste graad'}

          { name: "Lager 1ste graad", code: "https://data.meemoo.be/terms/ond/graad#lager-1ste-graad" },
          { name: "Lager 2de graad", code: "https://data.meemoo.be/terms/ond/graad#lager-2de-graad" },
          { name: "Lager 3de graad", code: "https://data.meemoo.be/terms/ond/graad#lager-3de-graad" },
          { name: "Secundair 1ste graad", code: "https://data.meemoo.be/terms/ond/graad#secundair-1ste-graad" },
          { name: "Secundair 2de graad", code: "https://data.meemoo.be/terms/ond/graad#secundair-2de-graad" },
          { name: "Secundair 3de graad", code: "https://data.meemoo.be/terms/ond/graad#secundair-3de-graad" },
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
