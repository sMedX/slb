<template>
  <v-app>
    <v-app-bar
      app
      color="white"
      dark
    >
      <img :src="require('./assets/logo.png')" />
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<style lang="scss" scoped>
img {
  height: 50px;
}
</style>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'App',

  components: {
  },

  data: () => ({
    //
  }),
});
</script>
