<template>
  <div id="trefwoorden_selector">
    <multiselect v-model="value" 
      tag-placeholder="Maak nieuw trefwoord aan" 
      placeholder="Zoek of voeg een nieuw trefwoord toe" 
      label="name" 
      track-by="code" 
      :options="options" :multiple="true" 
      :taggable="true" @tag="addTrefwoord" @input="updateValue">
    </multiselect>
    <textarea name="trefwoorden" v-model="json_value" id="trefwoorden_json_value"></textarea>
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
    data () {
      return {
        value: default_value,
        json_value: JSON.stringify(default_value),
        options: [
          { name: 'reportage', code: 'reportage' },
          { name: 'Silent Movie', code: 'Silent Movie' },
          { name: 'Belgium', code: 'Belgium' },
          { name: 'France', code: 'France' },
          { name: 'Spain', code: 'Spain' },
          { name: "BURGER", code: 'BURGER' }, 
          { name: "CONFLICT", code: 'CONFLICT' }, 
          { name: "CONVENTIE VAN GENEVE", code: 'CONVENTIE VAN GENEVE' }, 
          { name: "INTERNATIONAAL STRAFGERECHTSHOF", code: 'INTERNATIONAAL STRAFGERECHTSHOF' }, 
          { name: "MENSENRECHT", code: 'MENSENRECHT' }, 
          { name: "OORLOG", code: 'OORLOG' }, 
          { name: "OORLOGSMISDAAD", code: 'OORLOGSMISDAAD' }, 
          { name: "SCHENDING", code: 'SCHENDING' }, 
          { name: "STRAFRECHT", code: 'STRAFRECHT' }, 
          { name: "VAN DEN WIJNGAERT CHRIS", code: 'VAN DEN WIJNGAERT CHRIS' }, 
          { name: "VEILIGHEID", code: 'VEILIGHEID' }
          // TODO: populate this using a div in jinja or axios call !!!
          // coming from the suggest library (aka knowledge graph).
        ]
      }
    },
    created(){
      var keyword_div = document.getElementById("item_keywords");
      if(keyword_div){
        var keywords = JSON.parse(keyword_div.innerText);
        for(var k in keywords){
          var keyword = keywords[k]
          default_value.push(
            {
              'name': keyword['value'],
              'code': keyword['value']
            }
          );
        }
      }
      this.json_value = JSON.stringify(default_value);
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
</style>
