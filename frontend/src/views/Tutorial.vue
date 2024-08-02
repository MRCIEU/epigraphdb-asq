<template lang="pug">
v-container
  v-row
    // Main
    v-col(cols="10")
      v-card
        v-card-title
          h2#intro(ref="introduction", v-intersect="onIntersect") Introduction
        v-card-text
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/asq-architecture-diagram.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.introduction", :breaks="false")
      v-divider.py-3
      v-card
        v-card-title
          h2#text-query(ref="text-query", v-intersect="onIntersect") Extraction of claims from the query text
        v-card-text
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/1-text-query.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.textQuery", :breaks="false")
          v-divider.py-3
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/2-claim-triple-selection.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(
                :source="docs.claimTripleSelection",
                :breaks="false"
              )
          v-divider.py-3
      v-card
        v-card-title
          h2#entity-harmonization(
            ref="entity-harmonization",
            v-intersect="onIntersect"
          ) Harmonization of the query entities
        v-card-text
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/3-claim-entity-selection.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(
                :source="docs.claimEntitySelection",
                :breaks="false"
              )
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/4-loading.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.loading", :breaks="false")
      v-divider.py-3
      v-card
        v-card-title
          h2#evidence-retrieval(
            ref="evidence-retrieval",
            v-intersect="onIntersect"
          ) Retrieval of evidence from EpiGraphDB
        v-card-text
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/5-evidence-summary.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.evidenceSummary", :breaks="false")
          v-divider.py-3
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/6-evidence-group.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.evidenceGroup", :breaks="false")
      v-divider.py-3
      v-card
        v-card-title
          h2#others(ref="others", v-intersect="onIntersect") Other topics
        v-card-text
          v-row
            v-col(cols="8")
              .d-flex.flex-column.align-center.justify-space-between
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/7-parameters-pre.png')",
                    max-width="960px",
                    contain
                  )
                v-card
                  v-img(
                    :src="require('@/assets/tutorial/annotated/7-parameters.png')",
                    max-width="960px",
                    contain
                  )
            v-col(cols="4")
              vue-markdown(:source="docs.parameters", :breaks="false")
    // Sidebar
    v-col(cols="2")
      toc(:outline="outline", @goto="jump")
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";

import Toc from "@/components/widgets/Toc.vue";
import * as tutorialText from "@/resources/docs/tutorial";

const VIEW_TITLE = "ASQ: tutorial";

export default Vue.extend({
  name: "TutorialView",
  components: {
    Toc,
  },
  data() {
    return {
      docs: tutorialText,
      outline: {
        introduction: {
          ref: "introduction",
          label: "Introduction",
          focus: false,
        },
        "text-query": {
          ref: "text-query",
          label: "Extraction of claims",
          focus: false,
        },
        "entity-harmonization": {
          ref: "entity-harmonization",
          label: "Harmonization of the query entities",
          focus: false,
        },
        "evidence-retrieval": {
          ref: "evidence-retrieval",
          label: "Retrieval of evidence",
          focus: false,
        },
        others: {
          ref: "others",
          label: "Other topics",
          focus: false,
        },
      },
    };
  },
  computed: {
    outlineItems(): Array<Record<string, any>> {
      return _.chain(this.outline)
        .mapValues((item) => item)
        .value();
    },
  },
  mounted: function () {
    document.title = VIEW_TITLE;
    this.$store.dispatch("queryStage/setQueryMode", "off");
  },
  methods: {
    onIntersect(entries): void {
      // console.log(entries);
      const focus = entries[0].isIntersecting;
      const id = entries[0].target.id;
      this.outline[id].focus = focus;
    },
    jump(ref): void {
      const target = this.$refs[ref];
      // @ts-ignore
      this.$vuetify.goTo(target);
    },
  },
});
</script>

<style scoped>
#toc-card {
  position: fixed;
}
</style>
