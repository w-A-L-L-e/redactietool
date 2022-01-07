<template>
  <div id="eindgebruikers_selector"> 
    <multiselect v-model="value" 
      placeholder="Kies eindgebruikers" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="lom1_beoogde_eindgebruiker" v-model="json_value" id="eindgebruikers_json_value"></textarea>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  // todo: load in this from mam or jinja view and what is the mapping?
  var default_value = []  

  export default {
    name: 'EindgebruikerSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { name: "Docent", code: "Docent" },
          { name: "Student",code: "Student" },
          { name: "Directie",code: "Directie" },
          { name: "ICT-coördinator",code: "ICT-coördinator" },
          { name: "Systeembeheerder",code: "Systeembeheerder" },
          { name: "Preventieadviseur",code: "Preventieadviseur" },
          { name: "GOK",code: "GOK / Zorgcoördinator" },
          { name: "Pedagogisch begeleider",code: "Pedagogisch begeleider" },
          { name: "Inspectielid",code: "Inspectielid" },
          { name: "Administratief personeel",code: "Administratief personeel" },
          { name: "Met pensioen",code: "Met pensioen" },
          { name: "Ouder",code: "Ouder" },
          { name: "Ander",code: "Ander" },
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
  #eindgebruikers_selector{
    min-width: 30em;
  }

  #eindgebruikers_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
