<template>
  <div id="legacy_vakken" v-if="legacy_vakken.length>0">

    <div class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Vakken (legacy)</label>
      </div>
      <div class="field-body">
        <div class="legacy-vakken-list">
          <div 
            class="legacy-vak-pill" 
            v-for="vak, index in legacy_vakken" 
            :key="index"
            >
            {{vak.value}}
          </div>
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
    props: {},
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
      var legacy_vakken_div = document.getElementById("item_vakken_legacy");
      if(legacy_vakken_div){
        var legacy_vakken_values = JSON.parse(legacy_vakken_div.innerText);
        console.log("legacy vakken=", legacy_vakken_values);
        this.legacy_vakken = legacy_vakken_values
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

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  .legacy-vakken-list {
    min-height: 40px;
    min-width: 478px;
    background: #fff;
    border-radius: 5px;
    border: 1px solid #e8e8e8;
    padding: 5px;
    padding-top: 7px;
    margin-bottom: 10px;
  }
  .legacy-vak-pill {
    border-radius: 5px;
    /*background: #41b883;*/
    border: 1px solid #9cafbd;
    background-color: #edeff2;
    color: #2b414f;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 10px;
    padding: 1px 8px 1px 8px;
    margin-bottom: 5px;
    cursor: pointer;
  }
</style>
