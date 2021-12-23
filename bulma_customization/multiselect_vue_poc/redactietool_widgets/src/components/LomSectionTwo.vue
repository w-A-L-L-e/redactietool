<template>
  <div class="lom2_section_wrapper">

      <h2 class="title is-clickable" v-on:click="toggleCollapse">
        Leerobject metadata trap 2
        <CollapseIcon v-bind:minimized="isMinimized"/>
      </h2>
      <hr>

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
  import CollapseIcon from './CollapseIcon.vue'

  export default {
    name: 'LomSectionTwo',
    components: {
      VakkenSelector,
      CollapseIcon
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
    margin-top: 40px;
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
