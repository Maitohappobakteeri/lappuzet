<template>
  <div class="tile note">
    <div class="card is-info new-entry-bg">
      <div class="card-header">
        <p class="is-uppercase title is-4">
          New journal entry
        </p>
      </div>
      <div class="card-content new-note-content">
        <div class="content flex-rows">
          <div class="flex-columns additional-inputs-container">
            <b-field label="Mood">
              <b-select v-model="mood">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </b-select>
            </b-field>

            <b-field label="Sleep">
              <b-select v-model="sleep">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </b-select>
            </b-field>

            <b-field label="Food">
              <b-select v-model="food">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </b-select>
            </b-field>

            <b-field label="Stress">
              <b-select v-model="stress">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </b-select>
            </b-field>
          </div>

          <b-field>
            <b-input
              v-model="message"
              maxlength="1500"
              type="textarea"
            ></b-input>
          </b-field>
        </div>
      </div>
      <footer class="card-footer">
        <a v-on:click="create()" class="card-footer-item">Add entry</a>
      </footer>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      message: "",
      food: 3,
      sleep: 3,
      mood: 3,
      stress: 3
    };
  },
  computed: {},
  methods: {
    create() {
      const message = this.$data.message.trim();

      if (message) {
        this.$store.dispatch("createJournalEntry", {
          message,
          additional: {
            food: this.$data.food,
            sleep: this.$data.sleep,
            mood: this.$data.mood,
            stress: this.$data.stress
          }
        });
        this.$data.message = "";
        this.$data.food = 3;
        this.$data.sleep = 3;
        this.$data.mood = 3;
        this.$data.stress = 3;
      }
    }
  }
});
</script>

<style lang="scss">
.card-header {
  padding: 1em;
}

.new-entry-bg {
  background: #ffd1fa !important;
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

.additional-inputs-container {
  flex-wrap: wrap;

  & > * {
    margin: 1em 2em;
  }
}

textarea {
  min-height: 80px !important;
}
</style>
