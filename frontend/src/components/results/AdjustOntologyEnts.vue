<template>
  <div>
    <h3>Claim triple</h3>
    <v-row>
      <v-col>
        <claim-triple v-if="claimTriple" :item="claimTriple" />
      </v-col>
      <v-col>
        <div class="py-3">
          <v-btn color="primary" :disabled="btnState.disabled" @click="update">
            {{ btnState.label }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <h3>Select ontology entities</h3>
    <span class="text-caption">
      Maximum number of subject / object ontology entities should not exceed
    </span>
    <span class="font-weight-black">
      <code>{{ numOntologyEnts }}</code>
    </span>
    .
    <v-row>
      <v-col cols="6">
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
      <v-col cols="6">
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
</template>

<script lang="ts">
import Vue from "vue";

import ClaimTriple from "@/components/widgets/ClaimTriple.vue";
import EntityItem from "@/components/widgets/EntityItem.vue";
import { Triple, OntologyEnt } from "@/types/types";

export default Vue.extend({
  name: "AdjustOntologyEnts",
  components: {
    ClaimTriple,
    EntityItem,
  },
  data() {
    return {
      ontologyEntSubjectSelect: [],
      ontologyEntObjectSelect: [],
      numOntologyEnts: 4,
    };
  },
  computed: {
    claimTriple(): Triple {
      const claimTriple = this.$store.state.ents.claimTriple;
      return claimTriple;
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
    btnState(): Record<string, boolean | string> {
      // labels
      const good = "Confirm and proceed";
      const sizeReached = "Reduce number of selected entities";
      const empty = "Select subject and onject ontology entities";
      //
      const entLimitReached =
        this.ontologyEntSubjectSelect.length > this.numOntologyEnts ||
        this.ontologyEntObjectSelect.length > this.numOntologyEnts;
      if (entLimitReached)
        return {
          disabled: true,
          label: sizeReached,
        };
      const inputEmpty =
        this.ontologyEntSubjectSelect.length == 0 ||
        this.ontologyEntObjectSelect.length == 0;
      if (inputEmpty)
        return {
          disabled: true,
          label: empty,
        };
      return {
        disabled: false,
        label: good,
      };
    },
  },
  mounted() {
    this.numOntologyEnts = this.$store.state.params.ontologyNumEnts;
    const ontologyEntSubject = this.$store.state.ents.ontologySubjectEnts.ents;
    if (ontologyEntSubject) {
      this.ontologyEntSubjectSelect = ontologyEntSubject;
    }
    const ontologyEntObject = this.$store.state.ents.ontologyObjectEnts.ents;
    if (ontologyEntObject) {
      this.ontologyEntObjectSelect = ontologyEntObject;
    }
  },
  methods: {
    async update(): Promise<void> {
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
      await this.$emit("regen");
    },
  },
});
</script>

<style scoped>
.ent-picker {
  max-height: 750px;
  overflow-y: scroll;
}
</style>
