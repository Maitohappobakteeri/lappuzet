<template>
  <div class="goals-container">
    <div class="flex-columns flex-align-center new-category-container">
      <template v-if="!isAddingNew">
        <b-select
          v-model="currentTreeId"
          v-on:change.native="selectTree($event.target.value)"
          placeholder="Select a tree"
          required
        >
          <option v-for="c in trees" v-bind:value="c.id">{{ c.name }}</option>
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
          <b-field label="New tree name">
            <b-input v-model="newTreeName" maxlength="128"></b-input>
          </b-field>
          <div class="flex-columns flex-space-between">
            <b-button type="is-warning" v-on:click="createTree()"
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
      <!-- <new-note></new-note> -->
      <!-- <list></list> -->
      <div class="node-row-container" v-for="(nodeRow, index) in nodeRows">
        <div>
          <draggable
            @choose="startDrag($event)"
            @end="endDrag($event)"
            handle=".handle"
            v-bind="dragOptions"
          >
            <div v-bind:key="node.id" v-for="node in nodeRow">
              <tree v-bind:node="node"></tree>
            </div>
          </draggable>
        </div>
      </div>
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
import tree from "./goals/tree.vue";
import draggable from "vuedraggable";

function nodeRow(nodes: GoalTreeNodeDto[], node: GoalTreeNodeDto) {
  let n = node;
  let row = 0;
  while (n?.parent_node !== undefined && n?.parent_node !== null) {
    n = nodes.find(p => p.id == n.parent_node);
    ++row;
  }
  return row;
}

export default Vue.extend({
  components: {
    draggable,
    list,
    "new-note": newNote,
    "load-icon": loadIcon,
    tree: tree
  },
  data() {
    return {
      newTreeName: "",
      isAddingNew: false,
      currentTreeId: undefined
    };
  },
  computed: {
    dragOptions() {
      return {
        animation: 200,
        disabled: false,
        ghostClass: "ghost",
        chosenClass: "chosen",
        chosenDrag: undefined
      };
    },
    loading() {
      return this.$store.state.notesLoading;
    },
    trees() {
      return this.$store.state.goalTrees;
    },
    currentTree() {
      return this.$store.getters.currentGoalTree;
    },
    nodes() {
      return this.currentTree?.nodes || [];
    },
    nodeRows() {
      const nodes = this.nodes;
      const rows = {};
      const rowArr = [];
      for (const n of nodes) {
        const r = nodeRow(nodes, n);

        if (!rows[r]) {
          rows[r] = [];
        }
        rows[r].push({ ...n });
      }

      let i = 0;
      while (rows[i]) {
        const getParentPosition = node => {
          return i === 0
            ? 0
            : rows[i - 1].findIndex(p => p.id == node.parent_node);
        };

        let row = rows[i].sort(
          (a, b) => getParentPosition(a) - getParentPosition(b)
        );
        row = [...row];
        if (i === 0) {
          row[0].horizontalPosition = 0.5;
        } else {
          for (let nIndex = 0; nIndex < row.length; ++nIndex) {
            const node = row[nIndex];
            const parent = rows[i - 1].find(p => p.id == node.parent_node);
            node.parentHorizontalPosition = parent.horizontalPosition;
            node.horizontalPosition = (nIndex + 1) * (1 / (row.length + 1));
          }
        }
        rowArr.push(row);
        ++i;
      }

      return rowArr;
    }
  },
  methods: {
    createTree() {
      const name = this.$data.newTreeName.trim();

      if (name) {
        this.$store.dispatch("createGoalTree", name);
        this.$data.newTreeName = "";
      }

      this.$data.isAddingNew = false;
    },
    selectTree(tree: number) {
      this.$store.commit("setCurrentGoalTree", tree);
    },
    startDrag(s) {
      let el = s.explicitOriginalTarget;
      while (el.parentNode && el.dataset?.goaltreenodeid === undefined) {
        el = el.parentNode;
      }
      const targetId = el.dataset?.goaltreenodeid;
      this.$data.chosenDrag = targetId;
    },
    endDrag(s) {
      let el = s.explicitOriginalTarget;
      while (el.parentNode && el.dataset?.goaltreenodeid === undefined) {
        el = el.parentNode;
      }

      const targetNode = el.dataset?.goaltreenodeid;
      const movedNode = this.$data.chosenDrag;
      this.$store.dispatch("moveGoalTreeNodeTo", { movedNode, targetNode });
    }
  },
  mounted: function() {
    this.$store.dispatch("loadGoalTrees");
  },
  watch: {
    currentTree: {
      handler: function(curr, old) {
        if (curr?.id != old?.id) {
          this.$store.dispatch("loadGoalTree");
          this.$data.currentTreeId = curr.id;
        }
      },
      deep: true
    }
  }
});
</script>

<style lang="scss">
.node-row-container {
  height: 300px;
  border-top: 1px #ffffff44 solid;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  animation-name: node-row-animation-parent;
  animation-duration: 0.5s;
  animation-timing-function: ease-in;

  & > div {
    width: 100%;
    animation-name: node-row-animation;
    animation-duration: 2s;
    animation-timing-function: ease-in;
    height: 300px;
  }
}

$anim-color: #e84770;

@keyframes node-row-animation-parent {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

.goals-container {
  padding-top: 1em;
  margin-bottom: 200px;
  // background: white;
}
</style>
