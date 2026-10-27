import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ command }) => ({
  plugins: [vue()],
  // GitHub Pages 部署在 /xuegao-kaoyan/ 子路径下；本地开发保持根路径
  base: command === 'build' ? '/xuegao-kaoyan/' : '/',
  server: {
    port: 5173,
    open: false,
    host: true // 监听局域网，手机可通过电脑 IP 访问
  }
}))
