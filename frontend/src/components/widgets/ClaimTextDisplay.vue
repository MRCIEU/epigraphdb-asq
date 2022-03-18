<template>
  <div>
    <p>Query text segmented by sentence.</p>
    <div class="claim-text-display">
      <div v-for="item in sentItems" :key="item.idx">
        <span class="text-caption font-weight-light">#{{ item.idx }}</span>
        <v-sheet color="grey lighten-4">
          <p>{{ item.sent }}</p>
        </v-sheet>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

export default Vue.extend({
  name: "ClaimTextDisplay",
  props: {
    sents: {
      type: Array as PropType<string[]>,
      required: true,
    },
  },
  computed: {
    sentItems() {
      const items = this._.chain(this.sents)
        .map((item, idx) => {
          return {
            idx: idx,
            sent: item,
          };
        })
        .value();
      return items;
    },
  },
});
</script>

<style scoped>
.claim-text-display {
  max-height: 750px;
  overflow-y: scroll;
}
</style>
