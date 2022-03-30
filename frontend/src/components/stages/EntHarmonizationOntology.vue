<template>
  <v-container>
    <v-row justify="space-between">
      <v-col cols="6">
        <h2>{{ title }}</h2>
        <p class="blockquote">
          <vue-markdown
            :breaks="false"
            :source="
              $store.state.docs.general.entHarmonizationOntology
                .split('\n')
                .splice(1)
                .join('\n')
            "
          />
        </p>
      </v-col>
      <v-col>
        <div class="py-3 d-flex justify-end">
          <v-btn
            v-if="$store.state.queryStage.currentStage == stage && active"
            color="primary"
            class="confirm-btn"
            large
            :disabled="buttonDisabled"
            @click="submit"
          >
            <v-progress-circular v-if="loading" indeterminate color="grey" />
            {{ btnLabel }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <div v-if="active">
      <div>
        <h3>Claim triple</h3>
        <claim-triple
          v-if="claimTriple"
          :item="claimTriple"
          :html-text="claimHtmlText"
        />
        <h3>Select ontology entities</h3>
        <span class="text-caption">
          Maximum number of subject / object ontology entities should not exceed
        </span>
        <span class="font-weight-black">
          <code>{{ numOntologyEnts }}</code>
        </span>
        .
        <v-row>
          <v-col v-if="active" cols="6">
            <h4>Subject entities {{ subjectEntBadge }}</h4>
            <div class="ent-picker">
              <v-checkbox
                v-for="item in ontologyEntCandidates.subjects"
                :key="item.ent_id"
                v-model="ontologyEntSubjectSelect"
                :value="item"
              >
                <template v-slot:label>
                  <entity-item :item="item" ent-type="Efo" />
                </template>
              </v-checkbox>
            </div>
          </v-col>
          <v-col v-if="active" cols="6">
            <h4>Object entities {{ objectEntBadge }}</h4>
            <div class="ent-picker">
              <v-checkbox
                v-for="item in ontologyEntCandidates.objects"
                :key="item.ent_id"
                v-model="ontologyEntObjectSelect"
                :value="item"
              >
                <template v-slot:label>
                  <entity-item :item="item" ent-type="Efo" />
                </template>
              </v-checkbox>
            </div>
          </v-col>
        </v-row>
      </div>
      <br />
    </div>
    <div v-else>
      <v-alert type="info">{{ infoInactive }}</v-alert>
    </div>
  </v-container>
</template>

<script lang="ts">
import Vue from "vue";

import ClaimTriple from "@/components/widgets/ClaimTriple.vue";
import EntityItem from "@/components/widgets/EntityItem.vue";
import { checkStageComplete } from "@/funcs/utils";
import { Triple, OntologyEnt } from "@/types/types";

export default Vue.extend({
  name: "EntHarmonizationOntology",
  components: {
    ClaimTriple,
    EntityItem,
  },
  props: {
    stage: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      title: "Entity harmonization (Ontology)",
      subtitle: "Harmonization of claim triple entities and ontology entities",
      infoInactive: `Claim triple has not been processed. You should revert to last stage.`,
      ontologyEntSubjectSelect: [],
      ontologyEntObjectSelect: [],
      numOntologyEnts: 4,
      loading: false,
    };
  },
  computed: {
    progressStage(): number {
      const stage = this.$store.state.queryStage.latestStage;
      return stage;
    },
    claimTriple(): Triple {
      const claimTriple = this.$store.state.ents.claimTriple;
      return claimTriple;
    },
    claimHtmlText(): null | string {
      // NOTE: when idx is 0, falsiness gives false positiveness
      if (this.claimTriple && this.claimTriple.idx != null) {
        const idx = this.claimTriple.idx;
        const htmlText = this.$store.state.claimData.htmlDisplay[idx].text;
        return htmlText;
      } else {
        return null;
      }
    },
    ontologyEntCandidates(): {
      subjects: Array<OntologyEnt>;
      objects: Array<OntologyEnt>;
    } {
      const subjectCandidates = this._.chain(
        this.$store.state.ents.ontologySubjectEnts.candidates,
      )
        .sortBy(["identity_score"])
        .value();
      const objectCandidates = this._.chain(
        this.$store.state.ents.ontologyObjectEnts.candidates,
      )
        .sortBy(["identity_score"])
        .value();
      const res = {
        subjects: subjectCandidates,
        objects: objectCandidates,
      };
      return res;
    },
    active(): boolean {
      const active = this.$store.getters["ents/ontologyCandidatesDone"];
      return active;
    },
    buttonDisabled(): boolean {
      const locked = checkStageComplete(this.stage);
      const inputEmpty =
        this.ontologyEntSubjectSelect.length == 0 ||
        this.ontologyEntObjectSelect.length == 0;
      return inputEmpty || locked || this.entLimitReached;
    },
    entLimitReached(): boolean {
      const subjectInvalid =
        this.ontologyEntSubjectSelect.length > this.numOntologyEnts;
      const objectInvalid =
        this.ontologyEntObjectSelect.length > this.numOntologyEnts;
      const res = subjectInvalid || objectInvalid;
      return res;
    },
    btnLabel(): string {
      const good = "Confirm and proceed";
      const inactive = "Awaiting completion of previous stage";
      const sizeReached = "Reduce number of selected entities";
      const empty = "Select subject and onject ontology entities";
      const finished = "Query finished";
      const inputEmpty =
        this.ontologyEntSubjectSelect.length == 0 ||
        this.ontologyEntObjectSelect.length == 0;
      if (!this.active) {
        return inactive;
      } else if (checkStageComplete(this.stage)) {
        return finished;
      } else if (inputEmpty) {
        return empty;
      } else if (this.entLimitReached) {
        return sizeReached;
      } else {
        return good;
      }
    },
    subjectEntBadge(): string {
      const count = this.ontologyEntSubjectSelect.length;
      const limit = this.numOntologyEnts;
      const res = `${count} / ${limit}`;
      return res;
    },
    objectEntBadge(): string {
      const count = this.ontologyEntObjectSelect.length;
      const limit = this.numOntologyEnts;
      const res = `${count} / ${limit}`;
      return res;
    },
  },
  watch: {
    // NOTE: this component has already been mounted when the
    // whole stepper was created, so need to watch
    // if it is progressed to this stage
    progressStage(val) {
      if (val == this.stage) {
        const ontologyEntSubject =
          this.$store.state.ents.ontologySubjectEnts.ents;
        if (ontologyEntSubject) {
          this.ontologyEntSubjectSelect = ontologyEntSubject;
        }
        const ontologyEntObject =
          this.$store.state.ents.ontologyObjectEnts.ents;
        if (ontologyEntObject) {
          this.ontologyEntObjectSelect = ontologyEntObject;
        }
      }
    },
  },
  mounted() {
    this.numOntologyEnts = this.$store.state.params.ontologyNumEnts;
  },
  methods: {
    async submit(): Promise<void> {
      await this.update();
    },
    async update(): Promise<void> {
      this.loading = true;
      await this.$store.dispatch("ents/submitOntologyEnts", {
        ents: this.ontologyEntSubjectSelect,
        subject: true,
        entGroup: "ents",
      });
      await this.$store.dispatch("ents/submitOntologyEnts", {
        ents: this.ontologyEntObjectSelect,
        subject: false,
        entGroup: "ents",
      });
      this.loading = false;
      await this.$store.dispatch("queryStage/completeStage", this.stage);
    },
  },
});
</script>

<style scoped>
.ent-picker {
  max-height: 750px;
  overflow-y: scroll;
}
.confirm-btn {
  position: fixed;
  z-index: 99;
}
</style>
