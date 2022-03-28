<template>
  <div>
    <v-dialog v-model="showDialog" width="1440">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          outlined
          class="floating-button"
          color="error"
          @click="showDialog = !showDialog"
          v-on="on"
        >
          <v-icon>mdi-border-outside</v-icon>
          Adjust query
        </v-btn>
      </template>
      <v-card>
        <v-card-title>Adjust query</v-card-title>
        <loading v-if="loading" :message="loadingMessage" />
        <v-stepper v-model="stage" vertical>
          <v-row>
            <v-col cols="2">
              <v-stepper-step :step="1" editable :complete="stage > 1">
                Query parameters
              </v-stepper-step>
              <v-divider />
              <v-stepper-step :step="2" editable :complete="stage > 2">
                Entity harmonization
              </v-stepper-step>
            </v-col>
            <v-col>
              <v-stepper-items>
                <v-stepper-content :step="1">
                  <adjust-results-params @regen="updateEnts" />
                </v-stepper-content>
                <v-stepper-content :step="2">
                  <adjust-ontology-ents
                    :key="refresh"
                    @regen="updateEvidence"
                  />
                </v-stepper-content>
              </v-stepper-items>
            </v-col>
          </v-row>
        </v-stepper>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import AdjustResultsParams from "./AdjustResultsParams.vue";
import AdjustOntologyEnts from "./AdjustOntologyEnts.vue";
import Loading from "@/components/widgets/Loading.vue";

import * as processing from "@/funcs/processing";

export default Vue.extend({
  name: "AdjustResults",
  components: {
    AdjustResultsParams,
    AdjustOntologyEnts,
    Loading,
  },
  data() {
    return {
      showDialog: false,
      stage: 1,
      refresh: 0,
      loading: false,
      loadingMessage: "",
    };
  },
  computed: {
    //
  },
  methods: {
    async updateEnts(): Promise<void> {
      this.stage = 2;
      this.loading = true;
      this.loadingMessage = "Retrieving ontology entities";
      await this.refreshOntologyEnts();
      this.refresh = this.refresh + 1;
      this.loading = false;
    },
    async refreshOntologyEnts(): Promise<void> {
      const triple = this.$store.state.ents.claimTriple;
      await processing.getOntologyEnts(triple);
    },
    async updateEvidence(): Promise<void> {
      this.showDialog = false;
      await this.$emit("regen");
    },
  },
});
</script>

<style scoped>
.floating-button {
  position: fixed;
  right: 150px;
  bottom: 40px;
  z-index: 120;
}
</style>
