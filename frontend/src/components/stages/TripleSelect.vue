<template lang="pug">
v-container
  v-row(justify="space-between")
    v-col(cols=6)
      h2 {{ title }}
      p.blockquote
        vue-markdown(:breaks="false", :source="pageDocs")
    v-spacer
    v-col
      .py-3.d-flex.justify-end
      v-btn.confirm-btn(
        v-if="$store.state.queryStage.currentStage == stage && active",
        color="primary",
        large,
        :disabled="buttonDisabled",
        @click="update"
      )
        v-progress-circular(v-if="loading", indeterminate, color="grey")
        span {{ btnLabel }}
  div(v-if="!active")
    v-alert(:type="tripleResultsEmpty ? 'error' : 'info'") {{ inactiveMessage }}
    div(v-if="$store.state.queryStage.latestStage >= stage")
      v-subheader Invalid claim triples
      p
        | There are #[b {{ invalidTriples.length }}] &nbsp;
        tooltip(:docs="$store.state.docs.ents.invalidTriple") invalid triples
        | &nbsp; generated from the claim text. &nbsp;
        invalid-triple-dialog(:triples="invalidTriples")
      v-subheader Valid claim triples
      p
        | There are no &nbsp;
        tooltip(:docs="$store.state.docs.ents.validTriple") valid triples
        | &nbsp; generated from the claim text.
  div(v-else)
    v-row
      v-col(cols="4")
        h3 Original claim text
        claim-text-display(v-if="claimText", :sents="claimText")
      v-col(cols="8")
        h3 Parsed triple results
        v-subheader Invalid claim triples
        p
          | There are #[b {{ invalidTriples.length }}] &nbsp;
          tooltip(:docs="$store.state.docs.ents.invalidTriple") invalid triples
          | &nbsp; generated from the claim text. &nbsp;
          invalid-triple-dialog(:triples="invalidTriples")
        v-subheader Valid claim triples
        p
          | There are #[b {{ claimTriples.length }}] &nbsp;
          tooltip(:docs="$store.state.docs.ents.validTriple") valid triples
          | &nbsp; generated from the claim text.
          span(style="color: #e65100") &nbsp; Select a triple
          span &nbsp; for further analysis.
        v-radio-group.triple-radio-group(v-model="selectedTriple")
          div(v-for="item in claimTriples", :key="item.idx")
            .py-2
              v-radio(:value="item")
                template(v-slot:label="")
                  b \#{{ item.idx }}
                  | : &nbsp;
                  v-chip.ma-2(outlined, label, color="primary")
                    code.font-weight-bold.body-1(
                      style="background-color: transparent"
                    ) {{ item.sub_term }} -
                      | {{ item.pred }} -> {{ item.obj_term }}
              .pl-5
                .pl-5.pt-1
                span Details
                claim-triple(
                  :item="item",
                  :html-text="htmlDisplay[item.idx].text"
                )
</template>

<script lang="ts">
import Vue from "vue";

import ClaimTriple from "@/components/widgets/ClaimTriple.vue";
import { checkStageComplete } from "@/funcs/utils.ts";
import { Triple } from "@/types/types.ts";
import ClaimTextDisplay from "@/components/widgets/ClaimTextDisplay.vue";
import InvalidTripleDialog from "@/components/widgets/InvalidTripleDialog.vue";
import * as backendRequests from "@/funcs/backend_requests";
import * as processing from "@/funcs/processing";

export default Vue.extend({
  name: "TripleSelect",
  components: {
    ClaimTriple,
    ClaimTextDisplay,
    InvalidTripleDialog,
  },
  props: {
    stage: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      title: "Select a claim triple",
      selectedTriple: null,
      loading: false,
    };
  },
  computed: {
    pageDocs(): string {
      return this.$store.state.docs.general.tripleSelect
        .split("\n")
        .splice(1)
        .join("\n");
    },
    inactiveMessage(): string {
      const stageNotReachedMessage =
        "Claim text has not been processed. You should revert to last stage.";
      const emptyResultsMessage =
        "No results have been parsed successfully. You should revert to last stage and adjust your query.";
      if (this.tripleResultsEmpty) {
        return emptyResultsMessage;
      } else {
        return stageNotReachedMessage;
      }
    },
    active(): boolean {
      return this.$store.getters["claimData/claimParsed"];
    },
    tripleResultsEmpty(): boolean {
      const stageReached =
        this.$store.state.queryStage.latestStage == this.stage;
      const tripleEmpty = !this.$store.getters["claimData/claimParsed"];
      const res = tripleEmpty && stageReached;
      return res;
    },
    claimData(): null | Record<string, any> {
      return this.$store.state.claimData.claimTriples.length > 0
        ? this.$store.state.claimData
        : null;
    },
    claimText(): null | Array<string> {
      return this.claimData.sents.length > 0 ? this.claimData.sents : null;
    },
    claimTriples(): Array<Triple> {
      return this.claimData.claimTriples;
    },
    invalidTriples(): Array<Record<string, any>> {
      return this.$store.state.claimData.invalidTriples;
    },
    htmlDisplay(): Array<string> {
      return this.claimData.htmlDisplay;
    },
    buttonDisabled(): boolean {
      const locked = checkStageComplete(this.stage);
      const inputEmpty = !this.selectedTriple;
      const res = [locked, inputEmpty].reduce((a, b) => a || b);
      return res;
    },
    btnLabel(): string {
      const good = "Confirm and proceed";
      const inactive = "Awaiting completion of previous stage";
      const empty = "Awaiting triple selection";
      const finished = "Query finished";
      if (!this.active) {
        return inactive;
      } else if (checkStageComplete(this.stage)) {
        return finished;
      } else if (!this.selectedTriple) {
        return empty;
      } else {
        return good;
      }
    },
  },
  mounted: function () {
    const claimTriple = this.$store.state.ents.claimTriple;
    const completed = checkStageComplete(this.stage);
    if (claimTriple && completed) {
      this.selectedTriple = claimTriple;
    }
  },
  methods: {
    async update(): Promise<void> {
      this.loading = true;
      await this.$store.dispatch("ents/submitClaimTriple", this.selectedTriple);
      await processing.getOntologyEnts(this.selectedTriple);
      this.loading = false;
      await this.$store.dispatch("queryStage/completeStage", this.stage);
    },
  },
});
</script>

<style scoped>
.triple-radio-group {
  max-height: 750px;
  overflow-y: scroll;
}
.confirm-btn {
  position: fixed;
  z-index: 99;
}
</style>
