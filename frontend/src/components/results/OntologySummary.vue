<template>
  <div>
    <v-row>
      <v-col>
        <h3>Subject mapping</h3>
        <efo-mapping-table :data="ontologyMappingData.subjects" />
      </v-col>
      <v-col>
        <h3>Object mapping</h3>
        <efo-mapping-table :data="ontologyMappingData.objects" />
      </v-col>
    </v-row>
    <div v-if="ontologyPlotData" class="py-5">
      <h3>Mapping details</h3>
      <v-tabs v-model="tabs" show-arrows>
        <v-tab v-for="(item, idx) in ontologyEnts" :key="idx">
          <span class="font-weight-light">EFO:</span>
          {{ item.ent_term }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tabs" vertical>
        <v-tab-item v-for="(item, idx) in ontologyEnts" :key="idx">
          <v-row class="py-2">
            <v-col cols="5">
              <h4>EFO Ontology diagram</h4>
              <ontology-plot :data="ontologyPlotData[item.ent_id].efo_data" />
            </v-col>
            <v-col cols="7">
              <h4>Semantic similarity scores</h4>
              <ontology-diagram-mapping-table
                :data="ontologyPlotData[item.ent_id].similarity_scores"
              />
            </v-col>
          </v-row>
        </v-tab-item>
      </v-tabs-items>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

import EfoMappingTable from "@/components/widgets/EfoMappingTable.vue";
import OntologyDiagramMappingTable from "@/components/widgets/OntologyDiagramMappingTable.vue";
import OntologyPlot from "@/components/widgets/OntologyPlot.vue";
import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

export default Vue.extend({
  name: "OntologySummary",
  components: {
    EfoMappingTable,
    OntologyDiagramMappingTable,
    OntologyPlot,
  },
  props: {
    ontologyMappingData: {
      type: Object as PropType<Record<string, Array<any>>>,
      required: true,
    },
  },
  data() {
    return {
      ontologyDiagramSelect: null,
      ontologyPlotData: null,
      tabs: null,
    };
  },
  computed: {
    ontologyEnts(): Array<types.BaseEnt> {
      const res = this._.chain(this.$store.getters["ents/ontologyData"])
        .mapValues((item) => item.ents)
        .values()
        .flatten()
        .uniqWith(this._.isEqual)
        .map((item) => ({
          ent_id: item.ent_id,
          ent_term: item.ent_term,
        }))
        .value();
      console.log(res);
      return res;
    },
  },
  mounted: async function (): Promise<void> {
    const queryTerms = [
      this.$store.state.ents.claimTriple.sub_term,
      this.$store.state.ents.claimTriple.obj_term,
    ];
    this.ontologyPlotData = await processing.makeOntologyPlotData(
      this.ontologyEnts,
      queryTerms,
    );
  },
  methods: {
    //
  },
});
</script>
