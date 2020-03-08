<template>
  <div class="app-container flex-rows flex-center">
    <load-icon></load-icon>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import loadIcon from "../ui/load-icon.vue";

export default Vue.extend({
  components: {"load-icon": loadIcon},
  data() {
    return {
    };
  },
  computed: {
  },
  methods: {
  },
  mounted: function {
  }
});
</script>

<style>
html,
body {
  height: 100%;
}

#app {
  font-size: 18px;
  font-family: "Roboto", sans-serif;
  color: blue;
}

.fill-width {
  width: 100%;
}

.flex-columns {
  display: flex;
  flex-direction: row;
}

.flex-rows {
  display: flex;
  flex-direction: column;
}

.flex-align {
  align-items: center;
}

.flex-center {
  align-items: center;
  justify-content: center;
}

.username-text {
  margin: 0 1em;
  text-transform: uppercase;
  font-weight: bold;
}

.navbar {
  padding: 0.3em 3em;
  background: transparent !important;
}

.journal-view {
  background: #15111a;
}

.view-container {
  overflow-y: auto;
}

.fill {
  width: 100%;
  height: 100%;
}

.app-container {
  min-height: 100vh;
  max-height: 100vh;
  position: relative;
}

.app-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100vh;
  pointer-events: none;

  & > div {
    position: relative;
    width: 100%;
    height: 100%;
    pointer-events: none;
  }
}

.upload-indicator {
  position: absolute;
  right: 1em;
  bottom: 1em;
  width: 5em;
  height: 5em;
  transition: linear 1s;
  opacity: 0;
}

.upload-indicator.is-uploading {
  opacity: 1;
}

.main-container {
  max-height: 100vh;
  overflow-y: auto;
}
</style>
