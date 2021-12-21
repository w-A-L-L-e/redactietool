<template>
    <div id="app">
      <LomSectionOne/>

      <h1 class="title">Other custom selectors</h1> 
      <p>
        Further docs for styling other custom selectors here:
        <a href="https://vue-multiselect.js.org/#sub-tagging" target="_blank">Vue-multiselect docs</a>
      </p>
      <ThemaSelector/>
      <VakkenSelector/>
      <Todo/>
    </div>
</template>

<script>
import Todo from './components/Todo.vue'
import ThemaSelector from './components/ThemaSelector.vue'
import VakkenSelector from './components/VakkenSelector.vue'
import LomSectionOne from './components/LomSectionOne.vue'

export default {
  name: 'App',
  components: {
    ThemaSelector,
    VakkenSelector,
    Todo,
    LomSectionOne
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
