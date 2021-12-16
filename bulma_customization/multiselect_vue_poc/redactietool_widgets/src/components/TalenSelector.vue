<template>
  <div>
    <h1 class="title">Talen selector</h1> 
    <p>
      Further docs for styling other custom selectors here:
      <a href="https://vue-multiselect.js.org/#sub-tagging" target="_blank">Vue-multiselect docs</a>
    </p>
    <multiselect v-model="value" 
      tag-placeholder="Add this as new tag" 
      placeholder="Search or add a tag" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="false" @input="updateValue">
    </multiselect>
    <textarea name="talen" v-model="json_value" id="talen_json_value"></textarea>
    <pre class="language-json" id="talen_value_preview"><code>{{ value  }}</code></pre>
    <br/>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  // register globally
  // Vue.component('multiselect', Multiselect)
  // Setting taggable to 'true' allows adding new tags above!
  // TODO: for the languages we can set this to false again, but for themas we'll need this...

  // example: initial languages to show on loading metadata item
  var default_value = [{ name: 'Nederlands', code: 'nl' }, { name: 'Frans', code: 'fr' } ]  

  export default {
    name: 'TalenSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [ //other languages, searchable 
          { name: 'Nederlands', code: 'nl' },
          { name: 'Frans', code: 'fr' },
          { name: 'Duits', code: 'de' },
          { name: 'Italiaans', code: 'it' },
          { name: 'Engels', code: 'en' },
          { name: 'Spaans', code: 'sp' },

          //todo convert other optionslist in app/templates/components/language_select.html 
        ]
      }
    },
    methods: {
      addTag (newTag) {
        const tag = {
          name: newTag,
          code: newTag.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(tag)
        this.value.push(tag)
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
  /* customize your styles */
  #talen_json_value{
    display: flex;
    width: 80%;
    height: 100px;
    /*display: none;*/
  }
  #talen_value_preview{
    display: none;
  }

</style>
