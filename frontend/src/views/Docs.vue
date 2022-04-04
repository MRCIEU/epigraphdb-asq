<template lang="pug">
v-container
  v-row
    //- Main
    v-col
      //- # About
      v-card
        v-card-title
          h2#about(ref="about", v-intersect="onIntersect") Annotated Semantic Queries (ASQ)
        v-card-text
          vue-markdown(
            :source="$store.state.docs.about.aboutInit",
            :breaks="false"
          )
          .d-flex.flex-column.align-center.justify-space-between
            v-img(
              :src="require('@/assets/asq-architecture-diagram.png')",
              max-width="960px",
              contain
            )
          vue-markdown(
            :source="$store.state.docs.about.aboutCitation",
            :breaks="false"
          )
      v-divider.py-3
      //- # Terminology
      v-card
        v-card-title
          h2#terminology(ref="terminology", v-intersect="onIntersect") Terminology
        v-card-text
          v-row
            v-col
              vue-markdown(
                :source="$store.state.docs.about.aboutPt0",
                :breaks="false"
              )
              vue-markdown(
                :source="$store.state.docs.about.aboutPt1",
                :breaks="false"
              )
            v-col
              vue-markdown(
                :source="$store.state.docs.about.aboutPt2",
                :breaks="false"
              )
      v-divider.py-3
      v-row
        v-col
          //- # Ents
          v-card
            v-card-title
              h2#ents(ref="ents", v-intersect="onIntersect") Entities
            v-card-text
              p(v-for="(item, idx) in $store.state.docs.ents", :key="idx")
                vue-markdown(:source="item", :breaks="false")
        v-col
          //- # Params
          v-card
            v-card-title
              h2#params(ref="params", v-intersect="onIntersect") Parameters
            v-card-text
              p(v-for="(item, idx) in $store.state.docs.params", :key="idx")
                vue-markdown(:source="item", :breaks="false")
      v-divider.py-3
      v-row
        v-col
          //- # Stages
          v-card
            v-card-title
              h2#stages(ref="stages", v-intersect="onIntersect") Query stages
            v-card-text
              p(v-for="(item, idx) in stageDocs", :key="idx")
                vue-markdown(:source="item", :breaks="false")
        v-col
          //- # Components
          v-card
            v-card-title
              h2#components(ref="components", v-intersect="onIntersect") Components
            v-card-text
              p(v-for="(item, idx) in componentDocs", :key="idx")
                vue-markdown(:source="item", :breaks="false")
      v-divider.py-3
      //- # Triple and literature evidence
      v-card
        v-card-title
          h2#triple-literature-evidence(
            ref="triple-literature-evidence",
            v-intersect="onIntersect"
          ) Triple and literature evidence
        v-card-text
          v-row
            v-col
              h4 Directional predicates
              p(
                v-for="(item, idx) in $store.state.docs.evidence.tripleLiteratureEvidenceTypes.directional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
            v-col
              h4 Non-directional predicates
              p(
                v-for="(item, idx) in $store.state.docs.evidence.tripleLiteratureEvidenceTypes.undirectional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
      v-divider.py-3
      //- # Association evidence
      v-card
        v-card-title
          h2#assoc-evidence(ref="assoc-evidence", v-intersect="onIntersect") Association evidence types
        v-card-text
          v-row
            v-col
              h4 Directional predicates
              p(
                v-for="(item, idx) in $store.state.docs.evidence.assocEvidenceTypes.directional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
            v-col
              h4 Non-directional predicates
              p(
                v-for="(item, idx) in $store.state.docs.evidence.assocEvidenceTypes.undirectional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
      v-divider.py-3
      //- # Scores
      v-card
        v-card-title
          h2#scores(ref="scores", v-intersect="onIntersect") Evidence Scores
        v-card-text
          v-row
            v-col
              vue-markdown(:source="$store.state.docs.scores.mappingScore")
              vue-markdown(:source="$store.state.docs.scores.evidenceScore")
            v-col
              vue-markdown(:source="$store.state.docs.scores.tripleScore")
              vue-markdown(:source="$store.state.docs.scores.assocScore")
      v-divider.py-3
      //- # medrxiv analysis
      v-card
        v-card-title
          h2#analysis(ref="analysis", v-intersect="onIntersect") MedRxiv analysis
        v-card-text
          vue-markdown(:source="$store.state.docs.analysis.about")
    // Sidebar
    v-col(cols="2")
      toc(:outline="outline", @goto="jump")
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";

import Toc from "@/components/widgets/Toc.vue";

const VIEW_TITLE = "ASQ: docs";

export default Vue.extend({
  name: "DocsView",
  components: {
    Toc,
  },
  data() {
    return {
      outline: {
        about: {
          ref: "about",
          label: "About",
          focus: false,
        },
        terminology: {
          ref: "terminology",
          label: "Terminology",
          focus: false,
        },
        ents: {
          ref: "ents",
          label: "Entities",
          focus: false,
        },
        params: {
          ref: "params",
          label: "Parameters",
          focus: false,
        },
        stages: {
          ref: "stages",
          label: "Stages",
          focus: false,
        },
        components: {
          ref: "components",
          label: "Components",
          focus: false,
        },
        "triple-literature-evidence": {
          ref: "triple-literature-evidence",
          label: "Triple and literature evidence",
          focus: false,
        },
        "assoc-evidence": {
          ref: "assoc-evidence",
          label: "Association evidence",
          focus: false,
        },
        scores: {
          ref: "scores",
          label: "Evidence scores",
          focus: false,
        },
        analysis: {
          ref: "analysis",
          label: "MedRxiv analysis",
          focus: false,
        },
      },
      stageDocs: _.chain([
        // be verbose
        "queryParsing",
        "tripleSelect",
        "entHarmonizationOntology",
        "evidenceSummary",
        "tripleLiteratureEvidence",
        "assocEvidence",
      ])
        .map((key) => this.$store.state.docs.general[key])
        .value(),
    };
  },
  computed: {
    outlineItems(): Array<Record<string, any>> {
      return _.chain(this.outline)
        .mapValues((item) => item)
        .value();
    },
    tripleEvidenceDocs(): Record<string, Array<string>> {
      const baseDocs = this.$store.state.evidence.tripleLiteratureEvidenceTypes;
      const res = _.chain(baseDocs)
        .mapValues((items) => {
          const res = _.chain(items).values().value();
          return res;
        })
        .value();
      return res;
    },
    assocEvidenceDocs(): Record<string, Array<string>> {
      const baseDocs = this.$store.state.evidence.assocEvidenceTypes;
      const res = _.chain(baseDocs)
        .mapValues((items) => {
          const res = _.chain(items).values().value();
          return res;
        })
        .value();
      return res;
    },
    componentDocs(): string[] {
      const res = this._.chain(this.$store.state.docs.plots).values().value();
      return res;
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
