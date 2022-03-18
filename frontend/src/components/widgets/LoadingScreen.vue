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

import * as evidenceTypesDocs from "@/resources/docs/evidence-types";
import * as params from "@/resources/docs/params";
import * as ents from "@/resources/docs/ents";
import * as generalDocs from "@/resources/docs/docs";
import {
  makeNetworkPlotDocs,
  makeOntologyPlotDocs,
} from "@/funcs/network-plot";

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
  mounted: function () {
    this.docList = this.makeDocs();
  },
  methods: {
    makeDocs(): string[] {
      const paramDocs = this._.values(params);
      const entsDocs = this._.values(ents);
      const general = this._.values(generalDocs);
      const networkPlotDocs = makeNetworkPlotDocs();
      const ontologyPlotDocs = makeOntologyPlotDocs();
      const networkDocs = [networkPlotDocs, ontologyPlotDocs];
      const evidenceTypeDocs = this._.chain([
        evidenceTypesDocs.tripleLiteratureEvidenceTypes.directional,
        evidenceTypesDocs.tripleLiteratureEvidenceTypes.undirectional,
        evidenceTypesDocs.assocEvidenceTypes.undirectional,
        evidenceTypesDocs.assocEvidenceTypes.directional,
      ])
        .map((item) => this._.values(item))
        .flatten()
        .value();
      const docGroups = [
        networkDocs,
        general,
        entsDocs,
        paramDocs,
        evidenceTypeDocs,
      ];
      const fullDocs = this._.chain(docGroups)
        .flatten()
        .filter((e) => typeof e == "string")
        .value();
      if (this.testLoading) {
        return fullDocs;
      }
      const res = this._.sampleSize(fullDocs, this.numDocs);
      return res;
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
