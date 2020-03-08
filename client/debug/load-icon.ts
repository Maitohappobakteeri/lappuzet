import Vue from "vue";
import Buefy from "buefy";
import "babel-polyfill";
import app from "./load-icon.vue";

Vue.use(Buefy);

new Vue({
  el: "#app",
  render: h => h(app)
});
