<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-row class="grey lighten-5">
          <v-card class="mx-auto" width="70%" outlined>
            <v-expansion-panels v-model="panel">
              <v-expansion-panel>
                <v-expansion-panel-header>
                  <span class="title">Full Match</span>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="fixed-height">
                  <v-container>
                    <v-row>
                      <v-col
                        v-for="(item, index) in GET_FULL_MATCH_RESULTS"
                        :key="item.name+index"
                        cols="12"
                        md="4"
                      >
                        <v-card
                          class="d-flex align-center"
                          height="100"
                          @click
                        >
                          <v-img :aspect-ratio="1" :height="100" :src="getRandomImage()"></v-img>
                          <v-card-title>{{item.name}}</v-card-title>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-expansion-panel-content>
              </v-expansion-panel>

              <v-expansion-panel>
                <v-expansion-panel-header>
                  <span class="title">Other Match</span>
                </v-expansion-panel-header>
                <v-expansion-panel-content class="fixed-height">
                  <v-container>
                    <v-row>
                      <v-col
                        v-for="(item, index) in GET_OTHER_MATCH_RESULTS"
                        :key="item.name+index"
                        cols="12"
                        md="4"
                      >
                        <v-card
                          class="d-flex align-center"
                          height="100"
                          @click
                        >
                          <v-img :aspect-ratio="1" :height="100" :src="getRandomImage()"></v-img>
                          <v-card-title class="no-flex">
                            <div>{{item.name}}</div>
                            <v-chip>Match: {{item.__match}}%</v-chip>
                          </v-card-title>
                        </v-card>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
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

            <v-expansion-panels class="fixed-height">
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
                        :step="0.05"
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

<style lang="scss" scoped>
.fixed-height {
  max-height: 700px;
  overflow-y: auto;
}

.no-flex {
  display: block;
}
</style>

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

const images = [
  "/img/1.jpg",
  "/img/2.jpg",
  "/img/3.jpg",
  "/img/4.jpg",
  "/img/5.jpg",
  "/img/6.jpg",
  "/img/7.jpg",
  "/img/8.jpg",
  "/img/9.jpg",
  "/img/10.jpg",
  "/img/11.jpg",
  "/img/12.jpg",
  "/img/13.jpg"
];

export default {
  name: "home",
  components: {},
  data() {
    return {
      selected: {},
      panel: 0
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
    },
    getRandomImage() {
      const index = Math.random() * (images.length - 1);
      return images[index ^ 0];
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
