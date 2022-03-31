<template>
  <v-container>
    <v-row justify="center">
      <v-expansion-panels v-model="panels" flat multiple>
        <!-- query -->
        <v-expansion-panel>
          <v-expansion-panel-header>
            <h1>{{ queryHeader }}</h1>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <stage-stepper />
          </v-expansion-panel-content>
        </v-expansion-panel>
        <!-- query -->
        <!-- results -->
        <v-expansion-panel :disabled="resultPanelDisabled">
          <v-expansion-panel-header>
            <h1>{{ resultsHeader }}</h1>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-lazy v-model="queryAllDone">
              <results />
            </v-lazy>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <!-- results -->
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";
import StageStepper from "@/components/StageStepper.vue";
import Results from "@/components/Results.vue";

export default Vue.extend({
  name: "Home",
  components: {
    StageStepper,
    Results,
  },
  data() {
    return {
      panels: [0],
      resultPanelDisabled: true,
    };
  },
  computed: {
    queryAllDone(): boolean {
      const res = this.$store.getters["queryStage/queryAllDone"];
      return res;
    },
    queryHeader(): string {
      if (this.queryAllDone) {
        return "Claim query (complete)";
      } else {
        return "Claim query";
      }
    },
    resultsHeader(): string {
      if (this.queryAllDone) {
        return "Evidence results";
      } else {
        // return "Evidence results (inactive)";
        return "";
      }
    },
  },
  watch: {
    queryAllDone(newVal) {
      if (newVal) {
        this.panels = [1];
        this.resultPanelDisabled = false;
      }
    },
  },
  mounted: async function (): Promise<void> {
    await this.$store.dispatch("queryStage/setQueryMode", "standard");
  },
  methods: {
    //
  },
});
</script>
