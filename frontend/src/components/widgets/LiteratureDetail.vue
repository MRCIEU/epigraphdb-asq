<template>
  <div>
    <loading v-if="loading" :message="loadingMessage" />
    <v-row v-if="!loading">
      <v-col v-if="literatureItems !== null">
        <v-data-table :headers="literatureHeaders" :items="literatureItems">
          <template v-slot:item.title="{ item }">
            <div>
              <span class="font-weight-thin">DOI: {{ item.doi }}</span>
              <br />
              <span>{{ item.title }}</span>
              <!-- <a :href="item.url" target="_blank">
                   <span>{{ item.title }}</span>
                   </a> -->
            </div>
          </template>
        </v-data-table>
      </v-col>
      <v-col>
        <div v-if="literatureHtml !== null && literatureHtml.length > 0">
          <v-btn
            small
            tile
            color="secondary"
            dark
            @click="toggleFullscreen('#literature-context')"
          >
            Fullscreen
          </v-btn>
          <div id="literature-context" class="literature-context">
            <div v-for="item in literatureHtml" :key="item.idx">
              <literature-context
                :data="literatureItems[item.idx]"
                :html-text="item"
              />
            </div>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";

import * as types from "@/types/types";
import * as backendRequests from "@/funcs/backend_requests";
import LiteratureContext from "@/components/widgets/LiteratureContext.vue";
import Loading from "@/components/widgets/Loading.vue";

export default Vue.extend({
  name: "LiteratureDetail",
  components: {
    LiteratureContext,
    Loading,
  },
  props: {
    triple: {
      type: Object as PropType<types.TripleItemRequest>,
      required: true,
    },
    numItems: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      literatureHeaders: [
        {
          text: "#",
          value: "idx",
        },
        {
          text: "Article",
          value: "title",
        },
        {
          text: "Year",
          value: "year",
        },
      ],
      loading: false,
      loadingMessage: "Literature data",
      literatureEvidence: null,
      literatureItems: null,
      literatureHtml: null,
    };
  },
  computed: {
    //
  },
  watch: {
    async triple(newVal, oldVal) {
      if (newVal != oldVal) {
        await this.updateData();
      }
    },
  },
  mounted: async function () {
    await this.updateData();
  },
  methods: {
    async updateData(): Promise<void> {
      this.loading = true;
      await this.getLiteratureEvidence();
      this.loading = false;
    },
    async getLiteratureEvidence(): Promise<void> {
      this.literatureEvidence = await backendRequests.requestLiteratureEvidence(
        this.triple,
        this.numItems,
      );
      this.literatureItems = this._.chain(this.literatureEvidence.data)
        .map((item, idx) => ({ ...item, idx: idx }))
        .value();
      this.literatureHtml = this.literatureEvidence.html_text;
    },
    toggleFullscreen(elemId) {
      const elem = this.$el.querySelector(elemId);
      this.$fullscreen.toggle(elem);
    },
  },
});
</script>

<style scoped>
.literature-context {
  max-height: 1000px;
  overflow-y: scroll;
  background-color: #ffffff;
}
</style>
