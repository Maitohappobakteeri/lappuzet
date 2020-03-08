<script>
import Vue from "vue";
import { Line } from "vue-chartjs";

const options = {
  maintainAspectRatio: false,
  responsive: true,
  scales: {
    yAxes: [
      {
        display: true,
        ticks: {
          suggestedMin: 0,
          suggestedMax: 5
        }
      }
    ]
  }
};

export default Vue.extend({
  extends: Line,
  computed: {
    journalStats() {
      return this.$store.getters.journalStats;
    }
  },
  mounted() {
    this.renderChart(
      {
        datasets: this.journalStats,
        labels: (this.journalStats[0].data || []).map((_, i) => i)
      },
      options
    );
  },
  watch: {
    journalStats: {
      handler: function(stats) {
        this.renderChart(
          {
            datasets: stats,
            labels: (this.journalStats[0].data || []).map((_, i) => i)
          },
          options
        );
      },
      deep: true
    }
  }
});
</script>

<style scoped></style>
