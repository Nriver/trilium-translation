/*
 * 一个显示当前笔记字数的小组件.
 * 给一个笔记加上 #字数统计 的标签就能启用字数统计功能, 你也可以把它设为可继承的标签属性, 这样所有的子笔记也会开启字数统计
 * 
 * 可以到"读书"笔记和子笔记里看到效果
 */
const TPL = `<div style="padding: 10px; border-top: 1px solid var(--main-border-color); contain: none;">
    <strong>字数: </strong>
    <span class="word-count"></span>

    &nbsp;

    <strong>字符数: </strong>
    <span class="character-count"></span>
</div`;

class WordCountWidget extends api.TabAwareWidget {
    get position() { return 100; } // higher value means position towards the bottom/right
    
    get parentWidget() { return 'center-pane'; }
    
    doRender() {
        this.$widget = $(TPL);
        this.$wordCount = this.$widget.find('.word-count');
        this.$characterCount = this.$widget.find('.character-count');
        return this.$widget;
    }
    
    async refreshWithNote(note) {
        if (note.type !== 'text' || !note.hasLabel('字数统计')) { 
            // 只在有 "字数统计" 这个标签的笔记里才显示组件
            this.toggleInt(false); // 隐藏
            
            return;
        }
        
        this.toggleInt(true); // 显示
        
        const {content} = await note.getNoteComplement();
        
        const text = $(content).text(); // get plain text only
        
        const counts = this.getCounts(text);

        this.$wordCount.text(counts.words);
        this.$characterCount.text(counts.characters);
    }
    
    getCounts(text) {
        const chunks = text
            .split(/[\s-+:,/\\]+/)
            .filter(chunk => chunk !== '');
        
        let words;
        
        if (chunks.length === 1 && chunks[0] === '') {
            words = 0;
        }
        else {
            words = chunks.length;
        }
        
        const characters = chunks.join('').length;
        
        return {words, characters};
    }
    
    async entitiesReloadedEvent({loadResults}) {
        if (loadResults.isNoteContentReloaded(this.noteId)) {
            this.refresh();
        }
    }
}

module.exports = new WordCountWidget();