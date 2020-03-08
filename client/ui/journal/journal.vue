<template>
  <div>
    <div v-if="!loading">
      <stats class="chart"></stats>
      <new-entry></new-entry>
      <list></list>
    </div>
    <div v-else class="flex-rows flex-center">
      <load-icon></load-icon>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import list from "./list.vue";
import newEntry from "./new-entry.vue";
import stats from "./stats.vue";
import loadIcon from "../load-icon.vue";

export default Vue.extend({
  components: {
    stats: stats,
    list,
    "new-entry": newEntry,
    "load-icon": loadIcon
  },
  computed: {
    loading() {
      return this.$store.state.journalLoading;
    }
  },
  mounted: function() {
    this.$store.dispatch("loadJournal");
  }
});
</script>

<style>
.chart {
  max-height: 200px;
}
</style>
