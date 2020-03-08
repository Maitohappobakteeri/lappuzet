<template>
  <div class="grid-container">
    <div class="grid" ref="notes">
      <div
        v-for="note in notes"
        class="item"
        v-bind:key="note.id"
        :ref="'note-' + note.id"
        v-bind:class="[sizeClass(note)]"
      >
        <div class="item-content">
          <div class="">
            <div
              class="flex-rows note-container"
              v-bind:class="[bgClass(note)]"
            >
              <div class="note-header">
                <p class="is-uppercase">
                  {{ timeSince(note.createdAt) }}
                </p>
              </div>
              <div class="note-content flex-rows flex-center flex-grow">
                <div class="content has-text-centered">
                  {{ note.message }}
                </div>
              </div>
              <footer class="note-footer">
                <b-button
                  v-if="!note.resolved"
                  outlined
                  class="is-info"
                  v-on:click="resolve(note.id)"
                  >Resolve</b-button
                >
                <div v-else>
                  <b-icon icon="check" class="resolved-icon"></b-icon>
                </div>
              </footer>
            </div>
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
      return this.$store.state.notes;
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
      handler: function(notes) {
        if (this.$data.grid === null) {
          this.$data.notes = Array.from(notes);
        } else {
          if (this.$data.notes.length !== notes.length) {
            setTimeout(() => {
              this.$data.grid.add(this.$refs["note-" + notes[0].id], {
                index: 0
              });
              this.$data.grid.refreshItems().layout();
            });
          } else {
            setTimeout(() => {
              this.$data.grid.refreshItems().layout();
            });
          }
          this.$data.notes = Array.from(notes);
        }
      }
    }
  },
  mounted() {
    // TODO: These timeouts are bad
    setTimeout(() => {
      if (this.$data.grid === null) {
        this.$data.notes = Array.from(this.allNotes);
        this.$data.notes = Array.from(this.$data.notes);
      }
    });
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
  background: rgba(18, 18, 18, 0.2) !important;
  font-size: 1.1em;
  overflow-wrap: break-word;
}

.accent-1 {
  background: #863247 !important;
  color: #f2a5c6 !important;
}

.accent-2 {
  background: #884762 !important;
  color: #ff95c2 !important;
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

$anim-color: #e84770;

.note-container {
  // border: 1px #eee solid;
  // border-radius: 5px;

  background: white;
  border: 2px #ffffffaa solid;
  box-shadow: 1px 1px 3px $anim-color;
  animation-name: node-animation;
  animation-duration: 20s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  transition: 0.3s;
  min-height: 200px;
  overflow: hidden;
}

.note-header {
  padding: 0.3em 1em 0em 1em;
}

.note-footer {
  padding: 0em 1em 0.3em 1em;
}

.grid {
  max-width: 1100px;
  width: 100%;
  & > * {
    width: 100% !important;
    padding-bottom: 1em;
  }
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-flow: dense;
  justify-items: center;
  grid-column-gap: 1em;
  grid-row-gap: 1em;
}
.item {
  display: block;
  z-index: 1;

  &.size-1 {
    width: 250px;
  }

  &.size-2 {
    width: 250px;
  }

  &.size-3 {
    width: 250px;
  }
}
.item.muuri-item-dragging {
  z-index: 3;
}
.item.muuri-item-releasing {
  z-index: 2;
}
.item.muuri-item-hidden {
  z-index: 0;
}
.item-content {
  position: relative;
  width: 100%;
  height: 100%;
}

@media (min-width: 767px) {
  .card-content {
    padding: 2em !important;
  }
}

@media (max-width: 767px) {
  .note-container {
    min-height: unset;
  }
}
</style>
