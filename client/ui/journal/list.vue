<template>
  <div class="grid-container">
    <div
      class="flex-rows flex-center"
      v-for="(note, index) in allNotes"
      v-bind:key="note.id"
      :ref="'note-' + note.id"
    >
      <div class="entry-separator" v-if="index !== 0"></div>
      <div class="card" v-bind:class="[bgClass(note)]">
        <div class="card-header">
          <p class="is-uppercase title is-4">
            {{ timeSince(note.createdAt) }}
          </p>
        </div>
        <div class="card-content">
          <div class="content has-text-centered">
            {{ note.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  data() {
    return {
      grid: null,
      notes: []
    };
  },
  computed: {
    allNotes() {
      return this.$store.state.journal;
    }
  },
  methods: {
    timeSince(date: Date) {
      const now = new Date();
      const diff = now - date;

      const days = diff / (1000 * 60 * 60 * 24);
      if (days >= 1) {
        return Math.floor(days) + " days ago";
      }

      const hours = diff / (1000 * 60 * 60);
      if (hours >= 1) {
        return Math.floor(hours) + " hours ago";
      }

      const minutes = diff / (1000 * 60);
      if (minutes >= 1) {
        return Math.floor(minutes) + " minutes ago";
      }

      return "Now";
    },
    sizeClass(note) {
      if (note.message.length > 100) {
        return "size-3";
      }

      return note.message.length < 30 ? "size-1" : "size-2";
    },
    bgClass(note) {
      if (note.resolved) {
        return "resolved";
      }

      if (note.id % 2 === 0) {
        return "accent-1";
      }

      return "accent-2";
    },
    resolve(noteId) {
      this.$store.dispatch("resolveNote", noteId);
    }
  },
  watch: {
    allNotes: {
      handler: function(notes) {}
    }
  }
});
</script>

<style lang="scss">
.grid-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-header {
  padding: 1em;
}

.card-content {
  background: white !important;
  font-size: 1.1em;
  padding: 0.5em 0.5em 1em 0.5em !important;
}

.accent-1 {
  background: white !important;
  color: #ff599f !important;
}

.accent-2 {
  background: white !important;
  color: #ff599f !important;
}

.resolved {
  background: #93888b !important;
}

.resolved-icon {
  color: darken(#ff599f, 30) !important;
}

.grid-note {
  width: 100%;
  height: 100%;
}

.note {
  margin: 2em 0;

  & > .card {
    max-width: 800px;
    width: 100%;
    margin: 0 auto;
  }
}

.entry-separator {
  height: 32px;
  width: 3px;
  background: #fd9ef3;
}
</style>
