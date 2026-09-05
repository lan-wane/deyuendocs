---
params:
  - name: class
    type: list[str]
    required: true
    positional: true
  - name: section
    type: Literal["条目", "段落", "命名空间", "章节", "引用", "附录"]
    required: false
    key_only: true
    default: "条目"
  - name: icon
    type: Path | cssClass
    required: false
    key_only: true
    default: "fas fa-info-circle"
  - name: style
    type: str
    required: false
    key_only: true
    default: "notice-info"
---
?function
function render(params) {
    let classList = params.class;
    if (typeof classList === 'string') {
        try {
            classList = JSON.parse(classList);
        } catch (e) {
            classList = classList.split(',').map(s => s.trim());
        }
    }
    if (!Array.isArray(classList)) classList = [];

    const section = params.section || '条目';
    if (classList.length > 0) {
        const highlightedItems = classList.map(item => `<span class="exclusive-highlight">${item}</span>`);
        let listText = '';
        if (highlightedItems.length === 1) {
            listText = highlightedItems[0];
        } else {
            const last = highlightedItems.pop();
            listText = highlightedItems.join('、') + '和' + last;
        }
        return '本' + section + '所述内容仅适用于' + listText + '。';
    } else {
        return params.msg || '';
    }
}
?main_render
[[Notice(content="{text}", icon="{icon}", style="{style}")]]
?style exclusive-highlight
.exclusive-highlight {
  font-weight: 700;
  color: #1a56db;
  background: transparent;
  padding: 0 4px;
  border-radius: 4px;
}