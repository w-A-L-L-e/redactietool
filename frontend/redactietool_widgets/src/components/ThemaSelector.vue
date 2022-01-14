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
    :taggable="true" @tag="addThema" @input="updateValue"
  >
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
        ]
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
      axios
        .get(redactie_api_url+'/themas')
        .then(res => {
          this.options = res.data;
        })
    },
    methods: {
      addThema(newThema) {
        const thema = {
          label: newThema,
          definition: 'beschrijving voor nieuwe thema?',
          id: newThema.substring(0, 2) + Math.floor((Math.random() * 10000000))
        }
        this.options.push(thema)
        this.value.push(thema)
        this.json_value = JSON.stringify(this.value)
      },
      updateValue(value){
        this.json_value = JSON.stringify(value)
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
</style>
