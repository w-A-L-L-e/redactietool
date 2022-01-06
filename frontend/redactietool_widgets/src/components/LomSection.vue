<template>
  <div class="lom1_section_wrapper">

      <h2 class="title is-clickable" v-on:click="toggleCollapse">
        Leerobject
        <CollapseIcon v-bind:minimized="isMinimized"/>
      </h2>
      <hr>

    <div id="lom1_section_block" v-bind:class="{minimized: isMinimized}">
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Type</label>
        </div>
        <div class="field-body">
          <div class="select">
            <select name="lom1_type" id="lom1_type">
              <option value="video">Video</option>
              <option value="audio">Audio</option>
            </select>
          </div>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label label-two-lines">Beoogde eindgebruiker</label>
        </div>
        <div class="field-body">
          <div class="select">
            <select name="lom1_beoogde_eindgebruiker" id="lom1_beoogde_eindgebruiker">
              <option value="Docent">Docent</option>
              <option value="Student">Student</option>
              <option value="Directie">Directie</option>
              <option value="ICT-coördinator">ICT-coördinator</option>
              <option value="Systeembeheerder">Systeembeheerder</option>
              <option value="Preventieadviseur">Preventieadviseur</option>
              <option value="GOK">GOK / Zorgcoördinator</option>
              <option value="Pedagogisch begeleider">Pedagogisch begeleider</option>
              <option value="Inspectielid">Inspectielid</option>
              <option value="Administratief personeel">Administratief personeel</option>
              <option value="Met pensioen">Met pensioen</option>
              <option value="Ouder">Ouder</option>
              <option value="Ander">Ander</option>
            </select>
          </div>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Taal</label>
        </div>
        <div class="field-body">
          <TalenSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Onderwijsniveaus</label>
        </div>
        <div class="field-body">
          <div class="select">
            <select name="lom1_onderwijsniveaus" id="lom1_onderwijsniveaus">
              <option value="Kleuteronderwijs">Kleuteronderwijs</option>
              <option value="Lager onderwijs">Lager onderwijs</option>
              <option value="Secundair onderwijs">Secundair onderwijs</option>
              <option value="Volwassenenonderwijs">Volwassenenonderwijs</option>
              <option value="Hoger onderwijs">Hoger onderwijs</option>
            </select>
          </div>
        </div>
      </div>


      <!-- todo: this data comes with request using suggest lib from knowledgegraph:
        {'id': 'https://data.meemoo.be/terms/ond/graad#lager-1ste-graad', 'label': 'Lager 1ste graad', 'definition': 'Lager 1ste graad'}
        {'id': 'https://data.meemoo.be/terms/ond/graad#lager-2de-graad', 'label': 'Lager 2de graad', 'definition': 'Lager 2de graad'}
        {'id': 'https://data.meemoo.be/terms/ond/graad#lager-3de-graad', 'label': 'Lager 3de graad', 'definition': 'Lager 3de graad'}
        {'id': 'https://data.meemoo.be/terms/ond/graad#secundair-1ste-graad', 'label': 'Secundair 1ste graad', 'definition': 'Secundair 1ste graad'}
        {'id': 'https://data.meemoo.be/terms/ond/graad#secundair-2de-graad', 'label': 'Secundair 2de graad', 'definition': 'Secundair 2de graad'}
        {'id': 'https://data.meemoo.be/terms/ond/graad#secundair-3de-graad', 'label': 'Secundair 3de graad', 'definition': 'Secundair 3de graad'}
      -->
      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Onderwijsgraden</label>
        </div>
        <div class="field-body">
          <div class="select">
            <select name="lom1_onderwijsniveaus" id="lom1_onderwijsniveaus">
              <option value="Kleuteronderwijs">Lager 1ste graad</option>
              <option value="Lager onderwijs">Lager 2de graad</option>
              <option value="Secundair onderwijs">Lager 3de graad</option>
              <option value="Volwassenenonderwijs">Secundair 1ste graad</option>
              <option value="Hoger onderwijs">Secundair 3de graad</option>
            </select>
          </div>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Thema</label>
        </div>
        <div class="field-body">
          <ThemaSelector/>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Vakken</label>
        </div>
        <div class="field-body">
          <VakkenSelector/>
        </div>
      </div>


      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label">Trefwoorden</label>
        </div>
        <div class="field-body">
          <TrefwoordenSelector/>
        </div>
      </div>

      <div class="field is-horizontal">
        <div class="field-label is-normal">
          <label class="label"></label>
        </div>
        <div class="field-body">
            <a target="_blank" href="http://link_trefwoorden_content_partners?">
              Bekijk trefwoorden van Content Partners
            </a>
        </div>
      </div>


    </div> <!-- lom1_section_block -->

  </div>
</template>

<script>
  import TalenSelector from './TalenSelector.vue'
  import ThemaSelector from './ThemaSelector.vue'
  import VakkenSelector from './VakkenSelector.vue'
  import TrefwoordenSelector from './TrefwoordenSelector.vue'
  import CollapseIcon from './CollapseIcon.vue'

  var pid = document.getElementById("pid").innerText;
  console.log("vue component received pid=", pid );

  export default {
    name: 'LomSection',
    components: {
      TalenSelector,
      ThemaSelector,
      VakkenSelector,
      TrefwoordenSelector,
      CollapseIcon
    },
    data () {
      return {
        isMinimized: false,
        pid: pid
      }
    },
    methods: {
      toggleCollapse: function(){
        this.isMinimized = !this.isMinimized;
      }
    }
  }
</script>


<style>
  .lom1_section_wrapper {
    margin-top: 40px;
    margin-bottom: 70px;
  }

  hr {
    border-bottom: 1px solid #363636;
    margin-top: -20px;
  }

  .minimized {
    display: none;
  }
</style>
