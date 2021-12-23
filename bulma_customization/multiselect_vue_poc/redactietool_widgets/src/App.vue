<template>
    <div id="app">

      <LomSectionOne/>
      <LomSectionTwo/>
      <LomSectionThree/>

      <!--
      <p>
        Further docs for styling other custom selectors here:
        <a href="https://vue-multiselect.js.org/#sub-tagging" target="_blank">Vue-multiselect docs</a>
      </p>
      <Todo/>
      -->
    </div>
</template>

<script>
//import Todo from './components/Todo.vue'
import LomSectionOne from './components/LomSectionOne.vue'
import LomSectionTwo from './components/LomSectionTwo.vue'
import LomSectionThree from './components/LomSectionThree.vue'

export default {
  name: 'App',
  components: {
    LomSectionOne,
    LomSectionTwo,
    LomSectionThree,
    //Todo
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
