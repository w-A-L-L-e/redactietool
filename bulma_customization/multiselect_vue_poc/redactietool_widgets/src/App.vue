<template>
    <div id="app">

      <LomSection/>

      <p>
        Further docs for styling other custom selectors here:
        <a href="https://vue-multiselect.js.org/#sub-tagging" target="_blank">Vue-multiselect docs</a>
      </p>
      <Todo/>
      <br/>
    </div>
</template>

<script>
import Todo from './components/Todo.vue'
import LomSection from './components/LomSection.vue'

export default {
  name: 'App',
  components: {
    LomSection,
    Todo
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
