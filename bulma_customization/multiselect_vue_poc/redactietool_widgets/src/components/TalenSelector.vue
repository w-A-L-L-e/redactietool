<template>
  <div>
    <h1 class="title">Multi select talen voorbeeld</h1> 
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
      :taggable="true" @tag="addTag">
    </multiselect>
    <pre class="language-json"><code>{{ value  }}</code></pre>
</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  // register globally
  // Vue.component('multiselect', Multiselect)
  // Setting taggable to 'true' allows adding new tags above!
  // TODO: for the languages we can set this to false again, but for themas we'll need this...

  export default {
    name: 'TalenSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: [
          { name: 'Nederlands', code: 'nl' } // initial languages to show on loading metadata item
        ],
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
      }
    }
  }
</script>

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  /* customize your styles */
</style>
