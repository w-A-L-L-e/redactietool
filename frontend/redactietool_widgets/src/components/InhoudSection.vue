<template>
  <div class="inhoud_section_wrapper">
    <div id="inhoud_section_block" v-bind:class="{minimized: isMinimized}">
      <p>
        Possible future work. Also pull in inhoud textareas here (hidden when empty)
        for now the jinja version works fine...
      </p>
    </div> 
  </div>
</template>

<script>
  import VakkenSelector from './VakkenSelector.vue'

  export default {
    name: 'LomSectionTwo',
    components: {
      VakkenSelector
    },
    data () {
      return {
        isMinimized: false
      }
    },
    methods: {
      toggleCollapse: function(){
        this.isMinimized = !this.isMinimized;
      }
    }
  }
</script>


<style>
  .inhoud_section_wrapper {
    margin-top: -50px;
    margin-bottom: 70px;
  }

</style>
