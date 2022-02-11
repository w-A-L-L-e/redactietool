<template>
    <div id="app">
      <LomSection v-bind:metadata="metadata"/>
      <PublicatieStatus v-bind:metadata="metadata"/>
    </div>
</template>

<script>
import LomSection from './components/LomSection.vue'
import PublicatieStatus from './components/PublicatieStatus.vue'

export default {
  name: 'App',
  data(){
    return {
      metadata: {},
    }
  },
  components: {
    LomSection,
    PublicatieStatus
  },
  created(){
    var metadata_div = document.getElementById("redactie_metadata");
      if(metadata_div){
        this.metadata = JSON.parse(metadata_div.value)
        // console.log("redactie metadata=", this.metadata);
      }
  }
}
</script>

<style>
#app {
  margin-top: -50px;
}
</style>
