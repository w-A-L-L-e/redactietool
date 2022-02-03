<template>
  <div id="eindgebruikers_selector"> 
    <multiselect v-model="value" 
      placeholder="Kies eindgebruikers" 
      label="name" 
      track-by="code" 
      :options="options"
      :multiple="true"
      :show-labels="false"
      :hide-selected="true"
      :searchable="false"
      :taggable="false"
      @input="updateValue">

      <template slot="noResult">Beoogde eindgebruiker niet gevonden</template>

    </multiselect>
    <textarea name="lom1_beoogde_eindgebruiker" v-model="json_value" id="eindgebruikers_json_value"></textarea>
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'
  var default_value = [];

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
    created(){
      var value_div = document.getElementById("item_eindgebruikers");
      if(value_div){
        var values = JSON.parse(value_div.innerText);
        this.value = [];
        for(var k in values){
          var preset_value = values[k]
          this.value.push(
            {
              'name': preset_value['value'],
              'code': preset_value['value']
            }
          );
        }
      }
      this.json_value = JSON.stringify(this.value);
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
