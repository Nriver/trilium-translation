/*
 * sticky notes
 * https://github.com/zadam/trilium/issues/1993
 * 这个是Trilium Notes的作者zadam在一个issue里写的一个小组件
 * 给笔记加上 #sticky 标签就能在右边固定显示（需要重启Trilium），虽然效果有点简陋
 */

let TPL = `
<div>
    <style>
    .stickyNote {
        border: 1px solid var(--main-border-color);
        min-height:6em;
        resize: vertical;
        width: 100%;padding:10px;
        font-family:var(--font-code); 
    }
    </style>
</div>
`

class stickyWidget extends api.CollapsibleWidget {
    
    get widgetTitle() {
        return "固定笔记"
    }
    
    get parentWidget() {
        return "right-pane"
    }
    
    async doRenderBody() {
      const stickyNotes = await api.searchForNotes('#sticky');   

      const $content = $("<div>"); 
        
      for (let i = 0; i < stickyNotes.length && i < 3; i++) {
          const note = stickyNotes[i];
  
          $content.append(await note.getContent());
       }
        
       this.$body.html(TPL).append($content);
    }    
}

module.exports = new stickyWidget()