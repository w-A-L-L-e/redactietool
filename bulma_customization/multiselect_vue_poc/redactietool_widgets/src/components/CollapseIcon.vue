<template>
  <div class="minimize-icon-wrapper">
    <span v-bind:class="[minimized ? 'icon-folded' : 'icon-unfolded']">
      <ion-icon name="chevron-down-circle-outline" 
      role="img" class="md hydrated" aria-label="chevron down circle outline"></ion-icon>
    </span>
    <span v-bind:class="[minimized ? 'icon-unfolded' : 'icon-folded']">
      <ion-icon 
        name="chevron-forward-circle-outline" 
        role="img" class="md hydrated" 
        aria-label="chevron forward circle outline"
      >
      </ion-icon>
    </span>
  </div>
</template>

<script>
  export default {
    name: 'CollapseIcon',
    components: {
    },
    props: {
      minimized: Boolean
    },
    methods: {
      updateValue(value){
        this.json_value = JSON.stringify(value)
      }
    }
  }
</script>

<style>
  .minimize-icon-wrapper {
    float: right;
  }

  .icon-folded {
    display: none;
  }

  .icon-unfolded {
    display: block;
  }
</style>
