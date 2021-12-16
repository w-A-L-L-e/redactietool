<template>
  <div class="container">
    <h3>Todo List with ajax to warm up my vue skills ;)</h3>
    <table class="table">
      <thead>
        <tr>
          <th scope="col">Id</th>
          <th scope="col">Todo</th>
          <th scope="col">completed</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="todo in todos" v-bind:key="todo.id"> 
          <th scope="row">{{todo.id}}</th>
          <td>{{todo.title}}</td>
          <td>{{todo.completed}}</td>
        </tr>
      </tbody>
    </table> 
  </div>
</template>
<script>
  import axios from 'axios'; //example of call to flask-app

  export default {
    name: 'Todo',
    //https://jsonplaceholder.typicode.com/todos

    data() {
      return {
        todos: null,
      };
    },
    created: function() {
      axios
        .get('https://jsonplaceholder.typicode.com/todos')
        .then(res => {
          this.todos = res.data;
        })
    }
  }
</script>
<style>
  h3 {
    margin-bottom: 5%;
  }
</style>
