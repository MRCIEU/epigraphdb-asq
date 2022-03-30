<template lang="pug">
v-container
  h3 Entity harmonization stage
  v-row
    v-col(cols="6")
      v-row
        v-col
          param-subheader(
            :label="labels['ontologyNumCandidates'].label",
            :docs="labels['ontologyNumCandidates'].docs"
          )
        v-col
          v-select(
            v-model="ontologyNumCandidates",
            :items="numEntsOptions",
            dense
          )
    v-col(cols="6")
      v-row
        v-col
          param-subheader(
            :label="labels['ontologyIcScoreThreshold'].label",
            :docs="labels['ontologyIcScoreThreshold'].docs"
          )
        v-col
          v-select(
            v-model="ontologyIcScoreThreshold",
            :items="icScoreOptions",
            dense
          )
  v-row
    v-col(cols="6")
      v-row
        v-col
          param-subheader(
            :label="labels['ontologySimilarityScoreThreshold'].label",
            :docs="labels['ontologySimilarityScoreThreshold'].docs"
          )
        v-col
          v-select(
            v-model="ontologySimilarityScoreThreshold",
            :items="similarityScoreOptions",
            dense
          )
    v-col(cols="6")
      v-row
        v-col
          param-subheader(
            :label="labels['ontologyIdentityScoreThreshold'].label",
            :docs="labels['ontologyIdentityScoreThreshold'].docs"
          )
        v-col
          v-select(
            v-model="ontologyIdentityScoreThreshold",
            :items="identityScoreOptions",
            dense
          )
  h3 Evidence retrieval stage
    v-row
      v-col(cols="6")
        v-row
          v-col
            param-subheader(
              :label="labels['postOntologyNumCandidates'].label",
              :docs="labels['postOntologyNumCandidates'].docs"
            )
          v-col
            v-select(
              v-model="postOntologyNumCandidates",
              :items="numEntsOptions",
              dense
            )
      v-col
        v-row
          v-col
            param-subheader(
              :label="labels['postOntologySimilarityScoreThreshold'].label",
              :docs="labels['postOntologySimilarityScoreThreshold'].docs"
            )
          v-col
            v-select(
              v-model="postOntologySimilarityScoreThreshold",
              :items="similarityScoreOptions",
              dense
            )
  h4 Association evidence
    v-row
      v-col(cols="6")
        v-row
          v-col
            param-subheader(
              :label="labels['assocPvalThreshold'].label",
              :docs="labels['assocPvalThreshold'].docs"
            )
          v-col
            v-select(v-model="assocPvalThreshold", :items="pvalOptions", dense)
  v-divider.py-3
  v-btn(color="primary", @click="update") Update parameters
</template>

<script lang="ts">
import Vue from "vue";
import * as paramDocs from "@/resources/docs/params";
import ParamSubheader from "@/components/widgets/ParamSubheader.vue";

export default Vue.extend({
  name: "AdjustResultsParams",
  components: {
    ParamSubheader,
  },
  data() {
    return {
      labels: {
        // ent harmonization
        ontologyNumCandidates: {
          label: "Number of entity candidates to retrieve",
          docs: paramDocs.paramNumOntologyEntCandidates,
        },
        ontologySimilarityScoreThreshold: {
          label: "Semantic similarity threshold (query vs. Ontology)",
          docs: paramDocs.paramSimilarityScore,
        },
        ontologyIcScoreThreshold: {
          label: "Ontology information score threshold",
          docs: paramDocs.paramIcScore,
        },
        ontologyIdentityScoreThreshold: {
          label: "Ontology identity score",
          docs: paramDocs.paramIdentityScore,
        },
        // rest
        postOntologyNumCandidates: {
          label: "Number of UMLS entities / GWAS traits to retrieve",
          docs: paramDocs.postOntologyNumCandidates,
        },
        postOntologySimilarityScoreThreshold: {
          label: "Semantic similarity threshold (Ontology vs. UMLS/GWAS)",
          docs: paramDocs.paramSimilarityScore,
        },
        assocPvalThreshold: {
          label: "Association evidence P-Value threshold",
          docs: paramDocs.assocPvalThreshold,
        },
      },
      storeParams: [
        "ontologyNumCandidates",
        "ontologySimilarityScoreThreshold",
        // "ontologyIdentityScoreThreshold",
        // "ontologyIcScoreThreshold",
        "postOntologyNumCandidates",
        "postOntologySimilarityScoreThreshold",
        "assocPvalThreshold",
      ],
      // builtin options
      pvalOptions: ["1e-1", "5e-2", "1e-2", "1e-3", "1e-5"],
      similarityScoreOptions: [0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99],
      numEntsOptions: [10, 20, 30, 50],
      icScoreOptions: [0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
      identityScoreOptions: [1.0, 1.2, 1.5, 2.0, 3.0],
      // store ents
      ontologyNumCandidates: this.$store.state.params.postOntologyNumCandidates,
      ontologySimilarityScoreThreshold:
        this.$store.state.params.ontologySimilarityScoreThreshold,
      ontologyIdentityScoreThreshold:
        this.$store.state.params.ontologyIdentityScoreThreshold,
      ontologyIcScoreThreshold:
        this.$store.state.params.ontologyIcScoreThreshold,
      postOntologyNumCandidates:
        this.$store.state.params.postOntologyNumCandidates,
      postOntologySimilarityScoreThreshold:
        this.$store.state.params.postOntologySimilarityScoreThreshold,
      assocPvalThreshold: this.$store.state.params.assocPvalThreshold,
    };
  },
  computed: {
    //
  },
  async mounted(): Promise<void> {
    //
  },
  methods: {
    async update(): Promise<void> {
      await this._.chain(this.storeParams)
        .map((param) => {
          this.$store.dispatch("params/updateParam", {
            key: param,
            value: this[param],
          });
        })
        .value();
      await this.$emit("regen");
    },
  },
});
</script>
