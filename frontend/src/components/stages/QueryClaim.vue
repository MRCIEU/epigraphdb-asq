<template>
  <v-container>
    <v-row justiy="space-between">
      <v-col cols="6">
        <h2>{{ title }}</h2>
        <p class="blockquote">
          <vue-markdown
            :breaks="false"
            :source="
              $store.state.docs.general.queryParsing
                .split('\n')
                .splice(1)
                .join('\n')
            "
          />
        </p>
      </v-col>
      <v-spacer />
      <v-col>
        <div class="py-3 d-flex justify-end">
          <v-btn color="error" @click="reload">Reload and start again</v-btn>
        </div>

        <div class="py-3 d-flex justify-end">
          <v-btn
            v-if="$store.state.queryStage.currentStage == stage"
            color="primary"
            class="confirm-btn"
            large
            :disabled="progButtonDisabled"
            @click="update"
          >
            <v-progress-circular v-if="loading" indeterminate color="grey" />
            {{ btnLabel }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8">
        <v-select
          v-model="topicSelect"
          :disabled="usingCustomText"
          label="Select a predefined topic category"
          :items="topicOptions"
        ></v-select>
        <v-select
          v-model="literatureSelect"
          :disabled="usingCustomText"
          label="Select a predefined source"
          :menu-props="{ maxHeight: 800 }"
          :items="queryOptions"
        >
          <template v-slot:item="{ item }">
            <div>
              <span>{{ item.text }}</span>
              <br />
              <p class="blockquote" style="max-width: 45rem">
                {{ showBuiltinText(item.value) }}
              </p>
            </div>
          </template>
        </v-select>
      </v-col>
      <v-spacer />
      <v-col cols="3">
        <v-switch v-model="usingCustomText" label="Custom claim text" />
        <adjust-results />
      </v-col>
    </v-row>
    <div v-if="!usingCustomText">
      <v-textarea
        v-model="builtinText"
        disabled
        auto-grow
        filled
        clear-icon="mdi-close-circle"
        label="Predefined claim text"
        counter
      />
    </div>
    <div v-else>
      <span class="text-caption">Max character limit: {{ charMaxLen }}</span>
      <v-textarea
        v-model="customClaimTextInput"
        filled
        auto-grow
        clearable
        clear-icon="mdi-close-circle"
        label="Custom claim text"
        counter
      />
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

// @ts-ignore
import defaultText from "@/resources/query-claim-default.md";
import { topics } from "@/resources/query-candidates";
import { checkStageComplete } from "@/funcs/utils";
import { parseClaim } from "@/funcs/backend_requests";

import AdjustResults from "@/components/results/AdjustResultsPreQuery.vue";

export default Vue.extend({
  name: "QueryClaim",
  components: {
    AdjustResults,
  },
  props: {
    stage: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      title: "Insert query text",
      customClaimTextInput: "",
      usingCustomText: false,
      loading: false,
      charMaxLen: null,
      topicSelect: "obesity",
      topics: topics,
      literatureSelect: "dixon-peters-2018",
    };
  },
  computed: {
    stageCompleted(): boolean {
      const completed = checkStageComplete(this.stage);
      return completed;
    },
    progButtonDisabled(): boolean {
      const res = [
        this.textEmpty,
        this.stageCompleted,
        this.textSizeReached,
      ].reduce((a, b) => a || b);
      return res;
    },
    textEmpty(): boolean {
      const str = this.inputText;
      return str == null || /^\s*$/.test(str);
    },
    textSizeReached(): boolean {
      const res =
        this.inputText !== null && this.inputText.length > this.charMaxLen;
      return res;
    },
    topicOptions(): Array<Record<string, string>> {
      const res = this._.chain(topics)
        .mapValues((item) => ({
          value: item.key,
          text: item.label,
        }))
        .values()
        .value();
      return res;
    },
    queryOptions(): Array<Record<string, string>> {
      const res = this._.chain(this.literatureCandidates)
        .mapValues((item) => ({
          value: item.key,
          text: item.title,
        }))
        .values()
        .value();
      return res;
    },
    literatureCandidates(): Record<string, Record<string, string>> {
      const candidates = this.topics[this.topicSelect].candidates;
      return candidates;
    },
    builtinText(): string {
      if (this.literatureSelect) {
        return this.literatureCandidates[this.literatureSelect].text;
      } else {
        return "";
      }
    },
    inputText(): string {
      return this.usingCustomText
        ? this.customClaimTextInput
        : this.builtinText;
    },
    btnLabel(): string {
      const good = "Confirm and proceed";
      const empty = "Awaiting text input";
      const sizeReached = "Reduce size of the input text";
      const finished = "Query completed (refresh session for a new query)";
      if (this.textEmpty) {
        return empty;
      } else if (this.stageCompleted) {
        return finished;
      } else if (this.textSizeReached) {
        return sizeReached;
      } else {
        return good;
      }
    },
  },
  watch: {
    topicSelect(newVal) {
      if (newVal) {
        this.literatureSelect = this.queryOptions[0].value;
      }
    },
  },
  mounted: function () {
    this.charMaxLen = this.$store.state.params.claimTextMaxCharLen;
  },
  methods: {
    reload() {
      window.location.reload();
    },
    async submit(): Promise<void> {
      await this.update();
    },
    async update(): Promise<void> {
      this.loading = true;
      await this.$store.dispatch("claimData/updateClaimText", this.inputText);
      const parseResults = await parseClaim(this.inputText);
      await this.$store.dispatch("claimData/updateParseResults", parseResults);
      this.loading = false;
      await this.$store.dispatch("queryStage/completeStage", this.stage);
    },
    showBuiltinText(key: string): string {
      const text = this.literatureCandidates[key].text;
      const cutoff = 500;
      const subtext =
        text.length > cutoff ? text.substring(0, cutoff) + "..." : text;
      const res = subtext;
      return res;
    },
  },
});
</script>

<style scoped>
.confirm-btn {
  position: fixed;
  z-index: 99;
}
</style>
