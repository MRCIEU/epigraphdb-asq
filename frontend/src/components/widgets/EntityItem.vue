<template>
  <div>
    <span>
      <span class="font-weight-thin">
        <span>
          EpiGraphDB
          <code>({{ entType }})</code>
        </span>
        &nbsp;
      </span>
      <span class="font-weight-thin">id: &nbsp;</span>
      <a :href="item.url" target="_blank" @click.stop>
        <span class="font-weight-bold">
          {{ item.ent_id }}
        </span>
      </a>
    </span>
    <br />
    <br />
    <v-row>
      <v-col>
        <span>
          <span class="font-weight-thin">term: &nbsp;</span>
          <span class="font-weight-bold">
            {{ item.ent_term }}
          </span>
        </span>
      </v-col>
      <v-col>
        <span v-if="item.similarity_score">
          <v-tooltip bottom max-width="400px">
            <template v-slot:activator="{ on, attrs }">
              <span class="font-weight-thin" v-bind="attrs" v-on="on">
                similarity_score: &nbsp;
              </span>
            </template>
            <vue-markdown :source="paramSimilarityScore" :breaks="false" />
          </v-tooltip>
          <code>
            {{ Number(item.similarity_score).toFixed(2) }}
          </code>
        </span>
        <span v-if="item.identity_score">
          <br />
          <v-tooltip bottom max-width="400px">
            <template v-slot:activator="{ on, attrs }">
              <span class="font-weight-thin" v-bind="attrs" v-on="on">
                identity_score: &nbsp;
              </span>
            </template>
            <vue-markdown :source="paramIdentityScore" :breaks="false" />
          </v-tooltip>
          <code>
            {{ Number(item.identity_score).toFixed(2) }}
          </code>
        </span>
        <span v-if="item.ic_score">
          <br />
          <v-tooltip bottom max-width="400px">
            <template v-slot:activator="{ on, attrs }">
              <span class="font-weight-thin" v-bind="attrs" v-on="on">
                ic_score: &nbsp;
              </span>
            </template>
            <vue-markdown :source="paramIcScore" :breaks="false" />
          </v-tooltip>
          <code>
            {{ Number(item.ic_score).toFixed(2) }}
          </code>
        </span>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import {
  paramSimilarityScore,
  paramIcScore,
  paramIdentityScore,
} from "@/resources/docs/params";

export default Vue.extend({
  name: "EntityItem",
  components: {
    //
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    entType: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      paramIcScore: paramIcScore,
      paramSimilarityScore: paramSimilarityScore,
      paramIdentityScore: paramIdentityScore,
    };
  },
});
</script>
