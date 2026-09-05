---
params:
  - name: content
    type: str
    required: true
    positional: true
  - name: icon
    type: str
    required: false
    default: "fas fa-info-circle"
  - name: style
    type: str
    required: false
    default: "notice-info"
---
?function
function render(params) {
    let content = params.content || '';
    let title = '';
    let body = content;
    const lines = content.split('\n');
    if (lines.length > 0 && lines[0].trim().startsWith('#')) {
        title = lines[0].trim().replace(/^#+\s*/, '');
        body = lines.slice(1).join('\n').trim();
    }
    const titleHtml = title ? `<div class="notice-title">${title}</div>` : '';
    const bodyHtml = body ? `<div class="notice-text">${body}</div>` : '';
    return { titleHtml, bodyHtml };
}
?main_render
<div class="notice {style}">
  <div class="notice-bar"></div>
  <div class="notice-body">
    <i class="{icon}"></i>
    <div class="notice-content">
      {titleHtml}
      {bodyHtml}
    </div>
  </div>
</div>
?style notice
.notice {
  display: flex;
  align-items: stretch;
  margin: 1.5em 0;
  overflow: hidden;
  border-radius: 0 !important;
}
.notice-bar {
  width: 6px;
  flex-shrink: 0;
}
.notice-body {
  flex: 1;
  padding: 18px 24px;
  display: flex;
  align-items: center;       /* 垂直居中图标与内容 */
  gap: 12px;
}
.notice-body i {
  font-size: 1.7em;          /* 与正文行高匹配 (16px * 1.7 ≈ 27px) */
  line-height: 1;            /* 消除图标额外行高 */
  width: auto;               /* 不强制宽度，由字体大小决定 */
  text-align: center;
  flex-shrink: 0;
  vertical-align: middle;    /* 辅助对齐 */
  color: inherit;
}
.notice-content {
  flex: 1;
  min-width: 0;
}
.notice-title {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 4px;
  line-height: 1.4;
  color: #000000;
}
.notice-text {
  font-size: 16px;
  line-height: 1.7;
  color: #000000;
}
.notice-text p {
  margin: 0 0 0.5em 0;
}
.notice-text p:last-child {
  margin-bottom: 0;
}
.notice-text a {
  text-decoration: underline;
}
.notice-text strong,
.notice-text b {
  font-weight: 600;
}
.notice-text em,
.notice-text i {
  font-style: italic;
}
.notice-text code {
  background: rgba(0,0,0,0.06);
  padding: 0.1em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}
.notice-text ul,
.notice-text ol {
  padding-left: 1.5em;
  margin: 0.5em 0;
}
/* 主题变体 */
.notice-info {
  background: #f4f8ff;
  border: 1px solid #d9e2ef;
}
.notice-info .notice-bar {
  background: #1a56db;
}
.notice-info i {
  color: #1a56db;
}
.notice-warning {
  background: #fffbeb;
  border: 1px solid #fcd34d;
}
.notice-warning .notice-bar {
  background: #f59e0b;
}
.notice-warning i {
  color: #f59e0b;
}
.notice-success {
  background: #ecfdf5;
  border: 1px solid #6ee7b7;
}
.notice-success .notice-bar {
  background: #10b981;
}
.notice-success i {
  color: #10b981;
}
.notice-danger {
  background: #fef2f2;
  border: 1px solid #fca5a5;
}
.notice-danger .notice-bar {
  background: #ef4444;
}
.notice-danger i {
  color: #ef4444;
}
.notice-dark {
  background: #f1f3f4;
  border: 1px solid #b0b8c0;
}
.notice-dark .notice-bar {
  background: #374151;
}
.notice-dark i {
  color: #374151;
}