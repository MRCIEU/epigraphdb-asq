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
        <tooltip :docs="$store.state.docs.params.paramSimilarityScore">
          {{ header.text }}
        </tooltip>
      </template>
      <template v-slot:item.ent_term="{ item }">
        <div>
          <span class="font-weight-thin">{{ item.meta_ent }}</span>
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
          <span class="font-weight-thin">{{ item.ref_meta_ent }}</span>
          <span v-if="refEntValid(item.ref_ent_id)">
            &nbsp;
            <code>{{ item.ref_ent_id }}</code>
          </span>
          <br />
          <span v-if="item.ref_meta_ent == 'Efo'">
            <a :href="item.ref_ent_url" target="_blank">
              <span>{{ item.ref_ent_term }}</span>
            </a>
          </span>
          <span v-else>
            <span>{{ item.ref_ent_term }}</span>
          </span>
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
import { refEntValid } from "@/funcs/utils";

export default Vue.extend({
  name: "MappingTable",
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
