<template>
  <div>
    <v-card id="toc-card" flat>
      <v-card-title>
        <h2>Contents</h2>
      </v-card-title>
      <v-list v-if="outline">
        <v-list-item-group>
          <v-list-item
            v-for="item in outline"
            :key="item.ref"
            @click="$emit('goto', item.ref)"
          >
            <v-list-item-content>
              <v-list-item-title>
                <span v-if="item.lv && item.lv > 1">
                  &nbsp; &nbsp; &nbsp; &nbsp;
                </span>
                <span v-if="item.focus" class="blue--text text--darken-4">
                  <span v-if="item.shortLabel">
                    {{ item.shortLabel }}
                  </span>
                  <span v-else>
                    {{ item.label }}
                  </span>
                </span>
                <span v-else class="grey--text">
                  <span v-if="item.shortLabel">
                    {{ item.shortLabel }}
                  </span>
                  <span v-else>
                    {{ item.label }}
                  </span>
                </span>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

type Outline = Record<
  string,
  {
    ref: string;
    label: string;
    shortLabel?: string;
    focus: boolean;
    lv?: number;
  }
>;

export default Vue.extend({
  name: "Toc",
  props: {
    outline: {
      type: Object as () => Outline,
      required: true,
    },
  },
});
</script>

<style scoped>
#toc-card {
  position: fixed;
}
</style>
