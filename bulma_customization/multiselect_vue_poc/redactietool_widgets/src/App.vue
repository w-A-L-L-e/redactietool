<template>
  <div class="container main pl-5 pr-5">
    <div id="app">
      <TalenSelector/>
      <Todo/>
    </div>
  </div>
</template>

<script>
import Todo from './components/Todo.vue'
import TalenSelector from './components/TalenSelector.vue'

export default {
  name: 'App',
  components: {
    Todo,
    TalenSelector
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
