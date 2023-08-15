<!-- App.vue -->
<template>
  <div>
    <input type="file" @change="uploadFile">
    <div v-for="file in files" :key="file.id">
      <span>{{ file.name }}</span>
      <button @click="deleteFile(file.id)">Delete</button>
      <video-player v-if="file.type.startsWith('video')" :options="playerOptions" :src="file.content"></video-player>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      files: [],
      playerOptions: {
        autoplay: true,
        controls: true,
        sources: []
      }
    }
  },
  methods: {
    async fetchFiles() {
      const response = await this.$http.get('/files')
      this.files = response.data
    },
    async uploadFile(event) {
      const formData = new FormData()
      formData.append('file', event.target.files[0])
      await this.$http.post('/files', formData)
      this.fetchFiles()
    },
    async deleteFile(fileId) {
      await this.$http.delete(`/files/${fileId}`)
      this.fetchFiles()
    }
  },
  created() {
    this.fetchFiles()
  }
}
</script>
