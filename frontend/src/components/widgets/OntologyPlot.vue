<template>
  <div v-if="plotData">
    <div>
      <v-btn
        small
        tile
        color="secondary"
        dark
        @click="toggleFullscreen('#vis-network-plot')"
      >
        Fullscreen
      </v-btn>
      <docs-dialog :docs="ontologyPlotDocs" />
    </div>
    <network
      v-if="plotData"
      id="vis-network-plot"
      :nodes="plotData.nodes"
      :edges="plotData.edges"
      :options="options"
      class="vis-network-plot"
      @double-click="clickUrl"
    />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

import { Network } from "vue-vis-network";

import * as types from "@/types/types";
import { makeOntologyPlotData } from "@/funcs/network-plot";
import DocsDialog from "@/components/widgets/DocsDialog.vue";

export default Vue.extend({
  name: "OntologyPlot",
  components: {
    Network,
    DocsDialog,
  },
  props: {
    data: {
      type: Array as PropType<Array<types.EfoDataItem>>,
      required: true,
    },
  },
  data() {
    return {
      plotData: null,
      ontologyPlotDocs: null,
    };
  },
  computed: {
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
          hierarchical: {
            direction: "UD",
            enabled: true,
            sortMethod: "directed",
          },
        },
      };
      return res;
    },
  },
  watch: {
    data(val) {
      if (val) {
        this.refresh();
      }
    },
  },
  async mounted() {
    this.ontologyPlotDocs = this.$store.state.docs.plots.ontologyPlot;
    await this.refresh();
  },
  methods: {
    async refresh() {
      this.plotData = await makeOntologyPlotData(this.data);
    },
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
    clickUrl(params): void {
      if (params.nodes.length === 1) {
        const node = this._.find(this.plotData.nodes, { id: params.nodes[0] });
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
  height: 40rem;
  background-color: #ffffff;
}
</style>
