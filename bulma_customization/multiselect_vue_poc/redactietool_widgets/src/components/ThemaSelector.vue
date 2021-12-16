<template>
  <div>
    <h1 class="title">Thema selector</h1> 
    <multiselect v-model="value" 
      tag-placeholder="Add this as new tag" 
      placeholder="Search or add a tag" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addThema" @input="updateValue">
    </multiselect>
    <textarea name="themas" v-model="json_value" id="thema_json_value"></textarea>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  var default_value = []; 

  export default {
    name: 'ThemaSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { name: 'Thema 1', code: 'thema1' },
          { name: 'Thema 2', code: 'thema2' },
          { name: 'Thema 3', code: 'thema3' },
          { name: 'Thema 4', code: 'thema4' },
          { name: 'Thema 5', code: 'thema5' },
          { name: 'Thema 6', code: 'thema6' },
          // TODO: get this with suggest library...
        ]
      }
    },
    methods: {
      addThema(newThema) {
        const thema = {
          name: newThema,
          code: newThema.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(thema)
        this.value.push(thema)
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
  #thema_json_value{
    display: flex;
    width: 80%;
    height: 100px;
    /*display: none;*/
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
