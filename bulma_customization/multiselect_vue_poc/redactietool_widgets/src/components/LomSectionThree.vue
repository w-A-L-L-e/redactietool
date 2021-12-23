<template>
  <div class="lom3_section_wrapper">

      <!-- now that I'm implementing this, why o why do we even need trap 1, 2, 3 and can't
      it just be one 'Leerobject metadata section'  which contains all the elements
      Type, beoogde eindgebruiker, tall, onderwijsniveaus, onderwijsgraden, themas, 
      vakken and trefwoorden ???
      -->

      <h2 class="title is-clickable" v-on:click="toggleCollapse">
        Leerobject metadata trap 3 
        <div class="minimize-icon-wrapper" id="lom1_section_icon">
          <!-- TODO fix icons
          <span class="icon-unfolded">
            <ion-icon name="chevron-down-circle-outline" 
            role="img" class="md hydrated" aria-label="chevron down circle outline"></ion-icon>
          </span>
          <span class="icon-folded">
            <ion-icon name="chevron-forward-circle-outline" 
            role="img" class="md hydrated" aria-label="chevron forward circle outline"></ion-icon>
          </span>
          -->
        </div>
      </h2>
      <hr>

    <div id="lom3_section_block" v-bind:class="{minimized: isMinimized}">
      
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Trefwoorden</label>
        </div>
        <div class="field-body">
          <TrefwoordenSelector/>
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
      TrefwoordenSelector,
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
