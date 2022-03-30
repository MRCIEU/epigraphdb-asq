<template lang="pug">
v-container
  v-row
    v-spacer
    v-col(cols="8")
      v-card.loading-doc-card
        v-card-title
          p
            span Now loading &nbsp;
            v-progress-circular(indeterminate, :size="30")
          v-spacer
          .text-center.text-body-2(style="width: 720px")
            p {{ message }}...
            v-progress-linear(:value="stage", height="10")
        v-carousel(
          v-model="carousel",
          :cycle="carouselCycle",
          hide-delimiters,
          show-arrows-on-hover,
          interval="4000"
        )
          v-carousel-item(v-for="(item, idx) in docList", :key="idx")
            v-card-title
              span Documentation fragments &nbsp;
                | \#{{ idx }} / {{ docList.length }}
            v-row
              v-spacer
              v-col(cols="10")
                v-card-text(style="overflow-y: auto")
                p.blockquote
                  vue-markdown(:source="item", :breaks="false")
              v-spacer
    v-spacer
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "LoadingScreen",
  components: {
    //
  },
  props: {
    message: {
      type: String,
      default: null,
    },
    stage: {
      type: Number,
      default: 0,
    },
  },
  data: () => ({
    carousel: 0,
    docList: [],
    numDocs: 10,
  }),
  computed: {
    testLoading(): boolean {
      return this.$route.name == "Loading";
    },
    snackbarVisible(): boolean {
      return this.$store.state.snackbar.visible;
    },
    carouselCycle(): boolean {
      const regular = true;
      if (this.snackbarVisible) return false;
      if (this.testLoading) return false;
      return regular;
    },
  },
  mounted: async function () {
    this.docList = await this.getDocs();
  },
  methods: {
    async getDocs(): Promise<string[]> {
      const fullDocs = await this.$store.getters["docs/getFlattenDocs"];
      if (this.testLoading) {
        return fullDocs;
      }
      return this._.sampleSize(fullDocs, this.numDocs);
    },
  },
});
</script>

<style>
.loading-doc-card {
  height: 720px;
  text-overflow: ellipsis;
  overflow: hidden;
}
</style>
