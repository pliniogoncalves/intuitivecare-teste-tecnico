<template>
    <div id="app">
      <h1>Busca de Operadoras da ANS</h1>
      <SearchComponent />
    </div>
  </template>
  
  <script>
  import SearchComponent from './components/Search.vue'
  
  export default {
    name: 'App',
    components: {
      SearchComponent
    }
  }
  </script>
  
  <style>
  #app {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 20px auto;
  }
  </style>