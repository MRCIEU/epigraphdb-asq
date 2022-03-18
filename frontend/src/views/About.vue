<template>
  <div class="about">
    <h1>This is an about page</h1>
    <p>Backend status: {{ backend_status }}</p>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";

import { web_backend_url } from "@/config.ts";

export default Vue.extend({
  name: "About",
  data: () => ({
    backend_status: null,
  }),
  mounted: function () {
    this.checkBackendStatus();
  },
  methods: {
    async checkBackendStatus() {
      const url = `${web_backend_url}/ping`;
      const params = {
        dependencies: false,
      };
      this.backend_status = await axios
        .get(url, { params: params })
        .then((r) => {
          return r.data;
        });
    },
  },
});
</script>
