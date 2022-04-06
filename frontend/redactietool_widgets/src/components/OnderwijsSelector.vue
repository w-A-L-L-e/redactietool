<template>
  <div id="onderwijs_selector">
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
            :blockKeys="['Delete']"
            :searchable="false"
            :taggable="false"
            :loading="loading"
            @input="updateValue" @remove="removeValue" @select="addValue">

            <template slot="noResult">niet gevonden</template>
            <template slot="noOptions">loading...</template>
          </multiselect>
          <p v-if="show_vakken_warning" class="help is-danger vakken-warning">
            Opgelet: indien je deze waarde verwijdert, 
            zijn mogelijks een aantal vakken niet meer relevant &nbsp;
             <!-- button class="delete" v-on:click="closeVakkenWarning($event)"></button> -->
          </p>
          
          <!-- not necessary as we split up and populate graden+niveaus seperately,
          but keeping it as we might evolve into one field with tree structure in future-->
          <textarea name="lom_onderwijs_combo" v-model="json_value" id="onderwijs_json_value"></textarea>
        </div>

      </div>
    </div>

    <div v-bind:class="[value.length && !show_onderwijsstructuur ? 'show' : 'hide']">
      <div class="field is-horizontal">
        <div class="field-label is-normal"></div>
        <div class="field-body">
          <a v-on:click="toggleOnderwijsstructuur">Bekijk de onderwijsstructuur</a>
        </div>
      </div>
    </div>
    
    <div v-bind:class="[value.length && show_onderwijsstructuur ? 'show' : 'hide']">
      <div class="field is-horizontal">
        <div class="field-label is-normal"></div>
        <div class="field-body">
          <a v-on:click="toggleOnderwijsstructuur">Verberg de onderwijsstructuur</a>
        </div>
      </div>

      <OnderwijsniveausSelector v-bind:metadata="metadata" v-bind:comboEdit="comboEdit"/> 
      <OnderwijsgradenSelector v-bind:metadata="metadata" v-bind:comboEdit="comboEdit"/> 
    </div>
 
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
      comboEdit: Boolean,
      metadata: Object
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
        loading: true,
        show_vakken_warning: false,
        vakken_selected: [],
        show_onderwijsstructuur: false
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
        this.niveau_options = data;
        this.readOptions();
      });

      this.$root.$on('graden_options_loaded', data => {
        this.graden_options = data;
        this.readOptions();
      });

      this.$root.$on('vakken_changed', data => {
        if(data.length) {
          this.vakken_selected = data;
        }
        else{
          this.vakken_selected = [];
        }
      });

    },
    created: function() { 
      this.options = []; 
      this.value = []; 
      this.json_value = JSON.stringify(this.value)
      //this.$root.$emit('onderwijs_changed', this.value);
    },

    methods: {
      toggleOnderwijsstructuur(){
        this.show_onderwijsstructuur = !this.show_onderwijsstructuur;
      },
      isRelated(vak, selected_vak){
        if( vak['related_id'] == undefined) return false;
        for( var r in vak['related_id'] ){
          var related_id = vak['related_id'][r]
          if(related_id == selected_vak['id']){
            return true;
          }
        }
      },
      removeValue(val){
        this.show_vakken_warning = false;
        if(this.vakken_selected.length){
          for(var v in this.vakken_selected){
            var vak = this.vakken_selected[v];
            if(this.isRelated(vak, val)){
              this.show_vakken_warning = true;
              return;
            }
          }
        }
      },
      addValue(){
        this.show_vakken_warning = false;
      },
      closeVakkenWarning(ev){
        ev.preventDefault();
        this.show_vakken_warning = false;
      },
      isLeaf(val){
        return val.child_count == 0;
      },
      updateValue(values){
        //strictly this is not necessary but it's nice for debugging later:
        this.json_value = JSON.stringify(values)

        // now we keep 2 arrays of graden and niveaus
        // and emit a change event for each
        var changed_graden = [];
        var changed_niveaus = [];
        var parents = {}

        for( var v in values ){
          var val = values[v];
          if(val.type == 'niveau'){ 
            if(this.isLeaf(val)){
              changed_niveaus.push({
                'id': val.id,
                'label': val['label'],
                'definition': val['definition'],
                'collection': val['collection'],
                'child_count': val['child_count'],
                'parent_id': val['parent_id']
              })
              if(val['parent_id']) parents[val['parent_id']] = val;
            }
          }

          // graad means it always has a parent_id and is a leaf also
          if(val.type == 'graad'){
            changed_graden.push({
              'id': val.id,
              'label': val['label'],
              'definition': val['definition'],
              'child_count': val['child_count'],
              'parent_id': val['parent_id']
            })
            if(val['parent_id']) parents[val['parent_id']] = val;
          }
        }

        for( var p in parents){
          for( var n in this.niveau_options){
            var niv = this.niveau_options[n];
            if(niv.id==p){
              changed_niveaus.push(niv);
            }
          } 
        }
        
        var data = {
          'niveaus': changed_niveaus,
          'graden': changed_graden
        }

        this.$root.$emit('onderwijs_changed', data);
        this.$root.$emit("metadata_edited", "true");
      },
      readValues(){
        this.value = [];

        for(var n in this.niveaus){
          var niv = this.niveaus[n];
          if(this.isLeaf(niv)){
            this.value.push({
              'id': niv.id,
              'label': niv['label'],
              'definition': niv['definition'],
              'collection': niv['collection'],
              'child_count': niv['child_count'],
              'parent_id': niv['parent_id'],
              'type': 'niveau'
            })
          }
        }

        for(var g in this.graden){
          var grd = this.graden[g];
          this.value.push({
            'id': grd.id,
            'label': grd['label'],
            'definition': grd['definition'],
            'child_count': grd['child_count'],
            'parent_id': grd['parent_id'],
            'type': 'graad'
          })
        }
      },
      readOptions(){
        this.options = [];

        for(var n in this.niveau_options){
          var niv = this.niveau_options[n];
          if(this.isLeaf(niv)){
            this.options.push({
              'id': niv.id,
              'label': niv['label'],
              'definition': niv['definition'],
              'collection': niv['collection'],
              'child_count': niv['child_count'],
              'parent_id': niv['parent_id'],
              'type': 'niveau'
            })
          }
        }

        for(var g in this.graden_options){
          var grd = this.graden_options[g];
          this.options.push({
            'id': grd.id,
            'label': grd['label'],
            'definition': grd['definition'],
            'child_count': grd['child_count'],
            'parent_id': grd['parent_id'],
            'type': 'graad'
          })
        }

        this.loading = false;
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
    min-width: 25em;
  }

  #onderwijs_json_value{
    display: none; 
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
  }
  
  .vakken-warning{
  }
</style>
