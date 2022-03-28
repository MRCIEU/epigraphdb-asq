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
      <template v-slot:header.ic_score="{ header }">
        <tooltip :docs="docsParams.paramIcScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.identity_score="{ header }">
        <tooltip :docs="docsParams.paramIdentityScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:header.similarity_score="{ header }">
        <tooltip :docs="docsParams.paramSimilarityScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:item.ent_term="{ item }">
        <div>
          <span class="font-weight-thin">Efo</span>
          &nbsp;
          <span>
            <code>{{ item.ent_id }}</code>
          </span>
          <br />
          <a :href="item.ent_url" target="_blank">
            <span>{{ item.ent_term }}</span>
          </a>
        </div>
      </template>
      <template v-slot:item.ref_ent_term="{ item }">
        <div>
          <span class="font-weight-thin">QueryUmls</span>
          <span v-if="refEntValid(item.ref_ent_id)">
            &nbsp;
            <code>{{ item.ref_ent_id }}</code>
          </span>
          <br />
          <span>{{ item.ref_ent_term }}</span>
        </div>
      </template>
      <template v-slot:item.similarity_score="{ item }">
        <div>
          {{ item.similarity_score.toFixed(2) }}
        </div>
      </template>
      <template v-slot:item.ic_score="{ item }">
        <div>
          {{ item.ic_score.toFixed(2) }}
        </div>
      </template>
      <template v-slot:item.identity_score="{ item }">
        <div>
          {{ item.identity_score.toFixed(2) }}
        </div>
      </template>
    </v-data-table>
  </v-card>
</template>

<script lang="ts">
import Vue from "vue";
import { refEntValid } from "@/funcs/utils";
import * as docsParams from "@/resources/docs/params";

export default Vue.extend({
  name: "EfoMappingTable",
  components: {
    //
  },
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      search: "",
      docsParams: docsParams,
      headers: [
        {
          text: "Entity",
          value: "ent_term",
        },
        {
          text: "Reference entity",
          value: "ref_ent_term",
        },
        {
          text: "Information content score",
          value: "ic_score",
        },
        {
          text: "Identity score",
          value: "identity_score",
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
      return this.data;
    },
  },
  methods: {
    refEntValid(item: string | null): boolean {
      return refEntValid(item);
    },
  },
});
</script>
