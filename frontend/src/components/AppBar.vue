<template>
  <v-app-bar :id="navbarId" app dense flat>
    <v-toolbar-title>
      <tooltip :docs="`Back to the main page`" :showUnderline="false">
        <v-btn href="/" text dark>
          <span>{{ appTitle }}</span>
        </v-btn>
      </tooltip>
    </v-toolbar-title>
    <span class="px-1" />
    <tooltip :docs="`Query using a claim triple`" :showUnderline="false">
      <v-btn href="/triple" target="_blank" text dark>
        <span class="mr-2">Triple query</span>
      </v-btn>
    </tooltip>
    <tooltip :docs="`Systematic analysis results on medRxiv submissions`" :showUnderline="false">
      <v-btn href="/medrxiv-analysis" target="_blank" text dark>
        <span class="mr-2">MedRxiv analysis</span>
      </v-btn>
    </tooltip>
    <v-spacer />
    <v-btn href="https://epigraphdb.org" target="_blank" text dark>
      <!-- <span class="mr-5">EpiGraphDB</span> -->
      <img alt="" src="@/assets/epigraphdb-logo-white.png" height="35px" />
    </v-btn>
    <v-sheet color="transparent">
      <div class="py-2" />
      <a href="https://mrcieu.github.io" target="_blank">
        <img alt="" src="@/assets/MRC_IEU_Bristol_White.svg" height="59px" />
      </a>
    </v-sheet>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AppBar",
  data: () => ({
    appTitle: "Annotated Semantic Queries",
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    navbarId() {
      if (this.currentRouteName == "TripleView") {
        return "navbar-triple";
      } else {
        return "navbar";
      }
    },
  },
});
</script>

<style scoped>
#navbar {
  background-color: rgba(21, 62, 62, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
#navbar-triple {
  background-color: rgba(188, 155, 92, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
</style>
