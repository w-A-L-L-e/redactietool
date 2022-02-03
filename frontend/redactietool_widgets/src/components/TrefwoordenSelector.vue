<template>
  <div id="trefwoorden_selector">
    <multiselect v-model="value" 
      tag-placeholder="Maak nieuw trefwoord aan" 
      select-label="Selecteer trefwoord"
      deselect-label="Verwijder trefwoord"
      selected-label=""
      :show-labels="false"
      :hide-selected="true"
      placeholder="Voeg nieuw trefwoord toe" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addTrefwoord" @input="updateValue">

      <template slot="noOptions">
        &nbsp;
      </template>
    </multiselect>
    <textarea name="trefwoorden" v-model="json_value" id="trefwoorden_json_value"></textarea>

    <div v-if="cp_keywords.length">
      <div class="cp_keywords_button">
        <a class="" v-on:click="toggleKeywordCollapse">
          {{cp_keyword_label}}
        </a>
        <div class="warning-pill" v-bind:class="[show_already_added_warning ? 'show' : 'hide']">
          Keyword werd al toegevoegd
        </div>
      </div>

      <div class="cp_keywords" v-bind:class="[show_cp_keywords ? 'show' : 'hide']">

        <div v-if="!cp_keywords.length" class="notification is-info is-light">
          Voor dit item zijn er geen Content Partner trefwoorden.
        </div>

        <!-- 
          v-on:click="addCpKeyword(keyword)"
        -->
        <div 
          class="keyword-pill" 
          v-for="keyword in cp_keywords" 
          :key="keyword.code"
          >
          {{keyword.name}}
        </div>
      </div>
    </div>

</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

  var default_value = [];
  export default {
    name: 'TrefwoordenSelector',
    components: {
      Multiselect 
    },
    props: {},
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          // { name: 'reportage', code: 'reportage' },
          // should be coming from the suggest library or eleastic search in next
          // release
        ],
        cp_keywords: [],
        show_cp_keywords: true,
        show_already_added_warning: false,
        cp_keyword_label: "Verberg trefwoorden van Content Partners"
      }
    },
    created(){
      var keyword_div = document.getElementById("item_keywords");
      if(keyword_div){
        var keywords = JSON.parse(keyword_div.innerText);
        this.value = [];
        for(var k in keywords){
          var keyword = keywords[k]
          this.value.push(
            {
              'name': keyword['value'],
              'code': keyword['value']
            }
          );
        }
        this.json_value = JSON.stringify(this.value);
      }

      var keywords_cp_div = document.getElementById("item_keywords_cp");
      if( keywords_cp_div ){
        var keywords_cp = JSON.parse(keywords_cp_div.innerText);
        this.cp_keywords = [];
        for(var cpk in keywords_cp){
          var cp_keyword = keywords_cp[cpk]
          this.cp_keywords.push(
            {
              'name': cp_keyword['value'],
              'code': cp_keyword['value']
            }
          );
        }
      }
    },
    methods: {
      addTrefwoord(new_keyword) {
        // instead this should call some suggest lib or other
        // api to create a new keyword (and show a modal with ok/cancel)
        console.log("addTrefwoord nieuw woord=", new_keyword);
        const tw = {
          name: new_keyword,
          code: new_keyword.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(tw)
        this.value.push(tw)
        this.json_value = JSON.stringify(this.value)
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
      },
      toggleKeywordCollapse: function(){
        this.show_cp_keywords= !this.show_cp_keywords;
        if(this.show_cp_keywords){
          this.cp_keyword_label = "Verberg trefwoorden van Content Partners";
        }
        else{
          this.cp_keyword_label = "Bekijk trefwoorden van Content Partners";
        }
      },
      addCpKeyword: function(kw){
        var already_added = false;

        for( var o in this.value){
          var okw = this.value[o];
          if(okw.code == kw.code){
            already_added = true;
            break;
          } 
        }

        if(!already_added){
          const tw = {
            name: kw.name,
            code: kw.code
          };
          this.options.push(tw);
          this.value.push(tw);
          this.json_value = JSON.stringify(this.value);
        }
        else{
          this.show_already_added_warning = true;
          setTimeout(()=>{
            this.show_already_added_warning = false;
          }, 3000);
        }
      }
    }
  }
</script>

<!-- New step!
     Add Multiselect CSS. Can be added as a static asset or inside a component. -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #trefwoorden_selector{
    min-width: 30em;
  }
  #trefwoorden_json_value{
    margin-top: 20px;
    margin-bottom: 20px;
    display: flex;
    width: 80%;
    height: 100px;
    display: none;
  }
  .cp_keywords_button {
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .keyword-pill{
    border-radius: 5px;
    border: 1px solid #9cafbd;
    background-color: #edeff2;
    color: #2b414f;
    text-overflow: ellipsis;
    position: relative;
    display: inline-block;
    margin-right: 10px;
    padding: 1px 8px 1px 8px;
    margin-bottom: 5px;
    /* cursor: pointer; */
  }
  .warning-pill{
    border-radius: 5px;
    background: #ff6a6a;
    color: #eee;
    display: inline-block;
    float: right;
    text-overflow: ellipsis;
    padding: 2px 8px 2px 13px;
    margin-bottom: 5px;
    width: 15em;
  }
  .hide{
    display: none;
  }
  .show{
    display: block;
  }
</style>
