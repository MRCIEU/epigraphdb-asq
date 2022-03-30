<template>
  <div>
    <v-row>
      <v-col>
        <v-btn
          small
          tile
          color="secondary"
          dark
          @click="toggleFullscreen('#vis-network-plot')"
        >
          Fullscreen
        </v-btn>
        <docs-dialog :docs="networkPlotDocs" />
      </v-col>
      <v-col>
        <v-switch
          v-model="filterEmpty"
          label="Remove entities that don't associate with evidence results"
        />
      </v-col>
    </v-row>
    <div v-if="!showPlot">
      <div class="py-5" />
      <div class="py-5" />
      <div class="d-flex justify-center py-5">
        <p>Network graph too large. Rendering is disabled.</p>
      </div>
      <div class="d-flex justify-center py-5">
        <v-btn color="error" @click="showPlot = !showPlot">
          Render the plot!
        </v-btn>
      </div>
    </div>
    <div v-else>
      <network
        v-if="plotData"
        id="vis-network-plot"
        :nodes="nodes"
        :edges="edges"
        :options="options"
        class="vis-network-plot"
        @double-click="clickUrl"
      />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import { Network } from "vue-vis-network";
import { makeNetworkPlotData } from "@/funcs/network-plot";

import DocsDialog from "@/components/widgets/DocsDialog.vue";

export default Vue.extend({
  name: "NetworkPlot",
  components: {
    Network,
    DocsDialog,
  },
  data() {
    return {
      plotData: null,
      showPlot: true,
      filterEmpty: true,
      networkPlotDocs: this.$store.state.docs.plots.networkPlot,
    };
  },
  computed: {
    nodes(): null | Record<string, any> {
      return this.plotData ? this.plotData.nodes : null;
    },
    edges(): null | Record<string, any> {
      return this.plotData ? this.plotData.edges : null;
    },
    graphTooLarge(): boolean {
      if (this.edges == null) return false;
      const threshold = 300;
      if (this.edges.length > threshold) return true;
      return false;
    },
    options(): Record<string, any> {
      const res = {
        nodes: {
          shape: "box",
        },
        physics: {
          barnesHut: {
            gravitationalConstant: -2000,
            avoidOverlap: 0.5,
            damping: 0.9,
          },
        },
        layout: {
          improvedLayout: true,
        },
      };
      return res;
    },
  },
  watch: {
    async filterEmpty(newVal) {
      this.plotData = await makeNetworkPlotData(newVal);
    },
  },
  mounted() {
    this.refresh();
  },
  methods: {
    async refresh() {
      this.plotData = await makeNetworkPlotData(this.filterEmpty);
      if (this.graphTooLarge) {
        this.showPlot = false;
      } else {
        this.showPlot = true;
      }
    },
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
    clickUrl(params): void {
      if (params.nodes.length === 1) {
        const node = this._.find(this.nodes, { id: params.nodes[0] });
        if (node.url) {
          window.open(node.url, "_blank");
        }
      }
    },
  },
});
</script>

<style scoped>
.vis-network-plot {
  height: 70rem;
  background-color: #ffffff;
}
</style>
