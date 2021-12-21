<template>
  <div class="lom1_section_wrapper">

      <h2 class="title is-clickable">
        Leerobjectmetadata trap 1
        <div class="minimize-icon-wrapper" id="lom1_section_icon">
          <!-- TODO fix icons
          <span class="icon-unfolded">
            <ion-icon name="chevron-down-circle-outline" 
            role="img" class="md hydrated" aria-label="chevron down circle outline"></ion-icon>
          </span>
          <span class="icon-folded">
            <ion-icon name="chevron-forward-circle-outline" 
            role="img" class="md hydrated" aria-label="chevron forward circle outline"></ion-icon>
          </span>
          -->
        </div>
      </h2>
      <hr>

      <div id="lom1_section_block">


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
            <div class="select is-multiple">
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
    </div> <!-- lom1_section_block -->

  </div>
</template>

<script>
  import TalenSelector from './TalenSelector.vue'

  export default {
    name: 'LomSectionOne',
    components: {
      TalenSelector,
    },
    data () {
      return {};
    },
    methods: {
    }
  }
</script>


<style>
  .lom1_section_wrapper {
    margin-top: 20px;
    margin-bottom: 70px;
  }
  
</style>
