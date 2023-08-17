import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'https://msus1.megashares.com', // Use the environment variable
  // other configurations
});

export default instance;