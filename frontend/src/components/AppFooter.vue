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
        <v-btn x-small tile text dark href="/docs" target="_blank">
          <span>Docs</span>
          <v-icon>mdi-file-search</v-icon>
        </v-btn>
        <v-btn x-small tile text dark href="#" target="_blank">
          <span>Feedback</span>
          <v-icon>mdi-comment-quote</v-icon>
        </v-btn>
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