<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      />
    </v-card-title>
    <v-data-table :headers="headers" :items="items" :search="search">
      <template v-slot:header.similarity_score="{ header }">
        <tooltip :docs="docsParams.paramSimilarityScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:item.source_ent_term="{ item }">
        <div>
          <span class="font-weight-thin">Efo</span>
          &nbsp;
          <span>
            <code>{{ item.source_ent_id }}</code>
          </span>
          <br />
          <a :href="item.ent_url" target="_blank">
            <span>{{ item.source_ent_term }}</span>
          </a>
        </div>
      </template>
      <template v-slot:item.similarity_score="{ item }">
        <div>
          {{ item.similarity_score.toFixed(2) }}
        </div>
      </template>
    </v-data-table>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";
import * as docsScores from "@/resources/docs/scores";

export default Vue.extend({
  name: "OntologyDiagramMappingTable",
  components: {
    //
  },
  props: {
    data: {
      type: Array as PropType<Array<any>>,
      required: true,
    },
  },
  data() {
    return {
      docsScores: docsScores,
      search: "",
      headers: [
        {
          text: "Ontology entity",
          value: "source_ent_term",
        },
        {
          text: "Query term",
          value: "target_ent_term",
        },
        {
          text: "Semantic similarity",
          value: "similarity_score",
        },
      ],
    };
  },
  computed: {
    items(): Array<any> {
      return this._.chain(this.data)
        .map((item) => ({
          ...item,
          ent_url: `https://epigraphdb.org/entity?meta_node=Efo&id=${item.source_ent_id}`,
        }))
        .value();
    },
  },
  methods: {
    //
  },
});
</script>
