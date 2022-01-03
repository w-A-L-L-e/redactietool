<template>
  <div class="lom2_section_wrapper">

    <div id="lom2_section_block" v-bind:class="{minimized: isMinimized}">
      
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Vakken</label>
        </div>
        <div class="field-body">
          <VakkenSelector/>
        </div>
      </div>

    </div> <!-- lom2_section_block -->

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
  .lom2_section_wrapper {
    margin-top: -50px;
    margin-bottom: 70px;
  }

  hr {
    border-bottom: 1px solid #363636;
    margin-top: -20px;
  }

  .minimized {
    display: none;
  } 
</style>
