import Axios from 'axios';

const axios = Axios.create({
  baseURL: process.env.BASE_URL,
});

export default axios;
