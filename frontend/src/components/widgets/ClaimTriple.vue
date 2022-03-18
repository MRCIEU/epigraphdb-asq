<template>
  <div>
    <p>
      <!-- triple main -->
      <span class="font-weight-thin">subject:</span>
      <span class="font-weight-bold">
        {{ item.sub_term }}
      </span>
      &nbsp;
      <span class="font-weight-thin">predicate:</span>
      <a :href="umlsPredicateUrl" target="_blank">
        <span class="font-weight-bold">
          {{ item.pred }}
        </span>
      </a>
      &nbsp;
      <span class="font-weight-thin">object:</span>
      <span class="font-weight-bold">{{ item.obj_term }}</span>
      <br />
      <!-- triple info -->
      <span>
        <span class="font-weight-light">subject type:</span>
        <a :href="semanticTypeUrl" target="_blank">
          <code>{{ item.sub_type }}</code>
        </a>
        &nbsp;
        <span class="font-weight-light">predicate type:</span>
        <a :href="umlsPredicateUrl" target="_blank">
          <code>{{ item.pred_type }}</code>
        </a>
        &nbsp;
        <span class="font-weight-light">object type:</span>
        <a :href="semanticTypeUrl" target="_blank">
          <code>{{ item.obj_type }}</code>
        </a>
      </span>
      <br />
      <span>
        <span class="font-weight-light">subject confidence score:</span>
        <code>{{ item.sub_confidence_score }}</code>
        &nbsp;
        <span class="font-weight-light">object confidence score:</span>
        <code>{{ item.sub_confidence_score }}</code>
        &nbsp;
      </span>
    </p>
    <!-- context -->
    <div v-if="htmlText">
      <span class="font-weight-thin">Context:</span>
      <br />
      <p>
        <span v-html="htmlText"></span>
      </p>
    </div>
    <hr />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

import { semanticTypeUrl, umlsPredicateUrl } from "@/resources/resources";

export default Vue.extend({
  name: "ClaimTriple",
  props: {
    item: {
      type: Object,
      required: true,
    },
    htmlText: {
      type: String,
      required: false,
      default: null,
    },
  },
  data: () => ({
    semanticTypeUrl: semanticTypeUrl,
    umlsPredicateUrl: umlsPredicateUrl,
  }),
});
</script>
