<template>
  <div class="login-container">
    <form v-if="!isPending" action="#">
      <b-field label="User">
        <b-input v-model="username"></b-input>
      </b-field>
      <b-field label="Password">
        <b-input type="password" v-model="password"></b-input>
      </b-field>
      <button class="button" v-on:click="signIn()">Sign in</button>
    </form>
    <load-icon v-else></load-icon>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import loadIcon from "./load-icon.vue";

export default Vue.extend({
  components: { "load-icon": loadIcon },
  data() {
    return {
      username: "",
      password: ""
    };
  },
  computed: {
    error() {
      return this.$store.state.login.error;
    },

    isPending() {
      return this.$store.state.login.pending;
    }
  },
  methods: {
    signIn() {
      this.$store.commit("signin", {
        username: this.$data.username,
        password: this.$data.password
      });
    }
  },
  watch: {
    error: {
      handler: function(error) {
        if (error) {
          this.$buefy.toast.open({
            duration: 10000,
            message: `Not authorized`,
            position: "is-bottom",
            type: "is-danger"
          });
        }
      },
      deep: true
    }
  }
});
</script>

<style>
label {
  color: pink !important;
}

.login-container {
  width: 100%;
  display: flex;
  justify-content: center;
  padding: 5em;
}
</style>
