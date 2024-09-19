class Message {

    // 构造函数
    constructor() {
        const containerId = 'message-container';
        this.containerEl = document.getElementById(containerId);

        if (!this.containerEl) {
            // 若不存在则创建新的
            this.containerEl = document.createElement('div');
            this.containerEl.id = containerId;
            // 插入body的末尾
            document.body.appendChild(this.containerEl);
        }
    }

    // 消息弹窗
    show({ type, text, duration, closeable }) {
        let messageEl = document.createElement('div');
        // 开始显示
        messageEl.className = 'message move-in';
        messageEl.innerHTML = `
            <span class="icon icon-${type}"></span>
            <div class="text">${text}</div>
        `;
        // 若当前按钮可关闭
        if (closeable) {
            // 创建关闭按钮
            let closeEl = document.createElement('div');
            closeEl.className = 'close icon icon-close';
            messageEl.appendChild(closeEl);
            // 监听按钮点击
            closeEl.addEventListener('click', () => {
                this.close(messageEl);
            });
        }

        // 追加到message-container末尾
        this.containerEl.appendChild(messageEl);

        // 计时结束后关闭弹窗
        if (duration > 0) {
            setTimeout(() => {
                this.close(messageEl);
            }, duration);
        }
    }

    // 弹窗关闭
    close(messageEl) {
        // 移除move-in效果
        messageEl.className = messageEl.className.replace('move-in', '');
        // 添加move-out效果
        messageEl.className += 'move-out';

        messageEl.addEventListener('animationend', () => {
            messageEl.setAttribute('style', 'height: 0; margin: 0');
        });

        // 动画结束后删除
        messageEl.addEventListener('transitionend', () => {
            messageEl.remove();
        });
    }

}