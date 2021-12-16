<template>
  <div class="container main pl-5 pr-5">
    <div id="app">
      <TalenSelector/>
      <ThemaSelector/>
      <VakkenSelector/>
      <Todo/>
    </div>
  </div>
</template>

<script>
import Todo from './components/Todo.vue'
import TalenSelector from './components/TalenSelector.vue'
import ThemaSelector from './components/ThemaSelector.vue'
import VakkenSelector from './components/VakkenSelector.vue'

export default {
  name: 'App',
  components: {
    TalenSelector,
    ThemaSelector,
    VakkenSelector,
    Todo
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
