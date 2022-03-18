<template>
  <div>
    <v-dialog v-model="showLiteratureDialog" width="1440px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" x-small color="info" v-on="on">Show detail</v-btn>
      </template>
      <v-card>
        <v-card-title>
          Literature detail:
          <code>{{ item.triple_label }}</code>
        </v-card-title>
        <v-card-text>
          <literature-detail
            :triple="triple"
            :num-items="item.literature_count"
          />
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

import LiteratureDetail from "@/components/widgets/LiteratureDetail.vue";
export default Vue.extend({
  name: "LiteratureDialog",
  components: {
    LiteratureDetail,
  },
  props: {
    item: {
      type: Object as PropType<Record<string, any>>,
      required: true,
    },
    triple: {
      type: Object as PropType<Record<string, any>>,
      required: true,
    },
  },
  data() {
    return {
      showLiteratureDialog: false,
    };
  },
  computed: {
    //
  },
  methods: {
    //
  },
});
</script>
