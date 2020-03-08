<template>
  <div class="">
    <div class="flex-columns flex-align-center new-category-container">
      <template v-if="!isAddingNew">
        <b-select
          v-model="currentCategoryId"
          v-on:change.native="selectCategory($event.target.value)"
          placeholder="Select a category"
          required
        >
          <option v-for="c in categories" v-bind:value="c.id">{{
            c.name
          }}</option>
        </b-select>

        <b-button
          type="is-info"
          icon="plus"
          v-on:click="isAddingNew = true"
          outlined
        >
          <b-icon icon="plus" size="is-small"></b-icon>
        </b-button>
      </template>

      <template v-else>
        <div class="flex-rows">
          <b-field label="New category name">
            <b-input v-model="newCategory" maxlength="128"></b-input>
          </b-field>
          <div class="flex-columns flex-space-between">
            <b-button type="is-warning" v-on:click="createCategory()"
              >Create new</b-button
            >
            <b-button
              type="is-danger"
              v-on:click="isAddingNew = false"
              outlined
            >
              <b-icon icon="close" size="is-small"></b-icon>
            </b-button>
          </div>
        </div>
      </template>
    </div>
    <div v-if="!loading">
      <new-note></new-note>
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
import newNote from "./new-note.vue";
import login from "./login.vue";
import loadIcon from "./load-icon.vue";

export default Vue.extend({
  components: { list, "new-note": newNote, "load-icon": loadIcon },
  data() {
    return {
      newCategory: "",
      isAddingNew: false,
      currentCategoryId: undefined
    };
  },
  computed: {
    loading() {
      return this.$store.state.notesLoading;
    },
    categories() {
      return this.$store.state.categories;
    },
    currentCategory() {
      return this.$store.getters.currentCategory;
    }
  },
  methods: {
    createCategory() {
      const name = this.$data.newCategory.trim();

      if (name) {
        this.$store.dispatch("createCategory", name);
        this.$data.newCategory = "";
        this.$data.isAddingNew = false;
      }
    },
    selectCategory(category: number) {
      this.$store.commit("setCurrentCategory", category);
    }
  },
  mounted: function() {
    this.$store.dispatch("loadCategories");
  },
  watch: {
    currentCategory: {
      handler: function(currentCategory) {
        this.$store.dispatch("loadNotes");
        this.$data.currentCategoryId = currentCategory?.id;
      },
      deep: true
    }
  }
});
</script>

<style></style>
