<template>
  <div id="onderwijs_selector" v-bind:class="[(!comboEdit || value.length) ? '' : 'onderwijs-pull-up']">

    <div  v-if="comboEdit" class="field is-horizontal">
      <div class="field-label is-normal">
        <label class="label">Onderwijs</label>
      </div>
      <div class="field-body">

        <div id="onderwijs_selector_dropdown"> 
          <multiselect v-model="value" 
            placeholder="Selecteer opleiding" 
            label="label" 
            track-by="id" 
            :options="options"
            :multiple="true" 
            :show-labels="false"
            :hide-selected="true"
            :searchable="false"
            :taggable="false"
            @input="updateValue">

            <template slot="noResult">niet gevonden</template>
            <template slot="noOptions">loading...</template>
          </multiselect>
          
          <!-- this is actually not needed here, but nice to have for debugging -->
          <textarea name="lom_onderwijs_combo" v-model="json_value" id="onderwijs_json_value"></textarea>
        </div>

      </div>
    </div>
   
    <OnderwijsniveausSelector v-bind:comboEdit="comboEdit"/> 
    <OnderwijsgradenSelector v-bind:comboEdit="comboEdit"/> 
 
  </div>
</template>

<script>
  import Multiselect from 'vue-multiselect'
  import OnderwijsgradenSelector from './OnderwijsgradenSelector.vue'
  import OnderwijsniveausSelector from './OnderwijsniveausSelector.vue'

  var default_value = []  

  export default {
    name: 'OnderwijsSelector',
    components: {
      Multiselect,
      OnderwijsgradenSelector,
      OnderwijsniveausSelector
    },
    props: {
      comboEdit: Boolean
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { 
            id: "", 
            label: "Thesaurus data inladen...", 
            definition: "Thesaurus data inladen..."
          },
        ],
        niveaus: [],
        graden: [],
        niveau_options: [],
        graden_options: [],
        secundair_niveau: {},
        lager_niveau: {}
      }
    },
    mounted: function() {
      this.$root.$on('niveaus_changed', data => {
        this.niveaus = data;
        this.readValues();
      });

      this.$root.$on('graden_changed', data => {
        this.graden = data;
        this.readValues();
      });

      this.$root.$on('niveau_options_loaded', data => {
        // console.log('COMBO: niveaus_changed event');
        this.niveau_options = data;
        this.readOptions();
      });

      this.$root.$on('graden_options_loaded', data => {
        // console.log('graden changed event');
        this.graden_options = data;
        this.readOptions();
      });


    },
    created: function() { 
      this.options = []; 
      this.value = []; 
      this.json_value = JSON.stringify(this.value)
      //this.$root.$emit('onderwijs_changed', this.value);
    },

    methods: {
      updateValue(values){
        //strictly this is not necessary but it's nice for debugging later:
        this.json_value = JSON.stringify(values)

        // now we keep 2 arrays of graden and niveaus
        // and emit a change event for each
        var changed_graden = [];
        var changed_niveaus = [];

        // TODO: later we need suggest lib from Miel to return parent_id on graden
        // this wil make this simpler and more robust for future
        // instead we can then use an array of ids of the parent to append to niveaus.
        var secundair_used = false;
        var lager_used = false;

        for( var v in values ){
          var val = values[v];
          if(val.type == 'niveau'){
            // also here we should have the niveau.child_count from suggest lib
            // which will be there when we merge and we only add ones with count=0 here
            if(!(val.label.includes("Secundair")||val.label.includes("Lager"))){
              changed_niveaus.push({
                'id': val.id,
                'label': val.label,
                'definition': val.definition
              })
            }
          }
          if(val.type == 'graad'){
            changed_graden.push({
              'id': val.id,
              'label': val.label,
              'definition': val.definition
            })
            if(val.label.includes("Secundair")) secundair_used = true;
            if(val.label.includes("Lager")) lager_used = true;
          }
        }

        // add secundair or lager niveau in case used=true
        if( lager_used ){
          changed_niveaus.push( this.lager_niveau );
          console.log("lager=", this.lager_niveau);
        }
        if( secundair_used ){
          changed_niveaus.push( this.secundair_niveau );
        }
        
        var data = {
          'niveaus': changed_niveaus,
          'graden': changed_graden
        }

        console.log("onderwijs_changed data=", data);
        this.$root.$emit('onderwijs_changed', data);
      },
      readValues(){
        // console.log("readValues: niveaus=",this.niveaus, "graden=", this.graden);
        this.value = [];

        for(var n in this.niveaus){
          var niv = this.niveaus[n];
          if(!(niv.label.includes("Secundair")||niv.label.includes("Lager"))){
            this.value.push({
              'id': niv.id,
              'label': niv.label,
              'definition': niv.definition,
              'type': 'niveau'
            })
          }
        }

        for(var g in this.graden){
          var grd = this.graden[g];
          this.value.push({
            'id': grd.id,
            'label': grd.label,
            'definition': grd.definition,
            'type': 'graad'
          })
        }

      },
      readOptions(){
        // console.log("readOptions: niveaus=", this.niveau_options, "graden=", this.graden_options);
        this.options = [];

        for(var n in this.niveau_options){
          var niv = this.niveau_options[n];
          if( niv.label.includes("Secundair") ){
            this.secundair_niveau = JSON.parse(JSON.stringify(niv));
          }
          else if( niv.label.includes("Lager") ){
            this.lager_niveau = JSON.parse(JSON.stringify(niv));
          }
          else{
            this.options.push({
              'id': niv.id,
              'label': niv.label,
              'definition': niv.definition,
              'type': 'niveau'
            })
          }
        }

        for(var g in this.graden_options){
          var grd = this.graden_options[g];
          this.options.push({
            'id': grd.id,
            'label': grd.label,
            'definition': grd.definition,
            'type': 'graad'
          })
        }
      }
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #onderwijs_selector{
    margin-bottom: 10px;
  }

  #onderwijs_selector_dropdown{
    min-width: 30em;
  }

  #onderwijs_json_value{
    display: none; 
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  .onderwijs-pull-up{
    margin-bottom: -24px !important;
  }
</style>
