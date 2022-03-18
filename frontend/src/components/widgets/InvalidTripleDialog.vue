<template lang="pug">
div
  v-dialog(v-model="showDialog", width="1080px")
    template(v-slot:activator="{ on, attrs }")
      v-btn(v-bind="attrs", x-small, color="secondary", v-on="on") Show detail
    v-card
      v-card-title Invalid triples
      v-divider
      v-card-text
        div(v-for="(item, idx) in triples", :key="idx")
          p.py-2
            b \#{{ idx }}
            | : &nbsp;
            code.font-weight-bold.body-1(style="background-color: transparent") {{ item.sub_term }} -
              | {{ item.pred }} -> {{ item.obj_term }}
            br
            v-subheader Context
            span.blockquote {{ item.text }}
          v-divider
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";
import { Triple } from "@/types/types.ts";

export default Vue.extend({
  name: "InvalidTripleDialog",
  components: {
    //
  },
  props: {
    triples: {
      type: Array as PropType<Array<Triple>>,
      required: true,
    },
  },
  data() {
    return {
      showDialog: false,
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
