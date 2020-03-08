<template>
  <div class="tile note">
    <div class="card is-info new-note-bg">
      <div class="card-header">
        <p class="is-uppercase title is-4">
          New note
        </p>
      </div>
      <div class="card-content new-note-content">
        <div class="content">
          <b-field>
            <b-input
              v-model="message"
              maxlength="128"
              type="textarea"
            ></b-input>
          </b-field>
        </div>
      </div>
      <footer class="card-footer">
        <a v-on:click="create()" class="card-footer-item">Create</a>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      message: ""
    };
  },
  computed: {},
  methods: {
    create() {
      const message = this.$data.message.trim();

      if (message) {
        this.$store.dispatch("createNote", message);
        this.$data.message = "";
      }
    }
  }
});
</script>

<style lang="scss">
.card-header {
  padding: 1em;
}

.new-note-bg {
  background: white !important;
}

.new-note-content {
  padding: 0.25em !important;
}

.new-note {
  margin: 2em 0;

  & > .card {
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
  }
}

textarea {
  min-height: 80px !important;
}
</style>
