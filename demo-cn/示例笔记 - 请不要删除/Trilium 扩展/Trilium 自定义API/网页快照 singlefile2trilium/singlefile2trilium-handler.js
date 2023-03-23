// HowTo:
//  1- Add this file to trilium as a `JS Backend` code note.
//  2- Set label `customRequestHandler` to 'singlefile2trilium'.
api.log("api 调用 singlefile2trilium");

// 安全考虑，默认不启用。
// 如果要启用，请先修改 SECRET_PASSWORD 然后再去掉这个return。
return
var SECRET_PASSWORD = '你的密码';

/*
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">

<iframe id="r-iframe" sandbox="allow-same-origin allow-scripts allow-popups allow-forms" style="width:100%; flex-grow: 1; border:none;" src="data:text/html;charset=utf-8,%%CONTENT%%" sandbox=""></iframe>
*/

const template = `

<iframe id="r-iframe" style="width:100%" src="data:text/html;charset=utf-8,%%CONTENT%%" sandbox=""></iframe>

<script>
    var iframe = document.getElementById('r-iframe');

    function pageY(elem) {
        return elem.offsetParent ? (elem.offsetTop + pageY(elem.offsetParent)) : elem.offsetTop;
    }

    function resizeIframe() {
        var height = document.documentElement.clientHeight;
        height -= pageY(iframe) + 20 ;
        height = (height < 0) ? 0 : height;
        iframe.style.height = height + 'px';
    }

    iframe.onload = resizeIframe;
    window.onresize = resizeIframe;
</script>
`;

const {req, res} = api;
const {secret, title, url, content} = req.body;

api.log('secret', secret);

if (req.method == 'POST' && secret === SECRET_PASSWORD) {
    api.log("==========================");

    //const todayNote = await api.getDateNote(today);
    const todayNote = api.getTodayNote();
    
    // create render note
    const renderNote = (api.createNewNote({
        parentNoteId: todayNote.noteId,
        title: title,
        content: '',
        type: 'render'
    })).note;
    renderNote.setLabel('clipType', 'singlefile2trilium');
    renderNote.setLabel('pageUrl', url);
    renderNote.setLabel('pageTitle', title);

    // create child `content.html`
    var wrapped_content = template.replace("%%CONTENT%%", encodeURIComponent(content));
    const htmlNote = (api.createNewNote({
        parentNoteId: renderNote.noteId,
        title: 'content.html',
        content: wrapped_content,
        type: 'file',
        mime: 'text/html'
    })).note;
    htmlNote.setLabel('archived');

    // link renderNote to htmlNote
    renderNote.setRelation('renderNote', htmlNote.noteId);

    res.send(201); // http 201: created
}
else {
    api.log("没有使用POST请求或密码不对");
    res.send(400); // http 400: bad request
}
