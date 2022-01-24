<template>
  <div id="lom_type_selector"> 
    <multiselect v-model="value" 
      placeholder="Kies media type" 
      label="name" 
      track-by="code" 
      :options="options"
      :multiple="false" 
      :taggable="false" 
      :searchable="false"
      :show-labels="false"
      @input="updateValue">

      <template slot="noResult">Media type niet gevonden</template>

    </multiselect>
    <textarea name="lom_type" v-model="json_value" id="lom_type_json_value"></textarea>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  var default_value = [{ name: 'Video', code: 'Video' }];

  export default {
    name: 'TypeSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { name: 'Video', code: 'Video' },
          { name: 'Audio', code: 'Audio' },
        ]
      }
    },
    created(){
      var item_type_div = document.getElementById("item_type");
      if(item_type_div){
        var item_type = item_type_div.innerText;
        if(item_type){
          default_value = [{name: item_type, code: item_type}];
          this.value = default_value;
        }

        this.json_value = JSON.stringify(default_value);
      }
      
    },

    methods: {
      updateValue(value){
        this.json_value = JSON.stringify([value])
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  
  #lom_type_selector{
    min-width: 30em;
  }

  #lom_type_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }

</style>
