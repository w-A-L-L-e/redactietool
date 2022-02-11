<template>
  <div class="columns">
    <div class="column">
      <h2 class="title">Publicatiestatus</h2>
      <hr/>
      <label class="checkbox">
        <input v-if="!loading"
               type="checkbox"
               name="publicatiestatus_checked" 
               id="publicatiestatus_checked"
               v-model="publish_item"/>
        <div class="checkbox-spinner multiselect__spinner" v-if="loading"></div>

        Dit item mag gepubliceerd worden op 
        <a target="blank" href="https://onderwijs.hetarchief.be">Het Archief voor Onderwijs.</a>

      </label>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'PublicatieStatus',
    props: {
      metadata: Object
    },
    data () {
      return {
        publish_item: false,
        loading: true
      }
    },
    created(){
      if(this.metadata.publish_item=="ajax"){
        var redactie_api_url = 'http://localhost:5000';
        var redactie_api_div = document.getElementById('redactie_api_url');
        if( redactie_api_div ){
          redactie_api_url = redactie_api_div.innerText;
        }
        else{
          return; // do not load on other redactietool pages
        }

        var stat_params = {
          'pid': this.metadata.pid,
          'department': this.metadata.department
        };

        axios
          .get(redactie_api_url+'/publicatie_status', {params: stat_params})
          .then(res => {
            this.publish_item = res.data.publish_item;
            this.loading = false;
          }).catch(error => {
            console.log(error.toJSON());
            this.loading = false;
          });
      }
      else{
        this.publish_item = this.metadata.publish_item;
        this.loading = false;
      }
    },
  }
</script>

<style>
 #publicatiestatus_checked{
    margin-right: 5px;
 }

 .checkbox-spinner{
    display: inline-block;
    position: relative;
    float: left;
    background: transparent;
    margin-top: -10px;
    margin-left: -17px;
    margin-right: -10px;
 } 
</style>
