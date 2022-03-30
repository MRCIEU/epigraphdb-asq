<template>
  <div>
    <div v-if="!hide">
      <v-footer :id="footerId" padless fixed>
        <v-btn x-small tile text dark @click="hide = true">
          <v-icon>mdi-minus</v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <div v-if="!queryFinished">
          <span class="blink" v-html="action"></span>
        </div>
        <div v-else>
          <span v-html="action"></span>
        </div>
        <span v-if="queryTriple" v-html="queryTriple"></span>
        <v-spacer></v-spacer>
        <v-tooltip v-model="showDocsTooltip" top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small tile text dark href="/docs" target="_blank">
              <div class="pt-1">
                <span v-bind="attrs" v-on="on">Docs</span>
              </div>
            </v-btn>
          </template>
          <span>Read documentation here</span>
        </v-tooltip>
        <tooltip :show-underline="false" :docs="'Github'" :position="'top'">
          <v-btn
            x-small
            tile
            text
            dark
            href="https://github.com/mrcieu/epigraphdb-asq"
            target="_blank"
          >
            <span>Code</span>
          </v-btn>
        </tooltip>
        <tooltip
          :show-underline="false"
          :docs="`Example on how to query the API programmatically`"
          :position="'top'"
        >
          <v-btn x-small tile text dark href="#" target="_blank">
            <span>Programmatic query</span>
          </v-btn>
        </tooltip>
        <tooltip
          :show-underline="false"
          :docs="`Feedbacks or queries welcome!`"
          :position="'top'"
        >
          <v-btn
            x-small
            tile
            text
            dark
            href="https://github.com/mrcieu/epigraphdb-asq/issues"
            target="_blank"
          >
            <span>Feedback</span>
          </v-btn>
        </tooltip>
      </v-footer>
    </div>
    <div v-else>
      <div class="footer-btn">
        <v-btn x-small depressed @click="hide = false">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AppFooter",
  data: () => ({
    hide: false,
    showDocsTooltip: true,
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    footerId() {
      if (this.currentRouteName == "TripleView") {
        return "footer-triple";
      } else {
        return "footer";
      }
    },
    queryFinished(): boolean {
      return this.$store.getters["queryStage/queryAllDone"];
    },
    queryTriple(): string | null {
      const latestStage = this.$store.state.queryStage.latestStage;
      const nonStandard = !this.$store.state.queryStage.standardQueryMode;
      const stageReached = !nonStandard ? latestStage > 2 : latestStage > 1;
      if (!stageReached) {
        return null;
      } else {
        const queryTriple = this.$store.state.ents.claimTriple;
        const queryTripleLabel = `<code style="color:#ffd740">${queryTriple.sub_term}-${queryTriple.pred}->${queryTriple.obj_term}</code>`;
        const res = ` &nbsp;  &nbsp; query triple: ${queryTripleLabel}`;
        return res;
      }
    },
    action(): string {
      const res = this.$store.getters["queryStage/stageAction"];
      return res;
    },
  },
  mounted: function () {
    this.timeoutTooltip();
  },
  methods: {
    timeoutTooltip(): void {
      setTimeout(
        function () {
          if (this.showDocsTooltip) {
            this.showDocsTooltip = false;
          }
        }.bind(this),
        5000,
      );
    },
  },
});
</script>

<style scoped>
.footer-btn {
  position: fixed;
  left: 0;
  bottom: 0;
}

#footer {
  background-color: rgba(21, 62, 62, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
#footer-triple {
  background-color: rgba(188, 155, 92, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
.blink {
  animation: blinker 6s linear infinite;
}
@keyframes blinker {
  50% {
    opacity: 0.4;
  }
}
</style>
