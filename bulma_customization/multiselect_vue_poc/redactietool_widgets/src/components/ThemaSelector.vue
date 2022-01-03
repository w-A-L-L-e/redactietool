<template>
  <div id="thema_selector">

  <multiselect v-model="value" 
    tag-placeholder="Voeg nieuw thema toe" 
    placeholder="Zoek thema" 
    label="title" 
    track-by="title" 
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
            {{ props.option.title }}
          </span>
          <span class="option_small">
            {{props.option.desc}}
          </span>
        </span>
    </template>
    <template 
      slot="option" 
      slot-scope="props">
        <div class="option__desc">
          <span class="option__title">{{ props.option.title }}</span>
          <span class="option__small">{{ props.option.desc }}</span>
        </div>
    </template>
  </multiselect>
  <textarea name="themas" v-model="json_value" id="thema_json_value"></textarea>

</div>
</template>

<script>
  import Multiselect from 'vue-multiselect'

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
            title: 'Politiek en overheid', 
            desc: 'Van politieke partijen en besluitvorming tot de werking van de overheid, wetgeving en burgerparticipatie. Zowel binnen- als buitenland',
            id: 'mediawijsheid'
          },
          {
            title: 'Mediawijsheid',
            desc: 'Mediawijsheid, beeldgeletterdheid, kritische zin',
            id: 'mediawijsheid'
          },
          { 
            title: 'Culturele diversiteit', 
            desc: 'Cultuurbeschouwing. Alles over de verscheidenheid aan culturen en culturele uitingen binnen een samenleving en het proces van wereldwijde culturele integratie (globalisering). Hier gaat het dan meer om symbolen, rituelen, ...',
            id: 'culturele_div'
          },
          { title: 'Thema 4', desc: 'Dit is de beschrijving voor thema 4', id: 'thema4' },
          { title: 'Thema 5', desc: 'Dit is de beschrijving voor thema 5', id: 'thema5'  },
          { title: 'Thema 6', desc: 'Dit is de beschrijving voor thema 6', id: 'thema6'  },
        ]
      }
    },
    methods: {
      addThema(newThema) {
        const thema = {
          title: newThema,
          desc: 'beschrijving voor nieuwe thema?',
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
