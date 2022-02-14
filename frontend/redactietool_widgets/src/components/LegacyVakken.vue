<template>
  <div id="legacy_vakken" v-if="legacy_vakken.length>0">

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label"></label>
      </div>
      <div class="field-body">
        <div class="legacy-vakken-list">
          <div class="legacy-title">Legacy vakken</div>
          <div 
            class="legacy-vak-pill is-pulled-left" 
            v-for="vak, index in legacy_vakken" 
            :key="index"
            >
            {{vak.value}}
          </div>
          <div class="is-clearfix"></div>
        </div>
      </div>
    </div>

  </div>
</template>

 
<script>
  export default {
    name: 'LegacyVakken',
    components: {
    },
    props: {
      metadata: Object
    },
    data () {
      return {
        legacy_vakken: [],
        vakken_suggesties:[],
        overige_vakken:[],
        graden: [],
        themas: [],
        vakken_search: "",
        vakken_prev_search: "",
        show_definitions: false,
      }
    },
    created: function() { 
      if(this.metadata.item_vakken_legacy){
        this.legacy_vakken = this.metadata.item_vakken_legacy;
      }
    },
    methods: {
     
    },
    filters: {
      truncate: function (text, length, suffix) {
        if (text.length > length) {
          return text.substring(0, length) + suffix;
        } 
        else{
          return text;
        }
      },
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #legacy_vakken{
    margin-top: -14px;
  }
  .legacy-title{
    font-weight: bold;
    margin-bottom: 5px;
    color: #363636;
  }
  .inline-suggesties{
    margin-left: 5px;
    margin-top: 5px;
  }
  .legacy-vakken-list {
    min-height: 40px;
    min-width: 478px;
    padding: 5px;
    padding-top: 7px;
    margin-bottom: 10px;
  }
  .legacy-vak-pill {
    border-radius: 5px;
    border: 1px solid #9cafbd;
    background-color: #edeff2;
    color: #2b414f;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 8px;
    padding: 0px 8px 0px 8px;
    margin-bottom: 5px;
  }
  
</style>
