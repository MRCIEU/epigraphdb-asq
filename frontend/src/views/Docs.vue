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
          vue-markdown(:source="docsView.aboutInit", :breaks="false")
          vue-markdown(:source="docsView.aboutCitation", :breaks="false")
      v-divider.py-3
      //- # Terminology
      v-card
        v-card-title
          h2#terminology(ref="terminology", v-intersect="onIntersect") Terminology
        v-card-text
          v-row
            v-col
              vue-markdown(:source="docsView.aboutPt0", :breaks="false")
              vue-markdown(:source="docsView.aboutPt1", :breaks="false")
            v-col
              vue-markdown(:source="docsView.aboutPt2", :breaks="false")
      v-divider.py-3
      v-row
        v-col
          //- # Ents
          v-card
            v-card-title
              h2#ents(ref="ents", v-intersect="onIntersect") Entities
            v-card-text
              p(v-for="(item, idx) in entsDocs", :key="idx")
                vue-markdown(:source="item", :breaks="false")
        v-col
          //- # Params
          v-card
            v-card-title
              h2#params(ref="params", v-intersect="onIntersect") Parameters
            v-card-text
              p(v-for="(item, idx) in params", :key="idx")
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
      v-card
        v-card-title
          h2#triple-literature-evidence(
            ref="triple-literature-evidence",
            v-intersect="onIntersect"
          ) Knowledge triple and literature evidence
        v-card-text
          v-row
            v-col
              h4 Directional predicates
              p(
                v-for="(item, idx) in tripleEvidenceDocs.directional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
            v-col
              h4 Non-directional predicates
              p(
                v-for="(item, idx) in tripleEvidenceDocs.undirectional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
      v-divider.py-3
      //- # Triple and literature evidence
      v-card
        v-card-title
          h2#triple-literature-evidence(
            ref="triple-literature-evidence",
            v-intersect="onIntersect"
          ) Knowledge triple and literature evidence types
        v-card-text
          v-row
            v-col
              h4 Directional predicates
              p(
                v-for="(item, idx) in tripleEvidenceDocs.directional",
                :key="idx"
              )
                vue-markdown(:source="item", :breaks="false")
            v-col
              h4 Non-directional predicates
              p(
                v-for="(item, idx) in tripleEvidenceDocs.undirectional",
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
                  v-for="(item, idx) in assocEvidenceDocs.directional",
                  :key="idx"
                )
                  vue-markdown(:source="item", :breaks="false")
              v-col
                h4 Non-directional predicates
                p(
                  v-for="(item, idx) in assocEvidenceDocs.undirectional",
                  :key="idx"
                )
                  vue-markdown(:source="item", :breaks="false")
    // Sidebar
    v-col(cols="2")
      toc(:outline="outline", @goto="jump")
</template>

<script lang="ts">
import Vue from "vue";
import _ from "lodash";

import Toc from "@/components/widgets/Toc.vue";
import {
  makeNetworkPlotDocs,
  makeOntologyPlotDocs,
} from "@/funcs/network-plot";

import * as evidenceTypesDocs from "@/resources/docs/evidence-types";
import * as params from "@/resources/docs/params";
import * as ents from "@/resources/docs/ents";
import * as docs from "@/resources/docs/docs";
import * as docsView from "@/resources/docs/docs-view";

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
          label: "Knowledge triple and literature evidence",
          focus: false,
        },
        "assoc-evidence": {
          ref: "assoc-evidence",
          label: "Association evidence",
          focus: false,
        },
      },
      docsView: docsView,
      evidenceTypesDocs: _.chain(evidenceTypesDocs)
        .mapValues((items) => items)
        .value(),
      entsDocs: _.chain(ents)
        .mapValues((items) => items)
        .value(),
      params: _.chain(params).values().value(),
      stageDocs: _.chain([
        // be verbose
        "queryParsing",
        "tripleSelect",
        "entHarmonizationOntology",
        "evidenceSummary",
        "tripleLiteratureEvidence",
        "assocEvidence",
      ])
        .map((key) => docs[key])
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
      const baseDocs = this.evidenceTypesDocs.tripleLiteratureEvidenceTypes;
      const res = _.chain(baseDocs)
        .mapValues((items) => {
          const res = _.chain(items).values().value();
          return res;
        })
        .value();
      return res;
    },
    assocEvidenceDocs(): Record<string, Array<string>> {
      const baseDocs = this.evidenceTypesDocs.assocEvidenceTypes;
      const res = _.chain(baseDocs)
        .mapValues((items) => {
          const res = _.chain(items).values().value();
          return res;
        })
        .value();
      return res;
    },
    componentDocs(): string[] {
      const networkPlotDocs = makeNetworkPlotDocs();
      const ontologyPlotDocs = makeOntologyPlotDocs();
      const otherDocs = [docs.forestPlot];
      const res = _.chain([networkPlotDocs, ontologyPlotDocs, otherDocs])
        .flatten()
        .value();
      return res;
    },
  },
  mounted: function () {
    document.title = VIEW_TITLE;
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
