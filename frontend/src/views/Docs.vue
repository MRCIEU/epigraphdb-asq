<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>
            <h2 id="about" ref="about" v-intersect="onIntersect">About</h2>
          </v-card-title>
        </v-card>
        <v-divider class="py-3" />
        <v-card>
          <v-card-title>
            <h2 id="terminology" ref="terminology" v-intersect="onIntersect">
              Terminology
            </h2>
          </v-card-title>
        </v-card>
        <v-divider class="py-3" />
        <v-row>
          <v-col>
            <v-card>
              <v-card-title>
                <h2 id="ents" ref="ents" v-intersect="onIntersect">Entities</h2>
              </v-card-title>
              <v-card-text>
                <p v-for="(item, idx) in entsDocs" :key="idx">
                  <vue-markdown :source="item" :breaks="false" />
                </p>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card>
              <v-card-title>
                <h2 id="params" ref="params" v-intersect="onIntersect">
                  Parameters
                </h2>
              </v-card-title>
              <v-card-text>
                <p v-for="(item, idx) in params" :key="idx">
                  <vue-markdown :source="item" :breaks="false" />
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-divider class="py-3" />
        <v-row>
          <v-col>
            <v-card>
              <v-card-title>
                <h2 id="stages" ref="stages" v-intersect="onIntersect">
                  Query stages
                </h2>
              </v-card-title>
              <v-card-text>
                <p v-for="(item, idx) in stageDocs" :key="idx">
                  <vue-markdown :source="item" :breaks="false" />
                </p>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card>
              <v-card-title>
                <h2 id="components" ref="components" v-intersect="onIntersect">
                  Components
                </h2>
              </v-card-title>
              <v-card-text>
                <p v-for="(item, idx) in componentDocs" :key="idx">
                  <vue-markdown :source="item" :breaks="false" />
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-divider class="py-3" />
        <v-card>
          <v-card-title>
            <h2 ref="evidence">Evidence</h2>
          </v-card-title>
          <v-divider class="py-3" />
          <v-card>
            <v-card-title>
              <h3
                id="triple-literature-evidence"
                ref="triple-literature-evidence"
                v-intersect="onIntersect"
              >
                Knowledge triple and literature evidence
              </h3>
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col>
                  <h4>Directional</h4>
                  <p
                    v-for="(item, idx) in tripleEvidenceDocs.directional"
                    :key="idx"
                  >
                    <vue-markdown :source="item" :breaks="false" />
                  </p>
                </v-col>
                <v-col>
                  <h4>Undirectional</h4>
                  <p
                    v-for="(item, idx) in tripleEvidenceDocs.undirectional"
                    :key="idx"
                  >
                    <vue-markdown :source="item" :breaks="false" />
                  </p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-divider class="py-3" />
          <v-card>
            <v-card-title>
              <h3
                id="assoc-evidence"
                ref="assoc-evidence"
                v-intersect="onIntersect"
              >
                Association evidence
              </h3>
            </v-card-title>
            <v-card-text>
              <v-row>
                <v-col>
                  <h4>Directional</h4>
                  <p
                    v-for="(item, idx) in assocEvidenceDocs.directional"
                    :key="idx"
                  >
                    <vue-markdown :source="item" :breaks="false" />
                  </p>
                </v-col>
                <v-col>
                  <h4>Undirectional</h4>
                  <p
                    v-for="(item, idx) in assocEvidenceDocs.undirectional"
                    :key="idx"
                  >
                    <vue-markdown :source="item" :breaks="false" />
                  </p>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
      <v-col cols="2">
        <toc :outline="outline" @goto="jump" />
      </v-col>
    </v-row>
  </v-container>
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
