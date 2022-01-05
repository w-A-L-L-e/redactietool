<template>
    <div id="app">
      <LomSection/>
    </div>
</template>

<script>
//import Todo from './components/Todo.vue'
import LomSection from './components/LomSection.vue'

export default {
  name: 'App',
  components: {
    LomSection,
    // Todo
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
