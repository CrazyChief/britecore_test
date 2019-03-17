import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import { API_URL } from "./config";

export class APIService {

  constructor() {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;
  }

  getAllRiskTypes() {
    const url = `${API_URL}risk-types/`;
    return Vue.axios.get(url)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  getSingleRiskType(id) {
    const url = `${API_URL}risk-types/${id}/`;
    return Vue.axios.get(url)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  createRiskType(data) {
    const url = `${API_URL}risk-types/`;
    return Vue.axios.post(url, data)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  updateRiskType(id, data) {
    const url = `${API_URL}risk-types/${id}/`;
    return Vue.axios.put(url, data)
      .then((response) => {
        return response;
      });
  }
}
