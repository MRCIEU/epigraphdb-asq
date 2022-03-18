<template>
  <div>
    <p>
      <!-- info -->
      <span>#{{ htmlText.idx }}:</span>
      &nbsp;
      <span class="font-weight-thin">PubMed ID:</span>
      &nbsp;
      <code>
        {{ data.pubmed_id }}
      </code>
      &nbsp;
      <span class="font-weight-thin">DOI:</span>
      &nbsp;
      <a :href="formatUrl(data.doi)" target="_blank">
        <code>
          {{ data.doi }}
        </code>
      </a>
      <span class="font-weight-thin">Year:</span>
      &nbsp;
      <code>
        {{ data.year }}
      </code>
      <br />
      <!-- title -->
      <span class="font-weight-thin">Title:</span>
      &nbsp;
      <span v-html="htmlText.title_text"></span>
      <br />
      <!-- sentence -->
      <span class="font-weight-thin">Context sentence:</span>
      &nbsp;
      <b><span v-html="htmlText.sentence"></span></b>
      <br />
      <!-- text -->
      <span class="font-weight-thin">Abstract:</span>
      &nbsp;
      <span v-html="htmlText.abstract"></span>
    </p>

    <hr />
    <p />
  </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "LiteratureContext",
  props: {
    data: {
      type: Object,
      required: true,
    },
    htmlText: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatUrl(doi): string {
      return `https://doi.org/${doi}`;
    },
  },
});
</script>
