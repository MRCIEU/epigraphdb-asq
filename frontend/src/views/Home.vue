<template>
  <v-container>
    <v-row justify="center">
      <div v-if="showLogo" class="text-center">
        <div class="py-5" />
        <img alt="" src="@/assets/ASQ_logo_draft_highres.png" height="120rem" />
        <p class="text-subtitle-1 grey--text">
          A natural language query interface to
          <a href="https://epigraphdb.org" target="_blank">EpiGraphDB</a>
          evidence
        </p>
        <p class="text-subtitle-1">
          <v-tooltip v-model="showDocsTooltip" bottom color="success">
            <template v-slot:activator="{ on, attrs }">
              <a href="/docs" class="px-3" v-bind="attrs" v-on="on">
                Documentation
              </a>
            </template>
            <span>Read documentation here</span>
          </v-tooltip>
          |
          <a href="/triple" class="px-3">Triple query</a>
          |
          <a href="/medrxiv-analysis" class="px-3">
            Systematic analysis results
          </a>
          <br />
          <br />
          <a href="https://forms.office.com/e/nM71WCid3g" class="px-3">
            (NEW) User experience survey
          </a>
        </p>
      </div>
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
      showDocsTooltip: true,
    };
  },
  computed: {
    queryAllDone(): boolean {
      const res = this.$store.getters["queryStage/queryAllDone"];
      return res;
    },
    showLogo(): boolean {
      const res = this.$store.state.queryStage.latestStage == 1;
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
    this.timeoutTooltip();
    await this.$store.dispatch("queryStage/setQueryMode", "standard");
  },
  methods: {
    timeoutTooltip(): void {
      setTimeout(
        function () {
          if (this.showDocsTooltip) {
            this.showDocsTooltip = false;
          }
        }.bind(this),
        3000,
      );
    },
  },
});
</script>
