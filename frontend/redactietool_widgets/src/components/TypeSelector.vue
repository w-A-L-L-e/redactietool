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
      :allow-empty="false"
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
    props: {
      metadata: Object
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
      if(this.metadata.item_type){
        var item_type = this.metadata.item_type;
        this.value = [{name: item_type, code: item_type}];
        this.json_value = JSON.stringify(this.value);
      }
      
    },

    methods: {
      updateValue(value){ 
        this.json_value = JSON.stringify([value])
        this.$root.$emit("metadata_edited", "true");
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  
  #lom_type_selector{
    min-width: 20em;
  }

  #lom_type_json_value{
    display: none;
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }

</style>
