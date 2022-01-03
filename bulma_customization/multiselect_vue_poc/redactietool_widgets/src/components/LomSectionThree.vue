<template>
  <div class="lom3_section_wrapper">

    <div id="lom3_section_block" v-bind:class="{minimized: isMinimized}">
      
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Trefwoorden</label>
        </div>
        <div class="field-body">
          <TrefwoordenSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label"></label>
        </div>
        <div class="field-body">
            <a target="_blank" href="http://link_trefwoorden_content_partners?">
              Bekijk trefwoorden van Content Partners
            </a>
        </div>
      </div>

    </div> <!-- lom2_section_block -->

  </div>
</template>

<script>
  import TrefwoordenSelector from './TrefwoordenSelector.vue'

  export default {
    name: 'LomSectionThree',
    components: {
      TrefwoordenSelector
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
  .lom3_section_wrapper {
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
