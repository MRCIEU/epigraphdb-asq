<template>
  <v-dialog v-model="showDialog" with="1080">
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-bind="attrs"
        small
        color="blue-grey"
        class="white--text"
        v-on="on"
      >
        <v-icon>mdi-comment-quote</v-icon>
        Explain
      </v-btn>
    </template>
    <v-card>
      <v-card-text>
        <vue-markdown :source="docs" :breaks="false" />
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

export default Vue.extend({
  name: "DocsDialog",
  components: {
    //
  },
  props: {
    docs: {
      type: String,
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
