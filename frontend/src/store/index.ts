import Vue from 'vue';
import Vuex from 'vuex';
import { API } from '@/api';
import { IAttributeObject } from '@/dto/attributes.response';
import { IAttribute, IAttributeValue, AttributeType } from '@/models';

export const LOAD_ATTRIBUTES = 'LOAD_ATTRIBUTES';
export const LOAD_FILTERED_PACKERS = 'LOAD_FILTERED_PACKERS';

export const SET_ATTRIBUTES = 'SET_ATTRIBUTES';
export const SET_RESULTS = 'SET_RESULTS';

export const GET_ATTRIBUTES = 'GET_ATTRIBUTES';
export const GET_FULL_MATCH_RESULTS = 'GET_FULL_MATCH_RESULTS';
export const GET_OTHER_MATCH_RESULTS = 'GET_OTHER_MATCH_RESULTS';
export const GET_OTHER_MATCH_FLAGS_RESULTS = 'GET_OTHER_MATCH_FLAGS_RESULTS';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    attributes: new Array<IAttribute>(),
    fullMatch: new Array<any>(),
    otherMatch: new Array<any>(),
    otherMatchFlag: new Array<any>()
  },
  mutations: {
    SET_ATTRIBUTES(state, payload) {
      const attributes = new Array<IAttribute>();

      for (const name in payload) {
        const element: IAttributeObject = payload[name];
        const attribute: Partial<IAttribute> = {
          displayName: element.name,
          description: element.description,
          name,
          values: []
        };

        for (const attrName in element) {
          if (['name', 'description'].indexOf(attrName) > -1) continue;
          
          const attr = element[attrName] as IAttributeValue;
          const val: any = {
            type: attr.type,
            name: attrName == 'value' ? '' : attrName
          };

          if (attr.type == AttributeType.NUMBER) {
            val.min = attr.min;
            val.max = attr.max;
          } else {
            val.values = attr.values;
          }

          attribute.values!.push(val);
        }

        attributes.push(attribute as IAttribute);
      }

      state.attributes = attributes;
    },
    SET_RESULTS(state, payload) {
      let results = new Array<any>();

      for (const name in payload.full_match) {
        const element = payload[name];
        results.push({
          name,
          ...element
        });
      }

      state.fullMatch = results;
      results = new Array<any>();

      for (const name in payload.other_match) {
        const element = payload[name];
        results.push({
          name,
          ...element
        });
      }

      state.otherMatch = results;
      results = new Array<any>();

      for (const name in payload.other_match_flag) {
        const element = payload[name];
        results.push({
          name,
          ...element
        });
      }

      state.otherMatchFlag = results;
    }
  },
  actions: {
    LOAD_ATTRIBUTES({ commit }) {
      API.getAttributes()
        .then((attributes) => {
          commit(SET_ATTRIBUTES, attributes);
        });
    },
    LOAD_FILTERED_PACKERS({ commit }, params) {
      API.getSearchResults(params)
        .then((results) => {
          commit(SET_RESULTS, results);
        });
    }
  },
  getters: {
    GET_ATTRIBUTES(state) {
      return state.attributes;
    },
    GET_FULL_MATCH_RESULTS(state) {
      return state.fullMatch;
    },
    GET_OTHER_MATCH_RESULTS(state) {
      return state.otherMatch;
    },
    GET_OTHER_MATCH_FLAGS_RESULTS(state) {
      return state.otherMatchFlag;
    }
  },
  modules: {
  }
});
