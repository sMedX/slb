<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-row class="grey lighten-5">
          <v-card class="mx-auto" width="70%" outlined>
            <v-list three-line>
              <v-subheader>Full Match</v-subheader>

              <template v-for="(item, index) in GET_FULL_MATCH_RESULTS">
                <v-list-item :key="item.name+index" @click>
                  <v-list-item-avatar tile size="200">
                    <v-img src="https://www.slb.com/-/media/images/co/packers/bluepack-naming.ashx?h=1378&w=2000&la=en&hash=4BFB791C0E4E3A05FEF343F1E93BE12D"></v-img>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <v-chip v-for="(value, key) in item" :key="key+value">{{key}}:{{value}}</v-chip>
                  </v-list-item-content>
                </v-list-item>
                <v-divider :key="item.name" inset="inset"></v-divider>
              </template>

              <v-subheader>Other Match</v-subheader>

              <template v-for="(item, index) in GET_OTHER_MATCH_RESULTS">
                <v-list-item :key="item.name" @click>
                  <v-list-item-avatar tile size="200">
                    <v-img src="https://www.slb.com/-/media/images/co/packers/bluepack-naming.ashx?h=1378&w=2000&la=en&hash=4BFB791C0E4E3A05FEF343F1E93BE12D"></v-img>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <v-list-item-subtitle v-html="item.subtitle"></v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider :key="item.name" inset="inset"></v-divider>
              </template>

              <v-subheader>Other Match Flag</v-subheader>

              <template v-for="(item, index) in GET_OTHER_MATCH_FLAGS_RESULTS">
                <v-list-item :key="item.name" @click>
                  <v-list-item-avatar tile size="200">
                    <v-img :src="item.avatar"></v-img>
                  </v-list-item-avatar>

                  <v-list-item-content>
                    <v-list-item-title v-html="item.name"></v-list-item-title>
                    <v-list-item-subtitle v-html="item.subtitle"></v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
                <v-divider :key="item.name" inset="inset"></v-divider>
              </template>
            </v-list>
          </v-card>

          <v-card class="mx-auto" width="25%" outlined>
            <v-card-title>
              <v-flex>
                <v-row>
                  <v-col cols="9">Parameters</v-col>
                  <v-col cols="3">
                    <v-btn small color="primary" @click="applyFilters">Search</v-btn>
                  </v-col>
                </v-row>
              </v-flex>
            </v-card-title>
            <v-card-subtitle>Use them to filter packers</v-card-subtitle>

            <v-expansion-panels>
              <v-expansion-panel v-for="(item, i) in GET_ATTRIBUTES" :key="i">
                <v-expansion-panel-header>
                  <span class="subtitle-2">{{item.displayName}}</span>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <span class="caption">{{item.description}}</span>

                  <v-row v-for="val in item.values" :key="val.name">
                    <v-col cols="12">
                      <v-slider
                        v-if="val.type == 'float64'"
                        v-model="selected[`${item.name}:${val.name || 'value'}`]"
                        :max="val.max"
                        :min="val.min"
                        :label="val.name"
                        thumb-label="always"
                      ></v-slider>

                      <v-combobox
                        v-if="val.type == 'string'"
                        v-model="selected[`${item.name}:${val.name || 'value'}`]"
                        :items="val.values"
                        :label="val.name"
                      ></v-combobox>
                    </v-col>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {
  LOAD_ATTRIBUTES,
  LOAD_FILTERED_PACKERS,
  GET_ATTRIBUTES,
  GET_FULL_MATCH_RESULTS,
  GET_OTHER_MATCH_RESULTS,
  GET_OTHER_MATCH_FLAGS_RESULTS
} from "@/store";
import { mapGetters, mapActions } from "vuex";
// @ is an alias to /src

export default {
  name: "home",
  components: {},
  data() {
    return {
      selected: {}
    };
  },
  mounted() {
    this.$store.dispatch(LOAD_ATTRIBUTES);
  },
  methods: {
    ...mapActions([LOAD_FILTERED_PACKERS]),
    applyFilters() {
      const params = [];

      for (const key in this.selected) {
        const value = this.selected[key];
        params.push([...key.split(":"), value]);
      }

      this.LOAD_FILTERED_PACKERS(params);
    }
  },
  computed: {
    ...mapGetters([
      GET_ATTRIBUTES,
      GET_FULL_MATCH_RESULTS,
      GET_OTHER_MATCH_RESULTS,
      GET_OTHER_MATCH_FLAGS_RESULTS
    ])
  }
};
</script>
