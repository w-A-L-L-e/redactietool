<template>
  <div id="vakken_selector">
    <multiselect v-model="value" 
      tag-placeholder="Kies vakken" 
      placeholder="Zoek of voeg een nieuw vak toe" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addVak" @input="updateValue">
    </multiselect>
    <textarea name="vakken" v-model="json_value" id="vakken_json_value"></textarea>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

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
          { name: 'Vak 1', code: 'vak1' },
          { name: 'Vak 2', code: 'vak2' },
          { name: 'Vak 3', code: 'vak3' },
          { name: 'Vak 4', code: 'vak4' },
          { name: 'Vak 5', code: 'vak5' },
          { name: 'Vak 6', code: 'vak6' },
          // TODO: get this with suggest library + axios...
          // or use the flask view/hidden field trick used for pid
          // which is actually better&faster because it avoids an extra request
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
