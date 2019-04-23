import Vue from 'vue';
import axios from 'axios';
import VueAxios from 'vue-axios';
import Cookies from 'js-cookie';
import { API_URL } from "./config";

export class APIService {

  constructor() {
    Vue.use(VueAxios, axios);
    Vue.axios.defaults.baseURL = API_URL;
    Vue.axios.defaults.headers = {
      'X-CSRFToken': Cookies.get('csrftoken')
    }
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

  getRisks(id) {
    const url = `${API_URL}risk-types/${id}/risk/`;
    return Vue.axios.get(url)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  getRisk(riskId) {
    const url = `${API_URL}risk/${riskId}/`;
    return Vue.axios.get(url)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  createRisk(data) {
    const url = `${API_URL}risk/`;
    return Vue.axios.post(url, data)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  updateRisk(riskId, data) {
    const url = `${API_URL}risk/${riskId}/`;
    return Vue.axios.put(url, data)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }

  deleteRisk(riskId) {
    const url = `${API_URL}risk/${riskId}/`;
    return Vue.axios.delete(url)
      .then((response) => {
        return response;
      })
      .catch((error) => {
        throw new Error(`ApiService ${error}`);
      });
  }
}
