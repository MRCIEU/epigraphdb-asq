<template lang="pug">
div
  v-dialog(v-model="showLiteratureDialog", width="1080px")
    template(v-slot:activator="{ on, attrs }")
      v-btn(v-bind="attrs", x-small, color="info", v-on="on") Show detail
    v-card
      v-card-title Literature detail: #[code {{ triple }}]
      v-divider
      v-card-text
        .py-3(v-for="(e, idx) in literatureData", :key="idx")
          b \#{{ idx }}: &nbsp;
          span.font-weight-thin {{ e.doi }}
          br
          a(:href="e.url", target="_blank") {{ e.title }}
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

export default Vue.extend({
  name: "AnalysisLiteratureSource",
  components: {
    //
  },
  props: {
    sourceData: {
      type: Array as PropType<Array<{ doi: string; title: string }>>,
      required: true,
    },
    triple: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showLiteratureDialog: false,
    };
  },
  computed: {
    literatureData(): Array<{ doi: string; title: string; url: string }> {
      const res = this._.chain(this.sourceData)
        .map((e) => ({
          ...e,
          url: `https://doi.org/${e.doi}`,
        }))
        .value();
      return res;
    },
  },
  methods: {
    //
  },
});
</script>
