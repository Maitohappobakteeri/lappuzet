<template>
  <div class="app-container" v-bind:class="[viewClass]">
    <login v-if="!user"></login>
    <div v-else class="main-container">
      <b-navbar>
        <template slot="brand">
          <!-- <b-navbar-item tag="router-link" :to="{ path: '/' }">
            Lappuzet
          </b-navbar-item> -->
        </template>
        <template slot="start">
          <b-navbar-item>
            <router-link to="/notes">Notes</router-link>
          </b-navbar-item>
          <b-navbar-item>
            <router-link to="/journal">Journal</router-link>
          </b-navbar-item>
          <b-navbar-item>
            <router-link to="/goals">Goals</router-link>
          </b-navbar-item>
        </template>

        <template slot="end">
          <b-navbar-item tag="div">
            <div class="flex-columns flex-align">
              <p class="username-text">{{ user.username }}</p>
              <b-button type="is-danger" v-on:click="signOut()"
                ><b-icon icon="logout" size="is-small"></b-icon
              ></b-button>
            </div>
          </b-navbar-item>
        </template>
      </b-navbar>
      <div class="view-container">
        <router-view></router-view>
      </div>
    </div>
    <div class="app-overlay">
      <div>
        <div
          v-bind:class="{ 'is-uploading': isUploading }"
          class="flex-rows flex-center upload-indicator"
        >
          <load-icon></load-icon>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import list from "./list.vue";
import newNote from "./new-note.vue";
import login from "./login.vue";
import loadIcon from "./load-icon.vue";

export default Vue.extend({
  components: { list, "new-note": newNote, login, "load-icon": loadIcon },
  data() {
    return {
      message: "asd"
    };
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    signedIn() {
      return this.$store.state.user !== null;
    },
    viewClass() {
      return this.$route.matched[0]?.name === "goal"
        ? "goal-view"
        : "note-view";
    },
    isUploading() {
      return this.$store.state.uploadingData;
    }
  },
  methods: {
    signOut() {
      this.$store.commit("signOut");
    }
  },
  mounted: function() {}
});
</script>

<style lang="scss">
html,
body {
  height: 100vh;
  width: 100vw;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background: linear-gradient(to bottom, #fff5f5, #fedcb2) !important;
  font-family: "Merriweather Sans", sans-serif;
}

a,
p {
  font-family: "Open Sans", sans-serif;
}

#app {
  font-size: 18px;
  // font-family: "Roboto", sans-serif;
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

.flex-grow {
  flex-grow: 1;
}

.flex-space-between {
  justify-content: space-between;
}

.new-category-container {
  padding: 0 0 0 1em;
}

.username-text {
  margin: 0 1em;
  text-transform: uppercase;
  font-weight: bold;
  font-family: "Merriweather Sans", sans-serif;
}

.navbar {
  padding: 0.3em 3em;
  border-bottom: 4px solid darken(#ffebea, 20);
}

.journal-view {
  background: #15111a;
}

.goal-view {
  background: linear-gradient(to bottom, #fff5f5, #fedcb2);
}

.note-view {
  background: linear-gradient(to bottom, #fff5f5, #fedcb2);
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
