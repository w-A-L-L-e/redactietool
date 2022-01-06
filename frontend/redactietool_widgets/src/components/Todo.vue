<template>
  <div class="container mt-5 pt-5">
    <h1 class="title">Todo List</h1>
    <p class="mb-5">
    Example with axios to show how to make vue style ajax json calls
    A similar approach we will be using soon to fetch our Thema's and Vakken using the
    suggest library from Miel</p>
    <table class="table is-bordered is-full-width">
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
