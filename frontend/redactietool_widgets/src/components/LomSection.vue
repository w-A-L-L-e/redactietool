<template>
  <div class="lom1_section_wrapper">

      <h2 class="title is-clickable" v-on:click="toggleCollapse">
        Leerobject
        <CollapseIcon v-bind:minimized="isMinimized"/>
      </h2>
      <hr>

    <div id="lom1_section_block" v-bind:class="{minimized: isMinimized}">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Type</label>
        </div>
        <div class="field-body">
          <TypeSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label label-two-lines">Beoogde eindgebruiker</label>
        </div>
        <div class="field-body">
          <EindgebruikerSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Taal</label>
        </div>
        <div class="field-body">
          <TalenSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Onderwijsniveaus</label>
        </div>
        <div class="field-body">
          <OnderwijsniveausSelector/> 
        </div>
      </div>
 
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Onderwijsgraden</label>
        </div>
        <div class="field-body">
          <OnderwijsgradenSelector/> 
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Thema</label>
        </div>
        <div class="field-body">
          <ThemaSelector/>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Vakken</label>
        </div>
        <div class="field-body">
          <VakkenSelector/>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Trefwoorden</label>
        </div>
        <div class="field-body">
          <TrefwoordenSelector/>
        </div>
      </div>

    </div> <!-- lom1_section_block -->

  </div>
</template>

<script>
  import TypeSelector from './TypeSelector.vue'
  import EindgebruikerSelector from './EindgebruikerSelector.vue'
  import TalenSelector from './TalenSelector.vue'
  import OnderwijsniveausSelector from './OnderwijsniveausSelector.vue'
  import OnderwijsgradenSelector from './OnderwijsgradenSelector.vue'
  import ThemaSelector from './ThemaSelector.vue'
  import VakkenSelector from './VakkenSelector.vue'
  import TrefwoordenSelector from './TrefwoordenSelector.vue'
  import CollapseIcon from './CollapseIcon.vue'

  var pid_div = document.getElementById("pid");
  if(pid_div){
    var pid = pid_div.innerText;
    console.log("LomSection for pid=", pid );
  }

  export default {
    name: 'LomSection',
    components: {
      TypeSelector,
      EindgebruikerSelector,
      TalenSelector,
      OnderwijsniveausSelector,
      OnderwijsgradenSelector,
      ThemaSelector,
      VakkenSelector,
      TrefwoordenSelector,
      CollapseIcon
    },
    data () {
      return {
        isMinimized: false,
        pid: pid
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
  .lom1_section_wrapper {
    margin-top: 60px;
    margin-bottom: 30px;
  }
  .label-two-lines {
    line-height: 17px;
  }

  hr {
    border-bottom: 1px solid #363636;
    margin-top: -20px;
  }

  .minimized {
    display: none;
  }
</style>
