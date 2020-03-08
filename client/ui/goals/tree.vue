<template>
  <div>
    <div></div>
    <div
      :data-goaltreenodeid="node.id"
      @dragover="onDragOver()"
      class="gtree-node-container flex-rows"
      :class="{
        isDragOver: isDragOver,
        edit: isEditing
      }"
      v-bind:style="{
        left: 'max( calc(' + node.horizontalPosition * 100 + '% - 125px), 0px )'
      }"
    >
      <template v-if="!isEditing">
        <div class="header">
          <p>{{ node.title }}</p>
          <div
            class="handle"
            @mouseover="hoverDrag = true"
            @mouseleave="hoverDrag = false"
          >
            <b-icon icon="drag" class="handle"></b-icon>
          </div>
        </div>
        <div class="content flex-grow">
          <p>{{ node.description }}</p>
        </div>
        <div class="button-container">
          <b-button type="is-danger is-light" v-on:click="addChildNode(node.id)"
            >Add</b-button
          >
          <b-button class="flex-grow" type="is-info" v-on:click="startEdit()"
            >Edit</b-button
          >
        </div>
      </template>
      <template v-else>
        <div class="header">
          <b-field label="Title">
            <b-input
              minlength="3"
              maxlength="256"
              v-model="editTitle"
            ></b-input>
          </b-field>
        </div>
        <div class="content flex-grow">
          <b-field label="Description">
            <b-input
              minlength="0"
              maxlength="512"
              size="description-size"
              type="textarea"
              v-model="editDescription"
            ></b-input>
          </b-field>
        </div>
        <div class="button-container">
          <b-button
            type="is-success"
            :disabled="isPending"
            v-on:click="saveEdit()"
            >Save</b-button
          >
          <b-button
            type="is-warning"
            :disabled="isPending"
            v-on:click="cancelEdit()"
            >Cancel</b-button
          >
          <b-button
            type="is-danger"
            :disabled="isPending"
            v-on:click="deleteNode(node.id)"
            >Delete</b-button
          >
        </div>
      </template>
    </div>
    <div
      class="connector-line"
      v-if="node.parentHorizontalPosition && !hoverDrag"
      v-bind:class="{
        reverse: node.horizontalPosition > node.parentHorizontalPosition
      }"
      v-bind:style="{
        left:
          'calc( ' +
          Math.min(node.horizontalPosition, node.parentHorizontalPosition) *
            100 +
          `% + ${
            node.horizontalPosition == node.parentHorizontalPosition ? 0 : 60
          }px )`,
        width: `calc( ${Math.max(
          node.horizontalPosition,
          node.parentHorizontalPosition
        ) *
          100 -
          Math.min(node.horizontalPosition, node.parentHorizontalPosition) *
            100}% - 120px )`
      }"
    ></div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

function changeHue(rgb, degree) {
  var hsl = rgbToHSL(rgb);
  hsl.h += degree;
  if (hsl.h > 360) {
    hsl.h -= 360;
  } else if (hsl.h < 0) {
    hsl.h += 360;
  }
  return hslToRGB(hsl);
}

// exepcts a string and returns an object
function rgbToHSL(rgb) {
  // strip the leading # if it's there
  rgb = rgb.replace(/^\s*#|\s*$/g, "");

  // convert 3 char codes --> 6, e.g. `E0F` --> `EE00FF`
  if (rgb.length == 3) {
    rgb = rgb.replace(/(.)/g, "$1$1");
  }

  var r = parseInt(rgb.substr(0, 2), 16) / 255,
    g = parseInt(rgb.substr(2, 2), 16) / 255,
    b = parseInt(rgb.substr(4, 2), 16) / 255,
    cMax = Math.max(r, g, b),
    cMin = Math.min(r, g, b),
    delta = cMax - cMin,
    l = (cMax + cMin) / 2,
    h = 0,
    s = 0;

  if (delta == 0) {
    h = 0;
  } else if (cMax == r) {
    h = 60 * (((g - b) / delta) % 6);
  } else if (cMax == g) {
    h = 60 * ((b - r) / delta + 2);
  } else {
    h = 60 * ((r - g) / delta + 4);
  }

  if (delta == 0) {
    s = 0;
  } else {
    s = delta / (1 - Math.abs(2 * l - 1));
  }

  return {
    h: h,
    s: s,
    l: l
  };
}

// expects an object and returns a string
function hslToRGB(hsl) {
  var h = hsl.h,
    s = hsl.s,
    l = hsl.l,
    c = (1 - Math.abs(2 * l - 1)) * s,
    x = c * (1 - Math.abs(((h / 60) % 2) - 1)),
    m = l - c / 2,
    r,
    g,
    b;

  if (h < 60) {
    r = c;
    g = x;
    b = 0;
  } else if (h < 120) {
    r = x;
    g = c;
    b = 0;
  } else if (h < 180) {
    r = 0;
    g = c;
    b = x;
  } else if (h < 240) {
    r = 0;
    g = x;
    b = c;
  } else if (h < 300) {
    r = x;
    g = 0;
    b = c;
  } else {
    r = c;
    g = 0;
    b = x;
  }

  r = normalize_rgb_value(r, m);
  g = normalize_rgb_value(g, m);
  b = normalize_rgb_value(b, m);

  return rgbToHex(r, g, b);
}

function normalize_rgb_value(color, m) {
  color = Math.floor((color + m) * 255);
  if (color < 0) {
    color = 0;
  }
  return color;
}

function rgbToHex(r, g, b) {
  return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

export default Vue.extend({
  props: ["node"],
  components: {},
  data() {
    return {
      hoverDrag: false,
      isDragOver: false,
      isDragOverTimeout: undefined,
      isEditing: false,
      isPending: false,
      editTitle: "",
      editDescription: ""
    };
  },
  computed: {
    backgroundColor() {
      return ["white"][this.node.id % 1];
    }
  },
  methods: {
    changeHue(color, deg) {
      return changeHue(color, deg);
    },
    addChildNode(nodeId) {
      this.$store.dispatch("createNewGoalTreeNode", nodeId);
    },
    onDragOver() {
      this.$data.isDragOver = true;

      if (this.$data.isDragOverTimeout) {
        clearTimeout(this.$data.isDragOverTimeout);
      }

      this.$data.isDragOverTimeout = setTimeout(() => {
        this.$data.isDragOver = false;
        this.$data.isDragOverTimeout = undefined;
      }, 500);
    },
    deleteNode(nodeId) {
      this.$store.dispatch("deleteGoalTreeNode", nodeId);
    },
    startEdit() {
      this.$data.isEditing = true;

      if (!this.$data.editTitle) {
        this.$data.editTitle = this.node.title;
        this.$data.editDescription = this.node.description || "";
      }
    },
    saveEdit() {
      this.$data.isPending = true;

      setTimeout(() => {
        this.$data.isPending = false;
      }, 1000);

      this.$store.dispatch("editGoalTreeNode", {
        id: this.node.id,
        title: this.$data.editTitle,
        description: this.$data.editDescription
      });
    },
    cancelEdit() {
      this.$data.isEditing = false;
    }
  },
  mounted: function() {},
  watch: {
    node: {
      handler: function(curr, old) {
        this.$data.isEditing = false;
        this.$data.isPending = false;
      }
    }
  }
});
</script>

<style lang="scss">
$anim-color: #e84770;

.ghost {
  .gtree-node-container {
    opacity: 0.4;
  }
}

.chosen:not(.ghost) {
  .gtree-node-container {
    opacity: 0.6;
    box-shadow: unset;
    border: 3px $anim-color solid;
  }
}

.gtree-node-container {
  // color: #fffdd0;
  position: absolute;
  // cursor: move;
  top: 10px;
  width: 250px;
  min-height: 250px;
  max-height: 280px;
  background: white;
  border: 2px #ffffffaa solid;
  box-shadow: 1px 1px 3px $anim-color;
  animation-name: node-animation;
  animation-duration: 20s;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  transition: 0.3s;

  .header {
    padding: 0.5em;
    transition: 0.3s;
    position: relative;
    color: #ff599f;
    text-transform: capitalize;
    border-bottom: lighten(#f18fa8, 20) 2px solid;
    p {
      font-family: "Cabin", sans-serif;
      font-size: 20px;
    }
    .handle {
      position: absolute;
      top: 4px;
      right: 4px;
      visibility: hidden;
      opacity: 0;
      transition: 1s;
    }
  }

  .content {
    padding: 0.5em;
  }

  .button-container {
    padding: 0.5em;
    visibility: hidden;
    opacity: 0;
    transition: 1s;
  }

  &:hover {
    z-index: 1;

    border: lighten(#f18fa8, 5) 2px solid;

    .header {
      border-bottom: lighten(#f18fa8, 5) 2px solid;
    }

    .handle {
      visibility: visible;
      opacity: 1;
      cursor: move;
    }

    .button-container {
      visibility: visible;
      opacity: 1;
    }
  }

  &.isDragOver {
    box-shadow: 1px 1px 3px $anim-color, -1px -2px 2px purple;
    .header {
      border-bottom: lighten(#f18fa8, 5) 2px solid;
    }
  }
}

.edit {
  z-index: 2;
  max-height: 340px;
  .content {
    margin-bottom: 0 !important;
    padding-bottom: 0;
  }
  .button-container {
    visibility: visible;
    opacity: 1;
  }
}

.connector-line {
  top: -40px;
  bottom: calc(100% - 10px);
  min-width: 1px;
  background: linear-gradient(
    to top left,
    rgba(0, 0, 0, 0) 0%,
    rgba(0, 0, 0, 0) calc(50% - 0.8px),
    #f18fa8 50%,
    rgba(0, 0, 0, 0) calc(50% + 0.8px),
    rgba(0, 0, 0, 0) 100%
  );
  &.reverse {
    background: linear-gradient(
      to top right,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0) calc(50% - 0.8px),
      #f18fa8 50%,
      rgba(0, 0, 0, 0) calc(50% + 0.8px),
      rgba(0, 0, 0, 0) 100%
    );
  }
  &.direct {
    background: linear-gradient(
      to right,
      rgba(0, 0, 0, 0) 0%,
      rgba(0, 0, 0, 0) calc(50% - 0.8px),
      #f18fa8 50%,
      rgba(0, 0, 0, 0) calc(50% + 0.8px),
      rgba(0, 0, 0, 0) 100%
    );
  }
  position: absolute;
}

.description-size {
  height: 100px;
  & > .textarea {
    height: 100% !important;
  }
}
</style>
