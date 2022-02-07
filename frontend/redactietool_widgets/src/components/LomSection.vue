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

      <OnderwijsSelector v-bind:comboEdit="onderwijsCombo"/>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Thema's</label>
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
      
      <LegacyVakken/>


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
  import OnderwijsSelector from './OnderwijsSelector.vue'
  import ThemaSelector from './ThemaSelector.vue'
  import VakkenSelector from './VakkenSelector.vue'
  import LegacyVakken from './LegacyVakken.vue'
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
      OnderwijsSelector,
      ThemaSelector,
      VakkenSelector,
      LegacyVakken,
      TrefwoordenSelector,
      CollapseIcon
    },
    data () {
      return {
        isMinimized: false,
        onderwijsCombo: true, //set to false 2 seperate multi-selects for graden and niveaus
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

  /* change colors for multiselect pills and highlights to match redactietool colors */
  .multiselect__tag{
    /* background: #3e8ed0; dark blue like buttons */
    background-color: #eff5fb;
    color: #296fa8;
  }

  .multiselect__tag-icon:hover {
    background: #3488ce;
  }
  
  .multiselect__option--highlight {
    background-color: #eff5fb;
    color: #296fa8;
  }
  .multiselect__option--highlight:after{
    background: #3e8ed0;
  }
  
  .multiselect__option--selected.multiselect__option--highlight{
    background-color: #eff5fb;
  }

  .multiselect__option .multiselect__option--highlight .multiselect__option--selected{
    color: #222; 
  }

  .multiselect__option--selected.multiselect__option--highlight{
    color: #222; 
  }
  .multiselect__spinner:after, .multiselect__spinner:before {
    border-top-color: #3e8ed0;
  }
  
</style>
