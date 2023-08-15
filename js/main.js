// main.js
import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VideoPlayer from 'vue-video-player'
import 'video.js/dist/video-js.css'

Vue.use(VideoPlayer)
Vue.prototype.$http = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
