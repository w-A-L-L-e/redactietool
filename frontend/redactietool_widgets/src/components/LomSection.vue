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
          <TypeSelector v-bind:metadata="metadata"/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label label-two-lines">Beoogde eindgebruiker</label>
        </div>
        <div class="field-body">
          <EindgebruikerSelector v-bind:metadata="metadata"/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Taal</label>
        </div>
        <div class="field-body">
          <TalenSelector v-bind:metadata="metadata"/>
        </div>
      </div>

      <OnderwijsSelector 
        v-bind:comboEdit="onderwijsCombo" 
        v-bind:metadata="metadata"
      />

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Thema's</label>
        </div>
        <div class="field-body">
          <ThemaSelector v-bind:metadata="metadata"/>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Vakken</label>
        </div>
        <div class="field-body">
          <VakkenSelector v-bind:metadata="metadata"/>
        </div>
      </div>
      
      <LegacyVakken v-bind:metadata="metadata"/>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Trefwoorden</label>
        </div>
        <div class="field-body">
          <TrefwoordenSelector v-bind:metadata="metadata"/>
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
    props: {
      metadata: Object
    },
    data () {
      return {
        isMinimized: false,
        onderwijsCombo: true, //set to false 2 seperate multi-selects for graden and niveaus
      }
    },
    created(){},
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

  /*
  hr {
    border-bottom: 1px solid #363636;
    margin-top: -17px;
  }*/

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
