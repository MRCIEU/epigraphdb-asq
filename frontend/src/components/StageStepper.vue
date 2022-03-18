<template>
  <v-stepper v-model="stage" flat non-linear>
    <v-stepper-header>
      <v-stepper-step :step="1" editable :complete="stage > 1">
        {{ stepTitles["stage1"] }}
      </v-stepper-step>
      <v-divider />
      <v-stepper-step :step="2" editable :complete="stage > 2">
        {{ stepTitles["stage2"] }}
      </v-stepper-step>
      <v-divider />
      <v-stepper-step :step="3" editable :complete="stage > 3">
        {{ stepTitles["stage3"] }}
      </v-stepper-step>
    </v-stepper-header>
    <v-stepper-items>
      <v-stepper-content :step="1">
        <query-claim :stage="1" />
      </v-stepper-content>

      <v-stepper-content :step="2">
        <triple-select :stage="2" />
      </v-stepper-content>

      <v-stepper-content :step="3">
        <ent-harmonization-ontology :stage="3" />
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</template>

<script lang="ts">
import Vue from "vue";

import QueryClaim from "@/components/stages/QueryClaim.vue";
import TripleSelect from "@/components/stages/TripleSelect.vue";
import EntHarmonizationOntology from "@/components/stages/EntHarmonizationOntology.vue";

export default Vue.extend({
  name: "StageStepper",
  components: {
    QueryClaim,
    TripleSelect,
    EntHarmonizationOntology,
  },
  data: () => ({
    stepTitles: {
      stage1: "Insert query text",
      stage2: "Select a claim triple",
      stage3: "Entity harmonization in ontology",
    },
  }),
  computed: {
    stage: {
      get() {
        return this.$store.state.queryStage.currentStage;
      },
      set(value: number) {
        this.$store.dispatch("queryStage/setCurrentStage", value);
      },
    },
  },
  methods: {},
});
</script>
