import store from './store';
import FileManager from './FileManager.vue';
import "./assets/over.css";

export default {
    install: (app, options) => {
        // eslint-disable-next-line no-console
        if (!options.store) console.error('Please provide a vuex store!!');

        app.component('file-manager', FileManager);

        options.store.registerModule('fm', store);
    },
};
