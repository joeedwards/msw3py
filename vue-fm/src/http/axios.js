import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000', // Change this to your Flask backend URL
  // other configurations
});

export default instance;