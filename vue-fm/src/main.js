import { createApp } from 'vue';
import { createStore } from 'vuex';
import { authenticateUserWithMetaMask } from './auth.js'; // Adjust the path to the auth.js module

// store
import fm from './store';
// App
import App from './FileManager.vue';

// create new store
const store = createStore({
    strict: import.meta.env.DEV,
    modules: { fm },
});


// Authenticate the user before mounting the Vue app
authenticateUserWithMetaMask()
  .then(response => {
    if (response.data.status === 'success') {
      // User is authenticated, mount the Vue app
      window.fm = createApp(App).use(store).mount('#fm');
    } else {
      // Handle error, e.g., show an error message to the user
      console.error('Authentication failed.');
    }
  })
  .catch(error => {
    console.error('Authentication error:', error.message);
  });
