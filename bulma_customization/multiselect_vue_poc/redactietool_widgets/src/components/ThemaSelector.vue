<template>
  <div>
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
          { 
            name: 'Politiek en overheid', 
            code: 'Van politieke partijen en besluitvorming tot de werking van de overheid, wetgeving en burgerparticipatie. Zowel binnen- als buitenland' 
          },
          {
            name: 'Mediawijsheid',
            code: 'Mediawijsheid, beeldgeletterdheid, kritische zin' 
          },
          { 
            name: 'Culturele diversiteit', 
            code: 'Cultuurbeschouwing. Alles over de verscheidenheid aan culturen en culturele uitingen binnen een samenleving en het proces van wereldwijde culturele integratie (globalisering). Hier gaat het dan meer om symbolen, rituelen, ...' 
          },
          { name: 'Thema 4', code: 'Dit is de beschrijving voor thema 4' },
          { name: 'Thema 5', code: 'Dit is de beschrijving voor thema 5' },
          { name: 'Thema 6', code: 'Dit is de beschrijving voor thema 6' },
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
    /*display: flex;*/
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
    display: none;
  }
</style>
