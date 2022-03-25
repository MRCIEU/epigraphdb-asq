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
          <tooltip :docs="paramSimilarityScore">
            <span class="font-weight-thin">similarity_score: &nbsp;</span>
          </tooltip>
          <code>
            {{ Number(item.similarity_score).toFixed(2) }}
          </code>
        </span>
        <span v-if="item.identity_score">
          <br />
          <tooltip :docs="paramIdentityScore">
            <span class="font-weight-thin">identity_score: &nbsp;</span>
          </tooltip>
          <code>
            {{ Number(item.identity_score).toFixed(2) }}
          </code>
        </span>
        <span v-if="item.ic_score">
          <br />
          <tooltip :docs="paramIcScore">
            <span class="font-weight-thin">ic_score: &nbsp;</span>
          </tooltip>
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

import Tooltip from "@/components/widgets/Tooltip.vue";

import {
  paramSimilarityScore,
  paramIcScore,
  paramIdentityScore,
} from "@/resources/docs/params";

export default Vue.extend({
  name: "EntityItem",
  components: {
    Tooltip,
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
