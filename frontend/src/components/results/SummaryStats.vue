<template>
  <div>
    <json-viewer
      theme="json-viewer-gruvbox-dark"
      :expand-depth="9"
      :value="data"
      class="json-view-focused"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "SummaryStats",
  components: {
    //
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      //
    };
  },
  computed: {
    tripleView(): boolean {
      return this.$route.name == "TripleView";
    },
  },
  methods: {
    //
  },
});
</script>
