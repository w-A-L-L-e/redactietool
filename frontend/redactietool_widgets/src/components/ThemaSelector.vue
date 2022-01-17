<template>
  <div id="thema_selector">

  <multiselect v-model="value" 
    tag-placeholder="Voeg nieuw thema toe" 
    placeholder="Zoek thema" 
    label="label" 
    track-by="id" 
    :options="options" 
    :option-height="104" 
    :show-labels="false"
    :multiple="true"
    :taggable="false" @input="updateValue"
  >

    <template slot="noResult">Thema niet gevonden</template>

    <template 
      slot="singleLabel" 
      slot-scope="props">
        <span class="option__desc">
          <span class="option__title">
            {{ props.option.label}}
          </span>
          <span class="option_small">
            {{props.option.definition}}
          </span>
        </span>
    </template>

    <template 
      slot="option" 
      slot-scope="props">
        <div class="option__desc">
          <span class="option__title">{{ props.option.label}}</span>
          <span class="option__small">{{ props.option.definition}}</span>
        </div>
    </template>

  </multiselect>

  <a class="button is-link is-small toon-themas-button" 
      v-on:click="toggleThemas" 
    >
      {{show_themas_label}}
  </a>
  <div class="thema-warning-pill" v-bind:class="[show_already_added_warning ? 'show' : 'hide']">
    Thema werd al toegevoegd
  </div>

  <div class="thema-cards" v-bind:class="[show_thema_cards ? 'show' : 'hide']">
      <!--h3 class="subtitle">Suggesties voor vakken</h3-->
      <div class="columns"  v-for="(row, index) in thema_cards" :key="index">
        <div class="column is-one-quarter" v-for="thema in row" :key="thema.id">
          <div class="tile is-ancestor">
            <div class="tile is-vertical mr-2 mt-2" >
              <div class="card" >
                <header class="card-header">
                  <p class="card-header-title">
                    {{thema.label}}
                  </p>
                </header>
                <div class="card-content">
                    {{thema.definition}} 
                </div>
                <footer class="card-footer">
                  <a v-on:click="addThema(thema)" 
                  class="card-footer-item">Selecteer</a>
                </footer>
              </div>
            </div>
          </div>

        </div>
      </div>

  </div>


  <textarea name="themas" v-model="json_value" id="thema_json_value"></textarea>

</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'
  import axios from 'axios';

  var default_value = []; 

  export default {
    name: 'ThemaSelector',
    components: {
      Multiselect 
    },
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { 
            id: "", 
            label: "Themas inladen...", 
            definition: "Themas inladen..."
          },
        ],
        thema_cards: [],
        show_thema_cards: false,
        show_already_added_warning: false,
        show_themas_label: 'Toon themas'
      }
    },
    created: function() { 
      // smart way to use mocked data during development
      // after deploy in flask this uses a different url on deployed pod
      var redactie_api_url = 'http://localhost:5000';
      var redactie_api_div = document.getElementById('redactie_api_url');
      if( redactie_api_div ){
        redactie_api_url = redactie_api_div.innerText;
      }
      else{
        return;
      }
      axios
        .get(redactie_api_url+'/themas')
        .then(res => {
          this.options = [];
          //only add non-empty labels
          for(var o in res.data){
            var thema = res.data[o];
            if(thema.label.length>1){
              this.options.push(thema);
            }
          }
        })

      // todo fetch currently set themas here (look at Onderwijsgraden for example)
      // then also emit the currently set themas so our vakken selector can pass it to suggest:
      // this.$root.$emit('themas_changed', this.value);
    },
    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
        this.$root.$emit('themas_changed', value);
      },
      toggleThemas(){
        this.show_thema_cards = !this.show_thema_cards;
        if( this.show_thema_cards ){
          this.show_themas_label = "Verberg themas";
        }
        else{
          this.show_themas_label = "Toon themas";
          this.thema_cards = [];
        }

        this.thema_cards = [];
        var row = [];
        for( var thema_index in this.options){
          row.push(this.options[thema_index]);
          if(row.length==4){
            this.thema_cards.push(row);
            row=[];
          }
        }
        if(row.length>0){
          this.thema_cards.push(row);
        }

      },
      addThema: function(thema){
        var already_added = false;

        for(var o in this.value){
          var okw = this.value[o];
          if(okw.id == thema.id){
            already_added = true;
            break;
          } 
        }

        if(!already_added){
          const new_thema = {
            id: thema.id,
            label: thema.label,
            definition: thema.definition
          };
          this.options.push(new_thema);
          this.value.push(new_thema);
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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>
  #thema_selector{
    min-width: 30em;
  }

  #thema_json_value{
    /*display: flex;*/
    width: 80%;
    height: 100px;
    margin-top: 20px;
    margin-bottom: 20px;
    display: none;
  }

  .option__title{
    display: block;
    text-decoration: none;
    padding-bottom: 8px;
    font-style: bold;
    font-size: 1.2em;
    text-transform: none;
    vertical-align: top;
    position: relative;
    cursor: pointer;
    white-space: nowrap;
  }

  .option__small{
    display: block;
  }
  .option__desc{
    display: block;
  }
  .multiselect__option {
    display: block;
    padding: 12px;
    min-height: 40px;
    line-height: 16px;
    text-decoration: none;
    text-transform: none;
    vertical-align: middle;
    position: relative;
    cursor: pointer;
    white-space: normal;
    border-bottom: 1px solid #eee;
  }
  .toon-themas-button {
    /*position: -webkit-sticky;
    position: sticky;
    top: 20px;
    float: left;
    z-index: 100;
    */
    margin-top: 10px;
    margin-bottom: 15px;
  }

  .thema-cards {
    height: 370px;
    overflow-y: scroll;
    /* overflow-y: hidden;*/
    overflow-x: hidden;
    border: 1px solid #e8e8e8;
    padding: 5px;
    border-radius: 5px;
    width: 45em;
    padding-left: 12px;
    padding-right: 15px;
  }
  .tile {
    margin-right: -30px;
    margin-left: 0px;
  }
  
  .card-header-title {
    height: 50px;
    overflow-y: scroll;
    overflow-wrap: anywhere;
    font-size: 14px;
    padding: 4px 15px;
    text-transform: capitalize;
  }
  .card-content {
    overflow-wrap: anywhere;
    font-size: 12px;
    padding: 4px 10px;
    height: 80px;
    overflow-y: scroll;
  }
  
  .show{
    display: block;
  }
  .hide{
    display: hidden;
  }

  .thema-warning-pill{
    border-radius: 5px;
    background: #ff6a6a;
    color: #eee;
    display: inline-block;
    float: right;
    text-overflow: ellipsis;
    padding: 2px 8px 2px 13px;
    margin-bottom: 5px;
    width: 15em;
    margin-top: 10px;
  }
  .hide{
    display: none;
  }
  .show{
    display: block;
  }


</style>
