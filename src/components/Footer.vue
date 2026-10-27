<script setup>
const year = new Date().getFullYear()
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <span class="footer-logo">🍦</span>
          <span>雪糕考研</span>
        </div>
        <p class="footer-desc">
          考研院校与信息一站式平台 · 祝你一战成硕
        </p>
        <p class="footer-note">
          本站国家线等动态数据同步自开源项目
          <a
            class="footer-link"
            href="https://github.com/danking211367/kaoyan-site"
            target="_blank"
            rel="noopener noreferrer"
          >kaoyan-site</a>（每周更新）及
          <a
            class="footer-link"
            href="https://yz.chsi.com.cn"
            target="_blank"
            rel="noopener noreferrer"
          >中国研究生招生信息网</a>；
          学科评估、复试线、报录比等为示例数据，仅供参考，请以各校研招网及教育部官方发布为准。
        </p>
        <p class="footer-copy">© {{ year }} 雪糕考研 · 仅供学习交流使用</p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #0f172a;
  color: #94a3b8;
  padding: 40px 0;
  margin-top: 64px;
}

.footer-inner {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #e2e8f0;
  font-size: 17px;
  font-weight: 700;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--primary);
  font-size: 15px;
}

.footer-desc {
  font-size: 14px;
}

.footer-note {
  font-size: 12px;
  line-height: 1.8;
  max-width: 760px;
}

.footer-link {
  color: #60a5fa;
  text-decoration: underline;
}

.footer-copy {
  font-size: 12px;
  margin-top: 8px;
}
</style>
