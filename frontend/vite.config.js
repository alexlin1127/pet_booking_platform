import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  // ✅ 引入 path 模組

export default defineConfig({
  plugins: [vue()],
   resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // ✅ 讓 @ 等於 src 資料夾
    }
  },
  css: {
    postcss: './postcss.config.js',
  }
})
