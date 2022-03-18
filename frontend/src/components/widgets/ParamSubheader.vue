<template>
  <div>
    <v-subheader>
      <v-tooltip bottom max-width="400px">
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on">
            {{ label }}
          </span>
        </template>
        <p>
          <vue-markdown :breaks="false" :source="docs" />
        </p>
      </v-tooltip>
    </v-subheader>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "ParamSubheader",
  components: {
    //
  },
  props: {
    docs: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      //
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
