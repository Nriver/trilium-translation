import os
import re
import shutil

from settings import BASE_FOLDER, PATCH_FOLDER, TRANSLATOR_URL, LANG
from translations import translation_dict

script_path = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = f'{BASE_FOLDER}trilium-src/'
CLIENT_PATH = f'{BASE_FOLDER}trilium-linux-x64/'
PATCH_FOLDER = PATCH_FOLDER

TARGET_PATH = f'{CLIENT_PATH}resources/app/'
os.chdir(BASE_PATH)

TRANSLATOR_LABEL = translation_dict['translator']

if not os.path.exists(f'{TARGET_PATH}src/public/'):
    os.system(f'cd {CLIENT_PATH}resources && asar extract app.asar ./app/')
# 是否要翻译属性标签(可能会影响代码, 小心使用)
# Whether to translate the note tag(may BREAK the code, use with care)
TRANSLATE_NOTE_TAG = True

# 用 {{}} 来标记要翻译的内容
# use {{}} to mark the content you want to translate

# .js文件修改源码再编译 复制
# .js files need to use the source code to compile
# .ejs 文件直接修改
# .ejs files will directly use the release files


pat = re.compile('{{(.*?)}}', flags=re.DOTALL + re.MULTILINE)

# check which file is not in use anymore
missing_files = []
# check which translation is not in use anymore
used_translations = [
    'translator',
]
unused_translations = []
missing_translations = []


def translate(m):
    s = m.group(1)
    trans = translation_dict.get(s, None)
    if not trans:
        trans = s
        missing_translations.append(s)
    else:
        used_translations.append(s)

    return trans


def replace_in_file(file_path, translation, base_path=BASE_PATH):
    file_full_path = os.path.join(base_path, file_path)
    if not os.path.exists(file_full_path):
        missing_files.append(file_path)
        return

    with open(file_full_path, 'r') as f:
        content = f.read()

    for ori_mark in translation:
        ori_content = ori_mark.replace('{{', '').replace('}}', '')

        trans = pat.sub(translate, ori_mark)

        # print('ori_content', ori_content)
        # print('11111trans', trans)

        content = content.replace(ori_content, trans)

    with open(file_full_path, 'w') as f:
        f.write(content)


# 关于页面添加翻译者信息
# add translator info in about page :)
print('add translator info in about page.')
# before 0.53
# about_file_path = f'{TARGET_PATH}src/public/app/widgets/dialogs/about.js'
# 0.53.2
about_file_path = f'src/public/app/widgets/dialogs/about.js'
with open(about_file_path, 'r') as f:
    content = f.read()
    if TRANSLATOR_LABEL not in content:
        content = content.replace(
            '                </table>',
            f'\n                    <tr>\n                        <th>{TRANSLATOR_LABEL}:</th>\n                        <td><a href="{TRANSLATOR_URL}" class="external">{TRANSLATOR_URL}</a></td>\n                    </tr>\n                </table>',
        )
with open(about_file_path, 'w') as f:
    f.write(content)

# Removed in 0.58.2
# # 修复flex布局下部分界面中文自动换行的问题
# # 选项界面
# file_path = 'src/public/app/widgets/dialogs/options.js'
# with open(file_path, 'r') as f:
#     content = f.read()
#     target_element = '<ul class="nav nav-tabs flex-column">'
#     if target_element in content:
#         content = content.replace('<ul class="nav nav-tabs flex-column">',
#                                   '<ul class="nav nav-tabs flex-column" style="white-space: nowrap;">')
# with open(file_path, 'w') as f:
#     f.write(content)

# 修复受保护的会话输入密码框样式
file_path = 'src/public/app/widgets/dialogs/protected_session_password.js'
with open(file_path, 'r') as f:
    content = f.read()
    target_element = '                    <div class="form-group">\n                        <label>'
    if target_element in content:
        content = content.replace(
            '                    <div class="form-group">\n                        <label>',
            '                    <div class="form-group">\n                        <label style="width: -webkit-fill-available">',
        )
with open(file_path, 'w') as f:
    f.write(content)

# Removed in 0.58.2
# # 修复设置界面样式
# file_path = 'src/public/app/widgets/dialogs/options.js'
# with open(file_path, 'r') as f:
#     content = f.read()
#     target_element = '                    <br/>\n                    <div class="tab-content">'
#     if target_element in content:
#         content = content.replace('                    <br/>\n                    <div class="tab-content">',
#                                   '                    <br/>\n                    <div class="tab-content" style="width: -webkit-fill-available">')
# with open(file_path, 'w') as f:
#     f.write(content)

# 升级属性
file_path = 'src/public/app/widgets/ribbon_widgets/promoted_attributes.js'
with open(file_path, 'r') as f:
    content = f.read()
    target_element = '<div class="promoted-attribute-cell">'
    new_element = '<div class="promoted-attribute-cell" style="white-space: nowrap;">'
    if target_element in content:
        content = content.replace(target_element, new_element)
with open(file_path, 'w') as f:
    f.write(content)

# 0.61 新增
# 附件功能 去掉复数名词后面的 s 字母
file_path = 'src/public/app/services/utils.js'
with open(file_path, 'r') as f:
    content = f.read()
    target_element = "const plural = (count, name) => `${count} ${name}${count > 1 ? 's' : ''}`;"
    new_element = "const plural = (count, name) => `${count} ${name}`;"
    if target_element in content:
        content = content.replace(target_element, new_element)
with open(file_path, 'w') as f:
    f.write(content)

# 下面一堆是正则匹配规则, 读代码的时候下面这一段可以跳过, 直接看最后面几行
# TL;DR, the following codes are regex matches, you can jump to the last few lines.

file_path = 'src/views/desktop.ejs'
translation = [
    '>{{Trilium Notes}}<',
    '>{{Trilium requires JavaScript to be enabled.}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/login.ejs'
translation = [
    '>{{Login}}<',
    '>{{Trilium login}}<',
    '>{{Username}}<',
    '>{{Password}}<',
    '> {{Remember me}}',
    '{{Username and / or password are incorrect. Please try again.}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/mobile.ejs'
translation = [
    '>{{Trilium Notes}}<',
    '>{{Trilium requires JavaScript to be enabled.}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/set_password.ejs'
translation = [
    '>{{Login}}<',
    '>{{Set password}}<',
    '>{{Before you can start using Trilium from web, you need to set a password first. You will then use this password to login.}}<',
    '>{{Password}}<',
    '>{{Password confirmation}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/setup.ejs'
translation = [
    '>{{Setup}}<',
    '>{{Trilium requires JavaScript to be enabled.}}<',
    '>{{Trilium Notes setup}}<',
    '>{{Next}}<',
    '>{{New document}}<',
    '>{{Username}}<',
    '>{{Password}}<',
    '>{{Repeat password}}<',
    '>{{Theme}}<',
    '>{{white}}<',
    '>{{dark}}<',
    '>{{light}}<',
    '>{{black}}<',
    '>{{Theme can be later changed in Options -> Appearance.}}<',
    '>{{Back}}<',
    '>{{Finish setup}}<',
    '>{{Document initialization in progress}}<',
    '>{{You will be shortly redirected to the application.}}<',
    '>{{Sync from Desktop}}<',
    '>{{This setup needs to be initiated from the desktop instance:}}<',
    '>{{please open your desktop instance of Trilium Notes}}<',
    '>{{click on Options button in the top right}}<',
    '>{{click on Sync tab}}<',
    '>{{configure server instance address to the: }}<',
    '>{{ and click save.}}<',
    '>{{click on "Test sync" button}}<',
    ">{{once you've done all this, click }}<",
    '>{{here}}<',
    '>{{Sync from Server}}<',
    '>{{Please enter Trilium server address and credentials below. This will download the whole Trilium document from server and setup sync to it. Depending on the document size and your connection speed, this may take a while.}}<',
    '>{{Trilium server address}}<',
    '>{{Proxy server (optional)}}<',
    '>{{Note:}}<',
    '>{{ If you leave proxy setting blank, system proxy will be used (applies to desktop/electron build only)}}<',
    '>{{Sync in progress}}<',
    ">{{Sync has been correctly set up. It will take some time for the initial sync to finish. Once it's done, you'll be redirected to the login page.}}<",
    '>{{N/A}}<',
    '{{Username and / or password are incorrect. Please try again.}}',
    "{{I'm a new user, and I want to create a new Trilium document for my notes}}",
    '{{I have a desktop instance already, and I want to set up sync with it}}',
    '{{I have a server instance already, and I want to set up sync with it}}',
    "{{You're almost done with the setup. The last thing is to choose username and password using which you'll login to the application.}}",
    '{{This password is also used for generating encryption key which encrypts protected notes.}}',
    'placeholder="{{Choose alphanumeric username}}"',
    'placeholder="{{Username}}"',
    'placeholder="{{Password}}"',
    '{{Outstanding sync items}}:',
    '{{Open your desktop instance of Trilium Notes.}}',
    '>{{From the Trilium Menu, click Options.}}<',
    '>{{Click on Sync tab.}}<',
    '>{{Change server instance address to: }}<',
    '>{{Click "Test sync" button to verify connection is successfull.}}<',
    ">{{Once you've completed these steps, click }}<",
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/share/404.ejs'
translation = [
    '>{{Not found}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/share/page.ejs'
translation = [
    '>{{This note was originally clipped from }}<',
    '>{{This note has no content.}}<',
    '>{{Child notes: }}<',
    '    {{parent: }}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/menus/electron_context_menu.js'
translation = [
    'title: `{{Add "${params.misspelledWord}" to dictionary}}`',
    'title: `{{Cut}}',
    'title: `{{Copy link}}`,',
    'title: `{{Copy}} <kbd>',
    'title: `{{Copy link}}`',
    'title: `{{Paste as plain text}}',
    'title: `{{Paste}}',
    'title: {{`Search for "${shortenedSelection}" with ${searchEngineName}`}}',
]
replace_in_file(file_path, translation)

# file_path = 'src/public/app/widgets/dialogs/about.js'
# 0.53.2
file_path = 'src/public/app/widgets/dialogs/about.js'
translation = [
    '>{{About Trilium Notes}}<',
    '>{{Homepage:}}<',
    '>{{App version:}}<',
    '>{{DB version:}}<',
    '>{{Sync version:}}<',
    '>{{Build date:}}<',
    '>{{Build revision:}}<',
    '>{{Data directory:}}<',
]
# replace_in_file(file_path, translation, TARGET_PATH)
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/add_link.js'
translation = [
    '>{{Add link}}<',
    '>{{Note}}<',
    '>{{Link title}}<',
    '>{{Add link}} <',
    '>{{enter}}<',
    'title="{{Help on links}}"',
    '{{search for note by its name}}',
    "{{link title mirrors the note's current title}}",
    '{{link title can be changed arbitrarily}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/branch_prefix.js'
translation = [
    '>{{Edit branch prefix}}<',
    '>{{Prefix}}: <',
    '>{{Save}}<',
    'title="{{Help on Tree prefix}}"',
    'showMessage("{{Branch prefix has been saved.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/bulk_actions.js'
translation = [
    '>{{Bulk actions}}<',
    '>{{Bulk assign attributes}}<',
    '>{{Affected notes: }}<',
    '                        {{Include descendants of the selected notes}}',
    '>{{Available actions}}<',
    '>{{Chosen actions}}<',
    '>{{Execute bulk actions}}<',
    '>{{None yet ... add an action by clicking one of the available ones above.}}<',
    'showMessage("{{Bulk actions have been executed successfully.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/clone_to.js'
translation = [
    '>{{Clone notes to ...}}<',
    '>{{Notes to clone}}<',
    '    {{Target parent note}}',
    '    {{Prefix (optional)}}',
    '>{{Clone to selected note }}<',
    '>{{enter}}<',
    'title="{{Help on links}}"',
    'title="{{Cloned note will be shown in note tree with given prefix}}"',
    '{{search for note by its name}}',
    'showMessage({{`Note "${clonedNote.title}" has been cloned into ${targetNote.title}`}}',
    '    logError("{{No path to clone to.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/confirm.js'
translation = [
    '>{{Confirmation}}<',
    '>{{Cancel}}<',
    '>{{OK}}<',
    '''.attr("title", "{{If you don't check this, the note will be only removed from the relation map.}}")''',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/delete_notes.js'
translation = [
    '>{{Delete notes preview}}<',
    '>{{Following notes will be deleted (}}<',
    '>{{Following relations will be broken and deleted (}}<',
    '>{{Cancel}}<',
    '>{{OK}}<',
    '    {{delete also all clones}}',
    '''title="{{Normal (soft) deletion only marks the notes as deleted and they can be undeleted (in recent changes dialog) within a period of time. Checking this option will erase the notes immediatelly and it won't be possible to undelete the notes.}}"''',
    '''        {{erase notes permanently (can't be undone). This will force application reload.}}''',
    '{{can be undone in recent changes}}',
    "{{erase notes permanently (can't be undone), including all clones. This will force application reload.}}",
    '{{No note will be deleted (only clones).}}',
    '.append(`{{Note}} `)',
    '.append(`{{ (to be deleted) is referenced by relation <code>${attr.name}</code> originating from }}`)',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/export.js'
translation = [
    '>{{Export note "}}<',
    '    {{this note and all of its descendants}}',
    '    {{HTML in ZIP archive - this is recommended since this preserves all the formatting.}}',
    '    {{OPML v1.0 - plain text only}}',
    '    {{OMPL v2.0 - allows also HTML}}',
    '    {{only this note without its descendants}}',
    '    {{HTML - this is recommended since this preserves all the formatting.}}',
    '>{{Export}}<',
    '{{this preserves most of the formatting.}}',
    '{{outliner interchange format for text only. Formatting, images and files are not included.}}',
    'title: "{{Export status}}"',
    'showError("{{Choose export type first please}}"',
    "throw new Error(`{{Unrecognized type}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/help.js'
translation = [
    '>{{Help (full documentation is available }}<',
    '>{{online}}<',
    '>{{Note navigation}}<',
    '>{{UP}}<',
    '>{{DOWN}}<',
    '>{{ - go up/down in the list of notes}}<',
    '>{{LEFT}}<',
    '>{{RIGHT}}<',
    '>{{ - collapse/expand node}}<',
    # shortcuts placeholder string. DO NOT MODIFY!
    # 这个 not set 是快捷键占位符, 千万别改!
    # '>not set<',
    '>{{ - go back / forwards in the history}}<',
    '>{{ - show }}<',
    '>{{"Jump to" dialog}}<',
    '>{{ - scroll to active note}}<',
    '>{{Backspace}}<',
    '>{{ - jump to parent note}}<',
    '>{{ - collapse whole note tree}}<',
    '>{{ - collapse sub-tree}}<',
    '>{{Tab shortcuts}}<',
    '>{{CTRL+click}}<',
    '>{{ (or middle mouse click) on note link opens note in a new tab}}<',
    '>{{ open empty tab}}<',
    '>{{ close active tab}}<',
    '>{{ activate next tab}}<',
    '>{{ activate previous tab}}<',
    '>{{Creating notes}}<',
    '>{{ - create new note after the active note}}<',
    '>{{ - create new sub-note into active note}}<',
    '>{{Moving / cloning notes}}<',
    '>{{ - move note up/down in the note list}}<',
    '>{{ - move note up in the hierarchy}}<',
    '>{{ - multi-select note above/below}}<',
    '>{{ - select all notes in the current level}}<',
    '>{{Shift+click}}<',
    '>{{ - select note}}<',
    '>{{ - copy active note (or current selection) into clipboard (used for }}<',
    '>{{cloning}}<',
    '>{{ - cut current (or current selection) note into clipboard (used for moving notes)}}<',
    '>{{ - paste note(s) as sub-note into active note (which is either move or clone depending on whether it was copied or cut into clipboard)}}<',
    '>{{ - delete note / sub-tree}}<',
    '>{{Editing notes}}<',
    '>{{ will switch back from editor to tree pane.}}<',
    '>{{Ctrl+K}}<',
    '>{{ - create / edit external link}}<',
    '>{{ - create internal link}}<',
    '>{{ - follow link under cursor}}<',
    '>{{ - insert current date and time at caret position}}<',
    '>{{ - jump away to the tree pane and scroll to active note}}<',
    '>{{Markdown-like autoformatting}}<',
    '>{{ etc. followed by space for headings}}<',
    '>{{ or }}<',
    '>{{ followed by space for bullet list}}<',
    '>{{ followed by space for numbered list}}<',
    '>{{start a line with }}<',
    '>{{ followed by space for block quote}}<',
    '>{{Troubleshooting}}<',
    '>{{ - reload Trilium frontend}}<',
    '>{{ - show developer tools}}<',
    '>{{ - show SQL console}}<',
    '>{{Other}}<',
    '>{{ - Zen mode - display only note editor, everything else is hidden}}<',
    '>{{ - focus on quick search input}}<',
    '>{{ - in page search}}<',
    '- {{edit <a class="external" href="https://github.com/zadam/trilium/wiki/Tree concepts#prefix">prefix</a> of active note clone}}<',
    '{{Only in desktop (electron build)}}:',
    '{{in tree pane will switch from tree pane into note title. Enter from note title will switch focus to text editor.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/import.js'
translation = [
    '>{{Import into note}}<',
    '>{{Choose import file}}<',
    '>{{Content of the selected file(s) will be imported as child note(s) into }}<',
    '>{{Options:}}<',
    '>{{Safe import}}<',
    '>{{Read contents of <code>.zip</code>, <code>.enex</code> and <code>.opml</code> archives.}}<',
    '>{{If you check this option, Trilium will attempt to shrink the imported images by scaling and optimization which may affect the perceived image quality. If unchecked, images will be imported without changes.}}<',
    ">{{This doesn't apply to }}<",
    '>{{ imports with metadata since it is assumed these files are already optimized.}}<',
    '>{{Shrink images}}<',
    "{{Import HTML, Markdown and TXT as text notes if it's unclear from metadata}}",
    "> {{Import recognized code files (e.g. <code>.json</code>) as code notes if it's unclear from metadata}}",
    '>{{Import}}<',
    'title="{{Trilium <code>.zip</code> export files can contain executable scripts which may contain harmful behavior. Safe import will deactivate automatic execution of all imported scripts. Uncheck &quot;Safe import&quot; only if the imported tar archive is supposed to contain executable scripts and you completely trust the contents of the import file.}}"',
    'title="{{If this is checked then Trilium will read <code>.zip</code>, <code>.enex</code> and <code>.opml</code> files and create notes from files insides those archives. If unchecked, then Trilium will attach the archives themselves to the note.}}"',
    '''title="{{<p>If you check this option, Trilium will attempt to shrink the imported images by scaling and optimization which may affect the perceived image quality. If unchecked, images will be imported without changes.</p><p>This doesn't apply to <code>.zip</code> imports with metadata since it is assumed these files are already optimized.</p>}}"''',
    '''{{Replace underscores with spaces in imported note names}}''',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/include_note.js'
translation = [
    '>{{Include note}}<',
    '>{{Note}}<',
    '>{{Include note }}<',
    '>{{enter}}<',
    '{{search for note by its name}}',
    '    logError("{{No noteId to include.}}"',
    '{{Box size of the included note:}}',
    '{{small (~ 10 lines)}}',
    '{{medium (~ 30 lines)}}',
    '{{full (box shows complete text)}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/info.js'
translation = [
    '>{{Info message}}<',
    '>{{OK}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/jump_to_note.js'
translation = [
    '>{{Jump to note}}<',
    '>{{Note}}<',
    '>{{Search in full text }}<',
    '>{{Ctrl+Enter}}<',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/markdown_import.js'
translation = [
    '>{{Markdown import}}<',
    ">{{Because of browser sandbox it's not possible to directly read clipboard from JavaScript. Please paste the Markdown to import to textarea below and click on Import button}}<",
    '>{{Import }}<',
    '>{{Ctrl+Enter}}<',
    'showMessage("{{Markdown content has been imported into the document.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/move_to.js'
translation = [
    '>{{Move notes to ...}}<',
    '>{{Notes to move}}<',
    '    {{Target parent note}}',
    '>{{Move to selected note }}<',
    '>{{enter}}<',
    '{{search for note by its name}}',
    'showMessage({{`Selected notes have been moved into ${parentNote.title}`}}',
    '    logError("{{No path to move to.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/revisions.js'
translation = [
    '>{{Note revisions}}<',
    '>{{Delete all revisions}}<',
    '>{{Dropdown trigger}}<',
    'title="{{Delete all revisions of this note}}"',
    'title="{{Help on Note revisions}}"',
    '>{{Restore this revision}}<',
    '>{{Delete this revision}}<',
    '>{{Download}}<',
    '{{This revision was last edited on}} ',
    '{{Do you want to restore this revision? This will overwrite current title/content of the note with this revision.}}',
    '{{Do you want to delete this revision? This action will delete revision title and content, but still preserve revision metadata.}}',
    "{{Preview isn't available for this note type.}}",
    '{{Do you want to delete all revisions of this note? This action will erase revision title and content, but still preserve revision metadata.}}',
    "showMessage('{{Note revision has been restored.}}'",
    "showMessage('{{Note revision has been deleted.}}'",
    "showMessage('{{Note revisions has been deleted.}}'",
    '"{{No revisions for this note yet...}}"',
    '.text("{{File size:}}")',
    '.text("{{Preview}}:")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/note_type_chooser.js'
translation = [
    '>{{Choose note type}}<',
    '{{Choose note type / template of the new note:}}',
    '>{{Dropdown trigger}}<',
]
replace_in_file(file_path, translation)

# Removed in 0.58.2
# file_path = 'src/public/app/widgets/dialogs/options.js'
# translation = [
#     '>{{Options}}<',
#     '>{{Appearance}}<',
#     '>{{Shortcuts}}<',
#     '>{{Keyboard shortcuts}}<',
#     '>{{Text notes}}<',
#     '>{{Code notes}}<',
#     # removed from 0.50
#     # '>{{Username & password}}<',
#     '>{{Password}}<',
#     '>{{ETAPI}}<',
#     '>{{Backup}}<',
#     '>{{Sync}}<',
#     '>{{Other}}<',
#     '>{{Advanced}}<',
# ]
# replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/password_not_set.js'
translation = [
    '>{{Password is not set}}<',
    '{{Protected notes are encrypted using a user password, but password has not been set yet.}}',
    '''{{To be able to protect notes, <a class="open-password-options-button" href="javascript:">\n                    click here to open the Options dialog</a> and set your password.}}''',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/prompt.js'
translation = [
    '>{{Prompt}}<',
    '>{{OK }}<',
    '>{{enter}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/protected_session_password.js'
translation = [
    '>{{Protected session}}<',
    '{{To proceed with requested action you need to start protected session by entering password:}}',
    '>{{Start protected session }}<',
    '>{{enter}}<',
    'title="{{Help on Protected notes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/recent_changes.js'
translation = [
    '>{{Recent changes}}<',
    '{{Erase deleted notes now}}',
    'showMessage("{{Deleted notes have been erased.}}"',
    '{{No changes yet ...}}',
    '{{Do you want to undelete this note and its sub-notes?}}',
    'text("{{undelete}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/sort_child_notes.js'
translation = [
    '>{{Sort children by ...}}<',
    '>{{Sorting criteria}}<',
    '>{{Sorting direction}}<',
    '>{{Folders}}<',
    '>{{Natural Sort}}<',
    '>{{Sort }}<',
    '>{{enter}}<',
    '    {{title}}',
    '    {{date created}}',
    '    {{date modified}}',
    '    {{ascending}}',
    '    {{descending}}',
    '    {{sort folders at the top}}',
    '{{sort with respect to different character sorting and collation rules in different languages or regions.}}',
    '{{Natural sort language}}',
    '{{The language code for natural sort, e.g. "zh-CN" for Chinese.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/dialogs/upload_attachments.js'
translation = [
    '>{{Upload attachments to note}}<',
    '>{{Choose files}}<',
    '>{{Files will be uploaded as attachments into }}<',
    '>{{Options:}}<',
    '>{{If you check this option, Trilium will attempt to shrink the uploaded images by scaling and optimization which may affect the perceived image quality. If unchecked, images will be uploaded without changes.}}<',
    '>{{Shrink images}}<',
    '>{{Upload}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/advanced/consistency_checks.js'
translation = [
    '>{{Consistency Checks}}<',
    '>{{Find and fix consistency issues}}<',
    'showMessage("{{Finding and fixing consistency issues...}}"',
    'showMessage("{{Consistency issues should be fixed.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/advanced/database_anonymization.js'
translation = [
    '>{{Database Anonymization}}<',
    '>{{Full Anonymization}}<',
    '>{{Save fully anonymized database}}<',
    '>{{Light Anonymization}}<',
    '>{{Existing anonymized databases}}<',
    '{{This action will create a new copy of the database and anonymize it (remove all note content and leave only structure and some non-sensitive metadata)\n        for sharing online for debugging purposes without fear of leaking your personal data.}}',
    '>{{This action will create a new copy of the database and do a light anonymization on it — specifically only content of all notes will be removed, but titles and attributes will remain. Additionally, custom JS frontend/backend script notes and custom widgets will remain. This provides more context to debug the issues.}}<',
    '>{{You can decide yourself if you want to provide a fully or lightly anonymized database. Even fully anonymized DB is very useful, however in some cases lightly anonymized database can speed up the process of bug identification and fixing.}}<',
    '>{{Save lightly anonymized database}}<',
    'showMessage({{`Created fully anonymized database in ${resp.anonymizedFilePath}`}}',
    'showMessage({{`Created lightly anonymized database in ${resp.anonymizedFilePath}`}}',
    'showMessage("{{Creating fully anonymized database...}}"',
    'showMessage("{{Creating lightly anonymized database...}}"',
    'showError("{{Could not create anonymized database, check backend logs for details}}"',
    '"{{no anonymized database yet}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/advanced/database_integrity_check.js'
translation = [
    '>{{Database Integrity Check}}<',
    '>{{This will check that the database is not corrupted on the SQLite level. It might take some time, depending on the DB size.}}<',
    '>{{Check database integrity}}<',
    'showMessage(`{{Integrity check failed:}}',
    'showMessage("{{Checking database integrity...}}"',
    'showMessage("{{Integrity check succeeded - no problems found.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/advanced/sync.js'
translation = [
    '>{{Sync}}<',
    '>{{Force full sync}}<',
    '>{{Fill entity changes records}}<',
    'showMessage("{{Full sync triggered}}"',
    'showMessage("{{Filling entity changes rows...}}"',
    'showMessage("{{Sync rows filled successfully}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/advanced/vacuum_database.js'
translation = [
    '>{{Vacuum Database}}<',
    '>{{Vacuum database}}<',
    '>{{This will rebuild the database which will typically result in a smaller database file. No data will be actually changed.}}<',
    'showMessage("{{Vacuuming database...}}"',
    'showMessage("{{Database has been vacuumed}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/fonts.js'
translation = [
    '>{{Fonts}}<',
    '>{{Main Font}}<',
    '>{{Font family}}<',
    '>{{Size}}<',
    '>{{Note Tree Font}}<',
    '>{{Note Detail Font}}<',
    '>{{Monospace (code) Font}}<',
    '>{{Note that tree and detail font sizing is relative to the main font size setting.}}<',
    '>{{Not all listed fonts may be available on your system.}}<',
    '>{{reload frontend}}<',
    '{{To apply font changes, click on}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/max_content_width.js'
translation = [
    '>{{Content Width}}<',
    '>{{Trilium by default limits max content width to improve readability for maximized screens on wide screens.}}<',
    '>{{Max content width in pixels}}<',
    '>{{reload frontend}}<',
    '{{To apply content width changes, click on}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/native_title_bar.js'
translation = [
    '>{{Native Title Bar (requires app restart)}}<',
    '>{{enabled}}<',
    '>{{disabled}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/ribbon.js'
translation = [
    '>{{Ribbon widgets}}<',
    '{{Promoted Attributes ribbon tab will automatically open if promoted attributes are present on the note}}',
    '{{Edited Notes ribbon tab will automatically open on day notes}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/theme.js'
translation = [
    '>{{Theme}}<',
    '>{{Override theme fonts}}<',
    "title: '{{Light}}",
    "title: '{{Dark}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/appearance/zoom_factor.js'
translation = [
    '>{{Zoom Factor (desktop build only)}}<',
    '>{{Zooming can be controlled with CTRL+- and CTRL+= shortcuts as well.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/backup.js'
translation = [
    'return "{{Backup}}"',
    '>{{Automatic backup}}<',
    '>{{Trilium can back up the database automatically:}}<',
    '    {{Enable daily backup}}',
    '    {{Enable weekly backup}}',
    '    {{Enable monthly backup}}',
    '''>{{It's recommended to keep the backup turned on, but this can make application startup slow with large databases and/or slow storage devices.}}<''',
    '>{{Backup now}}<',
    '>{{Backup database now}}<',
    'showMessage(`{{Database has been backed up to }}',
    'showMessage("{{Options changed have been saved.}}"',
    '>{{Existing backups}}<',
    '"{{no backup yet}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/code_notes/code_auto_read_only_size.js'
translation = [
    '>{{Automatic Read-Only Size}}<',
    '>{{Automatic read-only note size is the size after which notes will be displayed in a read-only mode (for performance reasons).}}<',
    '>{{Automatic read-only size (code notes)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/code_notes/code_mime_types.js'
translation = [
    '>{{Available MIME types in the dropdown}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/code_notes/vim_key_bindings.js'
translation = [
    '>{{Use vim keybindings in code notes (no ex mode)}}<',
    '{{Enable Vim Keybindings}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/code_notes/wrap_lines.js'
translation = [
    '>{{Wrap lines in code notes}}<',
    '{{Enable Line Wrap (change might need a frontend reload to take effect)}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/etapi.js'
translation = [
    '{{ETAPI is a REST API used to access Trilium instance programmatically, without UI.}}',
    """{{See more details on <a href="https://github.com/zadam/trilium/wiki/ETAPI">wiki</a> and <a onclick="window.open('etapi/etapi.openapi.yaml')" href="etapi/etapi.openapi.yaml">ETAPI OpenAPI spec</a>.}}""",
    '>{{Create new ETAPI token}}<',
    '>{{Existing tokens}}<',
    '>{{There are no tokens yet. Click on the button above to create one.}}<',
    '>{{Token name}}<',
    '>{{Created}}<',
    '>{{Actions}}<',
    'title: "{{New ETAPI token}}"',
    'title: "{{ETAPI token created}}"',
    '{{Copy the created token into clipboard. Trilium stores the token hashed and this is the last time you see it.}}',
    'title: "{{Rename token}}"',
    'title="{{Rename this token}}"',
    'title="{{Delete / deactive this token}}"',
    '''message: "{{Please enter new token's name}}"''',
    '''defaultValue: "{{new token}}"''',
    '''    alert("{{Token name can't be empty}}"''',
    '{{Are you sure you want to delete ETAPI token}}',
    'title="{{Delete / deactivate this token}}"',
    '''showError("{{Token name can't be empty}}"''',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/images/images.js'
translation = [
    '>{{Images}}<',
    '{{Download images automatically for offline use.}}',
    '>{{(pasted HTML can contain references to online images, Trilium will find those references and download the images so that they are available offline)}}<',
    '{{Enable image compression}}',
    '>{{Max width / height of an image in pixels (image will be resized if it exceeds this setting).}}<',
    '>{{JPEG quality (10 - worst quality, 100 best quality, 50 - 85 is recommended)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/options_widget.js'
translation = [
    'title: "{{Options status}}"',
    'message: "{{Options change have been saved.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/attachment_erasure_timeout.js'
translation = [
    '>{{Attachment Erasure Timeout}}<',
    '{{Attachments get automatically deleted (and erased) if they are not referenced by their note anymore after a defined time out.}}',
    '{{Erase attachments after X seconds of not being used in its note}}',
    '{{You can also trigger erasing manually (without considering the timeout defined above)}}',
    '{{Erase unused attachment notes now}}',
    'showMessage("{{Unused attachments have been erased.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/network_connections.js'
translation = [
    '>{{Network Connections}}<',
    '{{Check for updates automatically}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/note_erasure_timeout.js'
translation = [
    '>{{Note Erasure Timeout}}<',
    '>{{Erase notes after X seconds}}<',
    '>{{You can also trigger erasing manually:}}<',
    '>{{Erase deleted notes now}}<',
    'showMessage("{{Deleted notes have been erased.}}"',
    '{{Deleted notes (and attributes, revisions...) are at first only marked as deleted and it is possible to recover them \n    from Recent Notes dialog. After a period of time, deleted notes are "erased" which means \n    their content is not recoverable anymore. This setting allows you to configure the length \n    of the period between deleting and erasing the note.}}',
    '{{You can also trigger erasing manually (without considering the timeout defined above)}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/revisions_snapshot_interval.js'
translation = [
    '>{{Note Revisions Snapshot Interval}}<',
    '>{{Note revision snapshot time interval is time in seconds after which a new note revision will be created for the note. See }}<',
    '>{{wiki}}<',
    '> {{for more info.}}<',
    '>{{Note revision snapshot time interval (in seconds)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/search_engine.js'
translation = [
    '>{{Search Engine}}<',
    '>{{Custom search engine requires both a name and a URL to be set. If either of these is not set, DuckDuckGo will be used as the default search engine.}}<',
    '>{{Predefined search engine templates}}<',
    '>{{Bing}}<',
    '>{{Baidu}}<',
    '>{{Duckduckgo}}<',
    '>{{Google}}<',
    '>{{Custom search engine name}}<',
    '>{{Custom search engine URL should include <code>{keyword}</code> as a placeholder for the search term.}}<',
    '>{{Save}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/other/tray.js'
translation = [
    '>{{Tray}}<',
    '{{Enable tray (Trilium needs to be restarted for this change to take effect)}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/password.js'
translation = [
    'return "{{Password}}"',
    '>{{click here to reset it}}<',
    '>{{Old password}}<',
    '>{{New password}}<',
    '>{{New password confirmation}}<',
    '>{{Change password}}<',
    '    alert("{{Password has been reset. Please set new password}}"',
    '    alert("{{New passwords are not the same.}}"',
    '    alert("{{Password has been changed. Trilium will be reloaded after you press OK.}}"',
    '{{Please take care to remember your new password. Password is used for logging into the web interface and\n      to encrypt protected notes.}}',
    '{{If you forget your password, then all your protected notes are forever lost.}}',
    '{{In case you did forget your password}}',
    '"{{By resetting the password you will forever lose access to all your existing protected notes. Do you really want to reset the password?}}"',
    "'{{Change Password}}' : '{{Set Password}}')",
    '>{{Protected Session Timeout}}<',
    "{{Protected session timeout is a time period after which the protected session is wiped from\n        the browser's memory. This is measured from the last interaction with protected notes. See}}",
    '{{for more info.}}',
    '>{{Protected session timeout (in seconds)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/shortcuts.js'
translation = [
    'return "{{Shortcuts}}"',
    '>{{Keyboard Shortcuts}}<',
    '{{Multiple shortcuts for the same action can be separated by comma.}}',
    '{{See <a href="https://www.electronjs.org/docs/latest/api/accelerator">Electron documentation</a> for available modifiers and key codes.}}',
    '>{{Action name}}<',
    '>{{Shortcuts}}<',
    '>{{Default shortcuts}}<',
    '>{{Description}}<',
    '>{{Reload app to apply changes}}<',
    '>{{Set all shortcuts to the default}}<',
    '{{Do you really want to reset all keyboard shortcuts to the default?}}',
    '{{Type text to filter shortcuts...}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/spellcheck.js'
translation = [
    'return "{{Spellcheck}}"',
    '>{{Spell Check}}<',
    '>{{These options apply only for desktop builds, browsers will use their own native spell check. App restart is required after change.}}<',
    '{{Enable spellcheck}}',
    '>{{Language code(s)}}<',
    '>{{Multiple languages can be separated by comma, e.g. }}<',
    '>{{Available language codes: }}<',
    '>. {{Changes to the spell check options will take effect after application restart.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/sync.js'
translation = [
    'return "{{Sync}}"',
    '>{{Sync Configuration}}<',
    '>{{Server instance address}}<',
    '>{{Sync timeout (milliseconds)}}<',
    '>{{Sync proxy server (optional)}}<',
    '>{{Note:}}<',
    '> {{If you leave the proxy setting blank, the system proxy will be used (applies to desktop/electron build only)}}',
    '>{{Another special value is <code>noproxy</code> which forces ignoring even the system proxy and respectes <code>NODE_TLS_REJECT_UNAUTHORIZED</code>.}}<',
    '>{{Save}}<',
    '>{{Help}}<',
    '>{{Sync Test}}<',
    ">{{This will test the connection and handshake to the sync server. If the sync server isn't initialized, this will set it up to sync with the local document.}}<",
    '>{{Test sync}}<',
    'showMessage("{{Options changed have been saved.}}"',
    '"{{Sync server handshake failed, error:}} "',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/text_notes/heading_style.js'
translation = [
    '>{{Heading Style}}<',
    '>{{Plain}}<',
    '>{{Underline}}<',
    '>{{Markdown-style}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/text_notes/highlights_list.js'
translation = [
    '>{{Highlights List}}<',
    '{{You can customize the highlights list displayed in the right panel}}',
    '{{Bold font}}',
    '{{Italic font}}',
    '{{Underlined font}}',
    '{{Font with color}}',
    '{{Font with background color}}',
    '{{Highlists List visibility}}',
    '{{Highlights List visibility}}',
    '{{You can hide the hightlights widget per-note by adding a <code>#hideHighlightWidget</code> label.}}',
    '{{You can hide the highlights widget per-note by adding a <code>#hideHighlightWidget</code> label.}}',
    '{{You can configure a keyboard shortcut for quickly toggling the right pane (including Highlights) in the Options -> Shortcuts (name "toggleRightPane").}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/text_notes/table_of_contents.js'
translation = [
    '>{{Table of Contents}}<',
    '{{Table of contents will appear in text notes when the note has more than a defined number of headings. You can customize this number:}}',
    '>{{You can also use this option to effectively disable TOC by setting a very high number.}}<',
    '{{You can configure a keyboard shortcut for quickly toggling the right pane (including TOC) in the Options -> Shortcuts (name "toggleRightPane").}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/options/text_notes/text_auto_read_only_size.js'
translation = [
    '>{{Automatic Read-Only Size}}<',
    '>{{Automatic read-only note size is the size after which notes will be displayed in a read-only mode (for performance reasons).}}<',
    '>{{Automatic read-only size (text notes)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/services/search/expressions/ancestor.js'
translation = [
    '{{Unrecognized depth condition value}}',
    "`{{Subtree note '${this.ancestorNoteId}' was not not found.}}`",
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/import/enex.js'
translation = [
    'title: "{{resource}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/search/expressions/note_content_fulltext.js'
translation = [
    'throw new Error(`{{Note content can be searched only with operators: }}`',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/search/services/handle_parens.js'
translation = [
    'throw new Error("{{Did not find matching right parenthesis.}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

# no need for translate for now
file_path = 'src/services/search/services/search.js'
translation = []
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/sql_init.js'
translation = [
    "title: '{{root}}",
    'throw new Error("{{DB is already initialized}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/setup.js'
translation = [
    'throw new Error(`{{Could not setup sync since local sync protocol version is ${appInfo.syncVersion} while remote is ${response.syncVersion}. To fix this issue, use same Trilium version on all instances.}}`',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/sync.js'
translation = [
    'message: "{{No connection to sync server.}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/cloning.js'
translation = [
    '{{Note is deleted.}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/tray.js'
translation = [
    '{{Cannot move root note.}}',
    "? '{{Hide}}'",
    ": '{{Show}}'",
    "label: '{{Quit}}',",
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/tree.js'
translation = [
    '{{Cannot move root note.}}',
    '{{Cannot move anything into root parent.}}',
    '{{This note already exists in the target.}}',
    '{{Moving/cloning note here would create cycle.}}',
    '`{{Branch "${note.branchId}" was not found in note cache.}}`',
    '{{`Cannot move note to deleted parent note ${parentNoteId}`}}',
    '`{{Cannot create a branch for ${noteId} which is deleted.}}`',
]
replace_in_file(file_path, translation, TARGET_PATH)

# new note title
file_path = 'src/public/app/services/note_create.js'
translation = [
    ' "{{new note}}";',
    '`{{Note "${origNote.title}" has been duplicated}}`',
]
replace_in_file(file_path, translation)

# 0.48
file_path = 'src/public/app/layouts/desktop_layout.js'
translation = [
    'title("{{New note}}")',
    'title("{{Search}}")',
    'title("{{Jump to note}}")',
    'title("{{Show recent changes}}")',
    'title("{{Note Revisions}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/components/app_context.js'
translation = [
    'showMessage("{{Please wait for a couple of seconds for the save to finish, then you can try again.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/bundle.js'
translation = [
    '    logError("{{Widget initialization failed: }}"',
    '    toastService.showAndLogError({{`Execution of JS note "${note.title}" with ID ${bundle.noteId} failed with error: ${e.message}`}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/clipboard.js'
translation = [
    'showMessage("{{Note(s) have been copied into clipboard.}}"',
    'showMessage("{{Note(s) have been cut into clipboard.}}"',
    'throwError("{{Unrecognized clipboard mode=}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/components/entrypoints.js'
translation = [
    "title: '{{new note}}",
    'showMessage("{{Note executed}}"',
    '{{Note revision has been created.}}',
    '"{{Switching to desktop version}}"',
    '"{{Switching to mobile version}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/froca.js'
translation = [
    "`{{Search note '${note.noteId}' failed:}}",
    'throw new Error("{{Empty noteId}}"',
    "logError(`{{Not existing branch '${branchId}'}}`)",
    '    logError(`{{Could not find branchId for parent=${parentNoteId}, child=${childNoteId} since child does not exist}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/froca_updater.js'
translation = [
    "throw new Error(`{{Unknown entityName '${ec.entityName}'}}`",
    """throw new Error({{`Can't process entity ${JSON.stringify(ec)} with error ${e.message} ${e.stack}`}})""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/frontend_script_api.js'
translation = [
    'throw new Error("{{server error: }}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/frontend_script_api.js'
translation = [
    '"{{Shortcut}} "',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/script_context.js'
translation = [
    'throw new Error("{{Could not find module note }}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/sync.js'
translation = [
    '"{{Sync finished successfully.}}"',
    '"{{Sync failed}}: "',
    '"{{Note added to sync queue.}}"',
    'message: "{{No connection to sync server.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/components/tab_manager.js'
translation = [
    """throw new Error(`{{Cannot find noteContext id='${ntxId}'}}`""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/toast.js'
translation = [
    '"{{Info}}"',
    '"{{Error}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/utils.js'
translation = [
    '''throw new Error("{{Can't parse date from}} "''',
    "'{{day}}'",
    "'{{hour}}'",
    "'{{minute}}'",
    "'{{second}}'",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/ws.js'
translation = [
    'showError("{{Sync check failed!}}"',
    'showError("{{Consistency checks failed! See logs for details.}}"',
    '    alert(`{{Encountered error "${e.message}", check out the console.}}`',
    '    logError(`{{Encountered error ${e.message}: ${e.stack}, reloading frontend.}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/setup.js'
translation = [
    '''showAlert("{{Username can't be empty}}"''',
    '''showAlert("{{Password can't be empty}}"''',
    '''showAlert("{{Both password fields need be identical.}}"''',
    '''showAlert("{{Trilium server address can't be empty}}"''',
    "showAlert('{{Sync setup failed}}: '",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/hoisted_note.js'
translation = [
    '.confirm("{{Requested note is outside of hoisted note subtree and you must unhoist to access the note. Do you want to proceed with unhoisting?}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/import.js'
translation = [
    'title: "{{Import status}}"',
    '"{{Import in progress:}} "',
    '"{{Import finished successfully.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/keyboard_actions.js'
translation = [
    """throw new Error(`{{Cannot find keyboard action '${actionName}'}}`""",
    'throw new Error({{`Cannot find action ${actionName}`}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/link.js'
translation = [
    'title: "{{Open note in new tab}}"',
    'title: "{{Open note in new window}}"',
    '    logError("{{Missing note path}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/menus/launcher_context_menu.js'
translation = [
    "title: '{{Add a note launcher}}",
    "title: '{{Add a script launcher}}",
    "title: '{{Add a custom widget}}",
    "title: '{{Add spacer}}",
    "title: '{{Delete }}",
    "title: '{{Reset}}",
    "title: '{{Move to visible launchers}}",
    "title: '{{Move to available launchers}}",
    'title: `{{Duplicate launcher <kbd data-command="duplicateSubtree">}}`',
    '`{{Do you really want to reset "${this.node.title}"? \n                       All data / settings in this note (and its children) will be lost \n                       and the launcher will be returned to its original location.}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/menus/link_context_menu.js'
translation = [
    'title: "{{Open note in a new tab}}"',
    'title: "{{Open note in a new split}}"',
    'title: "{{Open note in a new window}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/glob.js'
translation = [
    '>{{Search tips}}<',
    '> - {{also see}} <',
    '>{{complete help on search}}<',
    '<li>{{Just enter any text for full text search</li>\n        <li><code>#abc</code> - returns notes with label abc</li>\n        <li><code>#year = 2019</code> - matches notes with label <code>year</code> having value <code>2019</code></li>\n        <li><code>#rock #pop</code> - matches notes which have both <code>rock</code> and <code>pop</code> labels</li>\n        <li><code>#rock or #pop</code> - only one of the labels must be present</li>\n        <li><code>#year &lt;= 2000</code> - numerical comparison (also &gt;, &gt;=, &lt;).</li>\n        <li><code>note.dateCreated >= MONTH-1</code> - notes created in the last month</li>\n        <li><code>=handler</code> - will execute script defined in <code>handler</code> relation to get results}}</li>',
    '{{Uncaught error:}}',
    '{{No details available}}',
    '{{Message:}}',
    '{{URL:}}',
    '{{Line:}}',
    '{{Column:}}',
    '{{Error object:}}',
    '{{Stack:}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/mime_types.js'
translation = [
    'title: "{{Plain text}}"',
    'title: "{{GitHub Flavored Markdown}}"',
    'title: "{{Java Server Pages}}"',
    'title: "{{Properties files}}"',
    'title: "{{Vue.js Component}}"',
    "title: '{{JS frontend}}",
    "title: '{{JS backend}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/content_renderer.js'
translation = [
    '>{{Download}}<',
    '>{{Open}}<',
    '>{{The diagram could not displayed.}}<',
    '>{{ Enter protected session}}<',
    '>{{This note is protected and to access it you need to enter password.}}<',
    '>{{Content of this note cannot be displayed in the book format}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/components/note_context.js'
translation = [
    'logError({{`Cannot resolve note path ${inputNotePath}`}})',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_list_renderer.js'
translation = [
    'title="{{Collapse all notes}}"',
    'title="{{Expand all children}}"',
    'title="{{List view}}"',
    'title="{{Grid view}}"',
    'throw new Error(`{{Invalid view type}} ${type}`',
    ' {{notes}})</span>',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_tooltip.js'
translation = [
    '>{{Note has been deleted.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_types.js'
translation = [
    'title: "{{Text}}"',
    'title: "{{Code}}"',
    'title: "{{Saved Search}}"',
    'title: "{{Relation Map}}"',
    'title: "{{Note Map}}"',
    'title: "{{Render Note}}"',
    'title: "{{Book}}"',
    'title: "{{Mermaid Diagram}}"',
    'title: "{{Canvas}}"',
    'title: "{{Web View}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/protected_session.js'
translation = [
    'showMessage("{{Protected session has been started.}}"',
    'showError("{{Wrong password.}}"',
    '" {{in progress:}} "',
    '" {{finished successfully.}}"',
    '+ " {{status}}",',
    '"{{Protecting}}"',
    '"{{Unprotecting}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/tree.js'
translation = [
    '    logError("{{Node is null}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/menus/tree_context_menu.js'
translation = [
    '>{{Ctrl+Click}}<',
    '"{{Info}}"',
    'title: "{{Text}}"',
    'title: "{{Code}}"',
    'title: "{{Saved search}}"',
    'title: "{{Relation Map}}"',
    'title: "{{Note Map}}"',
    'title: "{{Render HTML note}}"',
    'title: "{{Book}}"',
    'title: "{{Mermaid diagram}}"',
    'title: "{{Canvas}}"',
    'title: "{{Advanced}}"',
    'title: "{{Force note sync}}"',
    'title: "{{Protect subtree}}"',
    'title: "{{Unprotect subtree}}"',
    'title: "{{Export}}"',
    'title: "{{Import into note}}"',
    'title: "{{Apply bulk actions}}"',
    # special
    "title: '{{Open in a new tab }}",
    "title: '{{Open in a new split}}",
    "title: '{{Open in a new window}}",
    "title: '{{Insert note after }}",
    "title: '{{Insert child note }}",
    "title: '{{Delete }}",
    "title: '{{Search in subtree }}",
    "title: '{{Hoist note }}",
    "title: '{{Unhoist note }}",
    "title: '{{Edit branch prefix }}",
    "title: '{{Expand subtree }}",
    "title: '{{Collapse subtree }}",
    "title: '{{Sort by ... }}",
    "title: '{{Recent changes in subtree}}",
    "title: '{{Copy / clone }}",
    "title: '{{Clone to ... }}",
    "title: '{{Cut }}",
    "title: '{{Move to ... }}",
    "title: '{{Paste into }}",
    "title: '{{Paste after}}",
    "title: '{{Convert to attachment}}'",
    "title: '{{Copy note path to clipboard}}",
    # special colon
    "title: `{{Duplicate subtree}}",
    '`{{Are you sure you want to convert note selected notes into attachments of their parent notes?}}`',
    '`{{${converted} notes have been converted to attachments.}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/attachment_detail.js'
translation = [
    '{{`This attachment will be automatically deleted in ${utils.formatTimeInterval(willBeDeletedInMs)}`}}',
    '{{This attachment will be automatically deleted soon}}',
    "{{because the attachment is not linked in the note's content. To prevent deletion, add the attachment link back into the content or convert the attachment into note.}}",
    '{{Attachment link copied to clipboard.}}',
    '{{`Role: ${this.attachment.role}, Size: ${utils.formatSize(this.attachment.contentLength)}`}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/attribute_widgets/attribute_detail.js'
translation = [
    '>{{Name:}}<',
    '>{{Value:}}<',
    '>{{Target note:}}<',
    '>{{Promoted:}}<',
    '>{{Multiplicity:}}<',
    '>{{Single value}}<',
    '>{{Multi value}}<',
    '>{{Type:}}<',
    '>{{Text}}<',
    '>{{Number}}<',
    '>{{Boolean}}<',
    '>{{Date}}<',
    '>{{Precision:}}<',
    '>{{digits}}<',
    '>{{Inverse relation:}}<',
    '>{{Inheritable:}}<',
    '>{{Other notes with this label}}<',
    '- {{when Trilium frontend starts up (or is refreshed).}}<',
    '- {{when Trilium backend starts up}}<',
    '- {{run once an hour. You can use additional label <code>runAtHour</code> to specify at which hour.}}<',
    '- {{run once a day}}<',
    '>{{Custom request handler}}<',
    '>{{ will force the Table of Contents to be shown, }}<',
    '{{will force hiding it.}}',
    "{{If the label doesn't exist, the global setting is observed}}",
    'title="{{Cancel changes and close}}"',
    'title="{{Attribute name can be composed of alphanumeric characters, colon and underscore only}}"',
    'title="{{Relation is a named connection between source note and target note.}}"',
    'title="{{Promoted attribute is displayed prominently on the note.}}"',
    'title="{{Multiplicity defines how many attributes of the same name can be created - at max 1 or more than 1.}}"',
    'title="{{Type of the label will help Trilium to choose suitable interface to enter the label value.}}"',
    'title="{{What number of digits after floating point should be available in the value setting interface.}}"',
    'title="{{Optional setting to define to which relation is this one opposite. Example: Father - Son are inverse relations to each other.}}"',
    'title="{{Inheritable attribute will be inherited to all descendants under this tree.}}"',
    '`{{Other notes with ${this.attribute.type} name "${this.attribute.name}"}}`',
    '{{Save & close}} ',
    '{{Ctrl+Enter}}<',
    '{{Delete}}<',
    #
    "{{Label detail}}",
    "{{Label definition detail}}",
    "{{Relation detail}}",
    "{{Relation definition detail}}",
    "{{disables auto-versioning. Useful for e.g. large, but unimportant notes - e.g. large JS libraries used for scripting}}",
    "{{marks note which should be used as root for day notes. Only one should be marked as such.}}",
    "{{notes with this label won't be visible by default in search results (also in Jump To, Add Link dialogs etc).}}",
    "{{notes (with their sub-tree) won't be included in any note export}}",
    "{{defines on which events script should run. Possible values are:}}",
    "{{Define which trilium instance should run this on. Default to all instances.}}",
    "{{On which hour should this run. Should be used together with <code>#run=hourly</code>. Can be defined multiple times for more runs during the day.}}",
    "{{scripts with this label won't be included into parent script execution.}}",
    "{{keeps child notes sorted by title alphabetically}}",
    "{{ASC (the default) or DESC}}",
    "{{Folders (notes with children) should be sorted on top}}",
    "{{keep given note on top in its parent (applies only on sorted parents)}}",
    "{{Hide promoted attributes on this note}}",
    "{{editor is in read only mode. Works only for text and code notes.}}",
    "{{text/code notes can be set automatically into read mode when they are too large. You can disable this behavior on per-note basis by adding this label to the note}}",
    "{{marks CSS notes which are loaded into the Trilium application and can thus be used to modify Trilium's looks.}}",
    "{{marks CSS notes which are full Trilium themes and are thus available in Trilium options.}}",
    "{{value of this label is then added as CSS class to the node representing given note in the tree. This can be useful for advanced theming. Can be used in template notes.}}",
    "{{value of this label is added as a CSS class to the icon on the tree which can help visually distinguish the notes in the tree. Example might be bx bx-home - icons are taken from boxicons. Can be used in template notes.}}",
    "{{number of items per page in note listing}}",
    "{{marks this note as a custom widget which will be added to the Trilium component tree}}",
    "{{marks this note as a workspace which allows easy hoisting}}",
    "{{defines box icon CSS class which will be used in tab when hoisted to this note}}",
    "{{CSS color used in the note tab when hoisted to this note}}",
    "{{Defines per-workspace calendar root}}",
    "{{This note will appear in the selection of available template when creating new note, but only when hoisted into a workspace containing this template}}",
    "{{new search notes will be created as children of this note when hoisted to some ancestor of this workspace note}}",
    "{{new search notes will be created as children of this note}}",
    "{{default inbox location for new notes when hoisted to some ancestor of this workspace note}}",
    "{{default inbox location for new notes}}",
    """{{when you create a note using \\"new note\\" button in the sidebar, notes will be created as child notes in the note marked as with <code>#inbox</code> label.}}""",
    "{{default location of SQL console notes}}",
    "{{note with this label will appear in bookmarks as folder (allowing access to its children)}}",
    "{{note with this label will appear in bookmarks}}",
    "{{this note is hidden from left navigation tree, but still accessible with its URL}}",
    "{{define an alias using which the note will be available under https://your_trilium_host/share/[your_alias]}}",
    "{{default share page CSS will be omitted. Use when you make extensive styling changes.}}",
    "{{marks note which is served on /share root.}}",
    "{{define text to be added to the HTML meta tag for description}}",
    "{{note will be served in its raw format, without HTML wrapper}}",
    "{{will forbid robot indexing of this note via <code>X-Robots-Tag: noindex</code> header}}",
    "{{require credentials to access this shared note. Value is expected to be in format 'username:password'. Don't forget to make this inheritable to apply to child-notes/images.}}",
    "{{note with this this label will list all roots of shared notes}}",
    "{{This note will appear in the selection of available template when creating new note}}",
    "{{comma delimited names of relations which should be displayed. All other ones will be hidden.}}",
    "{{comma delimited names of relations which should be hidden. All other ones will be displayed.}}",
    "{{executes when note is created on backend}}",
    "{{executes when note title is changed (includes note creation as well)}}",
    "{{executes when note is changed (includes note creation as well)}}",
    "{{executes when note is being deleted}}",
    "{{executes when a branch is created. Branch is a link between parent note and child note and is created e.g. when cloning or moving note.}}",
    "{{executes when a branch is deleted. Branch is a link between parent note and child note and is deleted e.g. when moving note (old branch/link is deleted).}}",
    "{{executes when new note is created under this note}}",
    "{{executes when new attribute is created under this note}}",
    "{{executes when attribute is changed under this note}}",
    "{{attached note's attributes will be inherited even without parent-child relationship. See template for details.}}",
    '{{notes of type "render HTML note" will be rendered using a code note (HTML or script) and it is necessary to point using this relation to which note should be rendered}}',
    "{{target of this relation will be executed and rendered as a widget in the sidebar}}",
    "{{CSS note which will be injected into the share page. CSS note must be in the shared sub-tree as well. Consider using 'shareHiddenFromTree' and 'shareOmitDefaultCss' as well.}}",
    "{{JavaScript note which will be injected into the share page. JS note must be in the shared sub-tree as well. Consider using 'shareHiddenFromTree'.}}",
    "{{Favicon note to be set in the shared page. Typically you want to set it to share root and make it inheritable. Favicon note must be in the shared sub-tree as well. Consider using 'shareHiddenFromTree'.}}",
    '{{default title of notes created as children of this note. The value is evaluated as JavaScript string \n                        and thus can be enriched with dynamic content via the injected <code>now</code> and <code>parentNote</code> variables. Examples:}}',
    "{{<code>\\${parentNote.getLabelValue('authorName')}'s literary works</code>}}",
    "{{<code>Log for \\${now.format('YYYY-MM-DD HH:mm:ss')}</code>}}",
    '{{See <a href="https://github.com/zadam/trilium/wiki/Default-note-title">wiki with details</a>, API docs for <a href="https://zadam.github.io/trilium/backend_api/Note.html">parentNote</a> and <a href="https://day.js.org/docs/en/display/format">now</a> for details.}}',
    "'{{see}} <",
    "{{defines color of the note in note tree, links etc. Use any valid CSS color value like 'red' or #a13d5f}}",
    "{{Defines a keyboard shortcut which will immediately jump to this note. Example: 'ctrl+alt+e'. Requires frontend reload for the change to take effect.}}",
    "{{Opening this link won't change hoisting even if the note is not displayable in the current hoisted subtree.}}",
    "{{Title of the button which will execute the current code note}}",
    "{{Longer description of the current code note displayed together with the execute button}}",
    "{{Notes with this label will be hidden from the Note Map}}",
    "{{New notes will be created at the top of the parent note, not on the bottom.}}",
    "{{Use this relation if you want to run the script for all notes created under a specific subtree. In that case, create it on the subtree root note and make it inheritable. A new note created within the subtree (any depth) will trigger the script.}}",
    "{{executes when new note is created under the note where this relation is defined}}",
    "{{executes when note content is changed (includes note creation as well).}}",
    "{{Does not include content changes}}",
    "{{executes when new attribute is created for the note which defines this relation}}",
    "{{executes when the attribute is changed of a note which defines this relation. This is triggered also when the attribute is deleted}}",
    "{{note's attributes will be inherited even without a parent-child relationship, note's content and subtree will be added to instance notes if empty. See documentation for details.}}",
    "{{note's attributes will be inherited even without a parent-child relationship. See template relation for a similar concept. See attribute inheritance in the documentation.}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/abstract_bulk_action.js'
translation = [
    '{{Remove this search action}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/execute_script.js'
translation = [
    '        {{Execute script}}:',
    '"{{Execute script}}"',
    '{{You can execute simple scripts on the matched notes.}}',
    "{{For example to append a string to a note's title, use this small script:}}",
    "{{More complex example would be deleting all matched note's attributes:}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/label/add_label.js'
translation = [
    '"{{Add label}}"',
    '>{{Add label}}<',
    '>{{to value}}<',
    '>{{On all matched notes:}}<',
    ">{{create given label if note doesn't have one yet}}<",
    '>{{or change value of the existing label}}<',
    '>{{You can also call this method without value, in such case label will be assigned to the note without value.}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{label name}}"',
    'placeholder="{{new value}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/label/delete_label.js'
translation = [
    '        {{Delete label}}:',
    '"{{Delete label}}"',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{label name}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/label/rename_label.js'
translation = [
    '"{{Rename label}}"',
    '>{{Rename label from:}}<',
    '>{{To:}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{old name}}"',
    'placeholder="{{new name}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/label/update_label_value.js'
translation = [
    '"{{Update label value}}"',
    '>{{Update label value}}<',
    '>{{to value}}<',
    '>{{On all matched notes, change value of the existing label.}}<',
    '>{{You can also call this method without value, in such case label will be assigned to the note without value.}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{label name}}"',
    'placeholder="{{new value}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/note/delete_note.js'
translation = [
    '"{{Delete note}}"',
    '>{{This will delete matched notes.}}<',
    ">{{After the deletion, it's possible to undelete them from }}<",
    '>{{ Recent Notes dialog.}}<',
    '>{{To erase notes permanently, you can go after the deletion to the Option -> Other and click the "Erase deleted notes now" button.}}<',
    '        {{Delete matched notes}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/note/delete_revisions.js'
translation = [
    '"{{Delete note revisions}}"',
    '        {{Delete note revisions}}',
    "{{All past note revisions of matched notes will be deleted. Note itself will be fully preserved. In other terms, note's history will be removed.}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/note/move_note.js'
translation = [
    '"{{Move note}}"',
    '>{{Move note}}<',
    '>{{to}}<',
    '>{{On all matched notes:}}<',
    '>{{move note to the new parent if note has only one parent (i.e. the old placement is removed and new placement into the new parent is created)}}<',
    ">{{clone note to the new parent if note has multiple clones/placements (it's not clear which placement should be removed)}}<",
    '>{{nothing will happen if note cannot be moved to the target note (i.e. this would create a tree cycle)}}<',
    'placeholder="{{target parent note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/note/rename_note.js'
translation = [
    '"{{Rename note}}"',
    '>{{Rename note title to:}}<',
    '>{{The given value is evaluated as JavaScript string and thus can be enriched with dynamic content via the injected }}<',
    # '>{{note}}<',
    '>{{ variable (note being renamed). Examples:}}<',
    '>{{Note}}<',
    '>{{ - all matched notes are renamed to "Note"}}<',
    '>{{ - matched notes titles are prefixed with "NEW: "}}<',
    ">{{ - matched notes are prefixed with note's creation month-date}}<",
    '{{See API docs for <a href="https://zadam.github.io/trilium/backend_api/Note.html">note</a> and its <a href="https://day.js.org/docs/en/display/format">dateCreatedObj / utcDateCreatedObj properties</a> for details.}}',
    'title="{{Click help icon on the right to see all the options}}"',
    'placeholder="{{new note title}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/relation/add_relation.js'
translation = [
    '"{{Add relation}}"',
    '>{{Add relation}}<',
    '>{{to}}<',
    '>{{On all matched notes create given relation.}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{relation name}}"',
    'placeholder="{{target note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/relation/delete_relation.js'
translation = [
    '        {{Delete relation}}:',
    '"{{Delete relation}}"',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{relation name}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/relation/rename_relation.js'
translation = [
    '"{{Rename relation}}"',
    '>{{Rename relation from:}}<',
    '>{{To:}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{old name}}"',
    'placeholder="{{new name}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bulk_actions/relation/update_relation_target.js'
translation = [
    '"{{Update relation target}}"',
    '>{{Update relation}}<',
    '>{{to}}<',
    '>{{On all matched notes:}}<',
    ">{{create given relation if note doesn't have one yet}}<",
    '>{{or change target note of the existing relation}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    'placeholder="{{relation name}}"',
    'placeholder="{{target note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/attachments_actions.js'
translation = [
    "{{File will be open in an external application and watched for changes. You'll then be able to upload the modified version back to Trilium.}}",
    '>{{Open externally}}<',
    '>{{Open custom}}<',
    '>{{Download}}<',
    '>{{Rename attachment}}<',
    '>{{Upload new revision}}<',
    '>{{Copy link to clipboard}}<',
    '>{{Convert attachment into note}}<',
    '>{{Delete attachment}}<',
    '"{{New attachment revision has been uploaded.}}"',
    '"{{Upload of a new attachment revision failed.}}"',
    '"{{Opening attachment externally is available only from the detail page, please first click on the attachment detail first and repeat the action.}}"',
    '{{Are you sure you want to delete attachment}}',
    "{{Attachment '${this.attachment.title}' has been deleted.}}",
    "{{Are you sure you want to convert attachment '${this.attachment.title}' into a separate note?}}",
    "{{Attachment '${this.attachment.title}' has been converted to note.}}",
    'title: "{{Rename attachment}}",',
    "{{Please enter new attachment's name}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/close_pane_button.js'
translation = [
    '"{{Close this pane}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/create_pane_button.js'
translation = [
    '"{{Create new split}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/left_pane_toggle.js'
translation = [
    '"{{Hide panel}}"',
    '"{{Open panel}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/move_pane_button.js'
translation = [
    '"{{Move left}}"',
    '"{{Move right}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/revisions_button.js'
translation = [
    '.title("{{Note Revisions}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/attribute_widgets/attribute_editor.js'
translation = [
    'title: "{{Add new label definition}}"',
    'title: "{{Add new relation definition}}"',
    '"{{Type the labels and relations here}}"',
    '`{{Add new label}} <',
    '`{{Add new relation}} <',
    '"{{Add new label definition}}"',
    '"{{Add new relation definition}}"',
    'title="{{Save attributes <enter>}}"',
    'title="{{Add a new attribute}}"',
    """`\n{{<p>To add label, just type e.g. <code>#rock</code> or if you want to add also value then e.g. <code>#year = 2020</code></p> \n\n<p>For relation, type <code>~author = @</code> which should bring up an autocomplete where you can look up the desired note.</p>\n\n<p>Alternatively you can add label and relation using the <code>+</code> button on the right side.</p>}}`""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/zpetne_odkazy.js'
translation = [
    "{{`${resp.count} backlink`\n            + (resp.count === 1 ? '' : 's')}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bookmark_switch.js'
translation = [
    'title="{{Bookmark this note to the left side panel}}"',
    'title="{{Remove bookmark}}"',
    # 0.49
    '.text("{{Bookmark}}")',
    '.attr("title", "{{Bookmark this note to the left side panel}}")',
    '.attr("title", "{{Remove bookmark}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/calendar.js'
translation = [
    'super("bx-calendar", "{{Calendar}}"',
    '>{{Mon}}<',
    '>{{Tue}}<',
    '>{{Wed}}<',
    '>{{Thu}}<',
    '>{{Fri}}<',
    '>{{Sat}}<',
    '>{{Sun}}<',
    '    alert("{{Cannot find day note}}"',
    "'{{January}}',",
    "'{{Febuary}}',",
    "'{{March}}',",
    "'{{April}}',",
    "'{{May}}',",
    "'{{June}}',",
    "'{{July}}',",
    "'{{August}}',",
    "'{{September}}',",
    "'{{October}}',",
    "'{{November}}',",
    "'{{December}}'",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/edit_button.js'
translation = [
    '{{Edit this note}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/global_menu.js'
translation = [
    'title="{{Menu}}"',
    '            {{Options}}',
    '            {{Open New Window}}',
    '            {{Open Dev Tools}}',
    '            {{Open SQL Console History}}',
    '            {{Open SQL Console}}',
    '            {{Show Backend Log}}',
    '            {{Open Search History}}',
    '            {{Switch to Mobile Version}}',
    '            {{Switch to Desktop Version}}',
    '            {{Configure Launchbar}}',
    '            {{Show Shared Notes Subtree}}',
    '            {{Advanced}}',
    '            {{Reload Frontend}}',
    '            {{Show Hidden Subtree}}',
    'title="{{Reload can help with some visual glitches without restarting the whole app.}}"',
    '    {{Zoom}}',
    'title="{{Zoom Out}}"',
    'title="{{Reset Zoom Level}}"',
    'title="{{Zoom In}}"',
    'title="{{Toggle Fullscreen}}"',
    '            {{Show Help}}',
    '            {{About Trilium Notes}}',
    '            {{Logout}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/note_actions.js'
translation = [
    '>{{Convert into attachment}}<',
    '>{{ Re-render note}}<',
    '>{{Search in note }}<',
    '>{{ Note source}}<',
    '>{{ Note attachments}}<',
    '{{Open note externally}}',
    "{{File will be open in an external application and watched for changes. You'll then be able to upload the modified version back to Trilium.}}",
    '> {{Open note custom}}<',
    '>{{Import files}}<',
    '>{{Export note}}<',
    '>{{Delete note}}<',
    '>{{ Print note}}<',
    '>{{ Save revision}}<',
    "showMessage(`{{Converting note '${this.note.title}' failed.}}`",
    "showMessage(`{{Note '${newAttachment.title}' has been converted to attachment.}}`",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/protected_session_status.js'
translation = [
    '{{Protected session is active. Click to leave protected session.}}',
    '{{Click to enter protected session}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/left_pane_toggle.js'
translation = [
    '"{{Hide sidebar.}}"',
    '"{{Open sidebar.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/update_available.js'
translation = [
    'title="{{Update available}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/relation_map_buttons.js'
translation = [
    'title="{{Create new child note and add it into this relation map}}"',
    'title="{{Reset pan & zoom to initial coordinates and magnification}}"',
    'title="{{Zoom In}}"',
    'title="{{Zoom Out}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/mermaid_export_button.js'
translation = [
    'title="{{Export Mermaid diagram as SVG}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/mobile_widgets/mobile_detail_menu.js'
translation = [
    'title: "{{Insert child note}}"',
    'title: "{{Delete this note}}"',
    'throw new Error({{`Cannot get branchId for notePath ${notePath}`}}',
    'throw new Error("{{Unrecognized command}} "',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/ancestor.js'
translation = [
    '>{{Ancestor:}}<',
    '{{search for note by its name}}',
    '>{{depth:}}<',
    ">{{doesn't matter}}<",
    '>{{is exactly 1 (direct children)}}<',
    '>{{is exactly 2}}<',
    '>{{is exactly 3}}<',
    '>{{is exactly 4}}<',
    '>{{is exactly 5}}<',
    '>{{is exactly 6}}<',
    '>{{is exactly 7}}<',
    '>{{is exactly 8}}<',
    '>{{is exactly 9}}<',
    '>{{is greater than 0}}<',
    '>{{is greater than 1}}<',
    '>{{is greater than 2}}<',
    '>{{is greater than 3}}<',
    '>{{is greater than 4}}<',
    '>{{is greater than 5}}<',
    '>{{is greater than 6}}<',
    '>{{is greater than 7}}<',
    '>{{is greater than 8}}<',
    '>{{is greater than 9}}<',
    '>{{is less than 2}}<',
    '>{{is less than 3}}<',
    '>{{is less than 4}}<',
    '>{{is less than 5}}<',
    '>{{is less than 6}}<',
    '>{{is less than 7}}<',
    '>{{is less than 8}}<',
    '>{{is less than 9}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/debug.js'
translation = [
    '    {{Debug}}',
    '>{{Debug will print extra debugging information into the console to aid in debugging complex queries.}}<',
    '>{{To access the debug information, execute query and click on "Show backend log" in top left corner.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/fast_search.js'
translation = [
    # DO NOT CHANGE THIS ORDER!
    # order matters!
    '{{Fast search option disables full text search of note contents which might speed up searching in large databases.}}',
    '    {{Fast search}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/include_archived_notes.js'
translation = [
    '    {{Include archived notes}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/limit.js'
translation = [
    '    {{Limit}}',
    '{{Take only first X specified results.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/order_by.js'
translation = [
    '    {{Order by}}',
    '>{{Relevancy (default)}}<',
    '>{{Title}}<',
    '>{{Date created}}<',
    '>{{Date of last modification}}<',
    '>{{Note content size}}<',
    '>{{Note content size including revisions}}<',
    '>{{Note content size including attachments}}<',
    '>{{Note content size including attachments and revisions}}<',
    '>{{Number of revisions}}<',
    '>{{Number of children notes}}<',
    '>{{Number of clones}}<',
    '>{{Number of labels}}<',
    '>{{Number of relations}}<',
    '>{{Number of relations targeting the note}}<',
    '>{{Random order}}<',
    '>{{Ascending (default)}}<',
    '>{{Descending}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/search_script.js'
translation = [
    ">{{Search script allows to define search results by running a script. This provides maximal flexibility when standard search doesn't suffice.}}<",
    '>{{Search script must be of type "code" and subtype "JavaScript backend". The script receives  needs to return an array of noteIds or notes.}}<',
    '>{{See this example:}}<',
    ">{{Note that search script and search string can't be combined with each other.}}<",
    '    {{Search script:}}',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/containers/flex_container.js'
translation = [
    """throw new Error(`{{Direction argument given as "${direction}", use either 'row' or 'column'}}`""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/bookmark_switch.js'
translation = [
    '        {{Bookmark}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/editability_select.js'
translation = [
    '>{{auto}}<',
    """>{{Note is editable if it's not too long.}}<""",
    '>{{Note is read-only, but can be edited with a button click.}}<',
    '>{{Note is always editable, regardless of its length.}}<',
    '            {{Auto}}',
    '            {{Read-only}}',
    '            {{Always editable}}',
    '"auto": "{{Auto}}",',
    '"readOnly": "{{Read-only}}",',
    '"autoReadOnlyDisabled": "{{Always Editable}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/code_buttons.js'
translation = [
    'title="{{Execute script}}"',
    'title="{{Open Trilium API docs}}"',
    'showMessage(`{{SQL Console note has been saved into}}',
    'showMessage("{{Opening API docs...}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/copy_image_reference_button.js'
translation = [
    '{{Copy image reference to the clipboard, can be pasted into a text note.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/floating_buttons/hide_floating_buttons_button.js'
translation = [
    'title="{{Hide buttons}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/find.js'
translation = [
    '                {{case sensitive}}',
    '                {{match words}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/highlights_list.js'
translation = [
    '"{{Highlights List}}"',
    '"{{Close Highlights List}}"',
    '"{{Options}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/mermaid.js'
translation = [
    '>{{The diagram could not be displayed. See }}<',
    '>{{help and examples}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_detail.js'
translation = [
    'throw new Error("{{Could not find typeWidget for type: }}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_icon.js'
translation = [
    '>{{Category:}}<',
    '>{{Search:}}<',
    '>{{Reset to default icon}}<',
    'title="{{Change note icon}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_map.js'
translation = [
    'title="{{Link Map}}"',
    'title="{{Tree map}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_title.js'
translation = [
    "{{type note's title here...}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_tree.js'
translation = [
    '>{{Save & apply changes}}<',
    'title="{{Collapse note tree}}"',
    'title="{{Scroll to active note}}"',
    'title="{{Tree settings}}"',
    'title="{{Images which are shown in the parent text note will not be displayed in the tree}}"',
    'title="{{Notes will be collapsed after period of inactivity to declutter the tree.}}"',
    'title="{{Unhoist}}"',
    'title="{{Hoist this note (workspace)}}"',
    'title="{{Refresh saved search results}}"',
    'title="{{Create child note}}"',
    '"{{Saved search note refreshed.}}"',
    '    {{Hide archived notes}}',
    '    {{Hide images included in a note}}',
    '    {{Automatically collapse notes}}',
    'showMessage("{{Auto collapsing notes after inactivity...}}"',
    'infoDialog.info("{{Dropping notes into this location is not allowed.}}")',
    "{{Dropping notes into this location is not allowed.}}",
    'throw new Error(`{{Branch "${branch.branchId}" has no note "${branch.noteId}"}}`',
    'throw new Error("{{Unknown hitMode=}}"',
    '    logError(`{{Cannot parse ${jsonStr} into notes for drop}}`',
    '    logError({{`Cannot find branch=${branchId}`}}',
    '    logError("{{Could not find run path for notePath:}}"',
    '"{{Apply bulk actions on selected notes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_type.js'
translation = [
    'title: "{{File}}"',
    'title: "{{Image}}"',
    # capital letter!
    'title: "{{Saved Search}}"',
    'title: "{{Note Map}}"',
    'title: "{{Launcher}}"',
    'title: "{{Doc}}"',
    'title: "{{Widget}}"',
    'title: "{{Text}}"',
    'title: "{{Relation Map}}"',
    'title: "{{Render Note}}"',
    'title: "{{Canvas}}"',
    'title: "{{Book}}"',
    'title: "{{Web View}}"',
    'title: "{{Mermaid Diagram}}"',
    'title: "{{Code}}"',
    '    {{Type:}} <span',
    '.confirm("{{It is not recommended to change note type when note content is not empty. Do you want to continue anyway?}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/protected_note_switch.js'
translation = [
    '"{{Protect the note}}"',
    '"{{Note is not protected, click to make it protected}}"',
    '"{{Unprotect the note}}"',
    '"{{Note is protected, click to make it unprotected}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/quick_search.js'
translation = [
    # 0.47
    '>{{Searching ...}}<',
    # 0.48
    '>{{ Searching ...}}<',
    '>{{No results found}}<',
    '>{{... and ${searchResultNoteIds.length - MAX_DISPLAYED_NOTES} more results.}}<',
    '>{{Show in full search}}<',
    '"{{Quick search}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/basic_properties.js'
translation = [
    '>{{Note type:}}<',
    '>{{Editable:}}<',
    "title: '{{Basic Properties}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/book_properties.js'
translation = [
    '>{{View type:&nbsp; &nbsp;}}<',
    '>{{Grid}}<',
    '>{{List}}<',
    'title="{{Collapse all notes}}"',
    'title="{{Expand all children}}"',
    "title: '{{Book Properties}}",
    "throw new Error(`{{Invalid view type}} '${type}'`)",
    '    {{Collapse}}',
    '    {{Expand}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/edited_notes.js'
translation = [
    '>{{No edited notes on this day yet ...}}<',
    "title: '{{Edited Notes}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/file_properties.js'
translation = [
    '>{{Note ID:}}<',
    '>{{Original file name:}}<',
    '>{{File type:}}<',
    '>{{File size:}}<',
    '>{{Download}}<',
    '>{{Open}}<',
    '>{{Upload new revision}}<',
    "title: '{{File}}",
    'showMessage("{{New file revision has been uploaded.}}"',
    'showError("{{Upload of a new file revision failed.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/image_properties.js'
translation = [
    '>{{Original file name:}}<',
    '>{{File type:}}<',
    '>{{File size:}}<',
    '>{{Download}}<',
    '>{{Open}}<',
    '>{{Copy to clipboard}}<',
    '>{{Copy reference to clipboard}}<',
    '>{{Upload new revision}}<',
    "title: '{{Image}}",
    'showMessage("{{New image revision has been uploaded.}}"',
    'showError("{{Upload of a new image revision failed: }}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/inherited_attribute_list.js'
translation = [
    'title: "{{Inherited Attributes}}"',
    '"{{No inherited attributes.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/note_info_widget.js'
translation = [
    '>{{Note ID:}}<',
    '>{{Created}}:<',
    '>{{Modified}}:<',
    '>{{Type:}}<',
    '>{{Note size}}:<',
    '</span> {{calculate}}',
    '''title="{{Note size provides rough estimate of storage requirements for this note. It takes into account note's content and content of its note revisions.}}"''',
    "title: '{{Note Info}}",
    '({{subtree size}}: ',
    '{{in ${subTreeResp.subTreeNoteCount} notes}})',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/note_map.js'
translation = [
    'title="{{Open full}}"',
    'title="{{Collapse to normal size}}"',
    "title: '{{Note Map}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/note_paths.js'
translation = [
    '>{{Clone note to new location...}}<',
    'title="{{This path is outside of hoisted note and you would have to unhoist.}}"',
    'title="{{Archived}}"',
    'title="{{Search}}"',
    "title: '{{Note Paths}}",
    '{{This note is placed into the following paths:}}',
    '{{This note is not yet placed into the note tree.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/note_properties.js'
translation = [
    "title: '{{Info}}",
    "{{This note was originally taken from:}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/owned_attribute_list.js'
translation = [
    'title: "{{Owned Attributes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/promoted_attributes.js'
translation = [
    'title: "{{Promoted Attributes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/search_definition.js'
translation = [
    '>{{Add search option:}}<',
    '>{{enter}}<',
    'title="{{Fast search option disables full text search of note contents which might speed up searching in large databases.}}"',
    'title="{{Archived notes are by default excluded from search results, with this option they will be included.}}"',
    'title="{{Limit number of results}}"',
    'title="{{Debug will print extra debugging information into the console to aid in debugging complex queries}}"',
    "title: '{{Search Parameters}}",
    'showMessage(`{{Search note has been saved into }}',
    "showMessage('{{Actions have been executed.}}'",
    'logError(`{{Unknown search option}}`)',
    """logError({{`Parsing of attribute: '${actionAttr.value}' failed with error: ${e.message}`}})""",
    """    logError(`{{No action class for '${actionDef.name}' found.}}`""",
    '    {{Search & Execute actions}}',
    '    {{Save to note}}',
    '    {{search string}}',
    '    {{search script}}',
    '    {{ancestor}}',
    '    {{fast search}}',
    '    {{include archived}}',
    '    {{order by}}',
    '    {{limit}}',
    '    {{debug}}',
    '    {{action}}',
    '    {{Delete note}}<',
    '    {{Delete note revisions}}<',
    '    {{Delete label}}<',
    '    {{Delete relation}}<',
    '    {{Rename label}}<',
    '    {{Rename relation}}<',
    '    {{Set label value}}<',
    '    {{Set relation target}}<',
    '    {{Execute script}}<',
    '        {{Search}}\n',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/similar_notes.js'
translation = [
    "title: '{{Similar Notes}}",
    '"{{No similar notes found.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/abstract_search_option.js'
translation = [
    '{{Remove this search option}}',
    '    logError({{`Failed rendering search option: ${JSON.stringify(this.attribute.dto)} with error: ${e.message} ${e.stack}`}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/search_string.js'
translation = [
    '>{{Search string:}}<',
    '>{{Search syntax}}<',
    '> - {{also see}} <',
    '>{{complete help on search syntax}}<',
    "title: '{{Search: }}",
    """<li>{{Just enter any text for full text search</li>\n                <li><code>#abc</code> - returns notes with label abc</li>\n                <li><code>#year = 2019</code> - matches notes with label <code>year</code> having value <code>2019</code></li>\n                <li><code>#rock #pop</code> - matches notes which have both <code>rock</code> and <code>pop</code> labels</li>\n                <li><code>#rock or #pop</code> - only one of the labels must be present</li>\n                <li><code>#year &lt;= 2000</code> - numerical comparison (also &gt;, &gt;=, &lt;).</li>\n                <li><code>note.dateCreated >= MONTH-1</code> - notes created in the last month}}</li>""",
    """{{this.note.title.startsWith('Search: ')}}""",
    '{{fulltext keywords, #tag = value ...}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/shared_info.js'
translation = [
    '>. {{For help visit}} <',
    '"{{This note is shared publicly on}}"',
    '"{{This note is shared locally on}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/shared_switch.js'
translation = [
    '.text("{{Shared}}")',
    '.attr("title", "{{Share the note}}")',
    '.attr("title", "{{Unshare the note}}")',
    '.attr("title", "{{Note cannot be unshared here because it is shared through inheritance from an ancestor.}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/switch.js'
translation = [
    'title="{{Open help page}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/spacer.js'
translation = [
    'title: "{{Configure Launchbar}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/sync_status.js'
translation = [
    '>{{Sync status will be known once the next sync attempt starts.}}<',
    '>{{Click to trigger sync now.}}<',
    '>{{Connected to the sync server.}} <',
    '>{{There are some outstanding changes yet to be synced.}}<',
    '>{{Click to trigger sync.}}<',
    '>{{Connected to the sync server.}}<',
    '>{{All changes have been already synced.}}<',
    '>{{Click to trigger sync.}}<',
    '>{{Establishing the connection to the sync server was unsuccessful.}}<',
    '>{{All known changes have been synced.}}<',
    '"{{Sync with the server is in progress.}}"',
    'title: "{{Sync status}}"',
    'message: "{{Sync update in progress}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/title_bar_buttons.js'
translation = [
    '{{Keep this window on top.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/toc.js'
translation = [
    '"{{Table of Contents}}"',
    '.title("{{Close TOC}}")',
    '.title("{{Options}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_result.js'
translation = [
    '{{No notes have been found for given search parameters.}}',
    '{{Search has not been executed yet. Click on "Search" button above to see the results.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/tab_row.js'
translation = [
    'title: "{{Move this tab to a new window}}"',
    'title: "{{Close all tabs}}"',
    'title: "{{Close all tabs except for this}}"',
    'title="{{Close tab}}"',
    'title="{{Add new tab}}"',
    'title: "{{Close}}"',
    'title: "{{Close other tabs}}"',
    ", '{{New tab}}')",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/content/backend_log.js'
translation = [
    '>{{Refresh}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/attachment_detail.js'
translation = [
    '"{{Owning note}}: "',
    '", {{you can also open the}} "',
    "title: '{{List of all attachments}}',",
    '>{{This attachment has been deleted.}}<',
    'title="{{Open help page on attachments}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/attachment_list.js'
translation = [
    '"{{Owning note}}: "',
    '"{{Upload attachments}}"',
    '{{This note has no attachments.}}',
    'title="{{Open help page on attachments}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/book.js'
translation = [
    """{{This note of type Book doesn't have any child notes so there's nothing to display. See <a href="https://github.com/zadam/trilium/wiki/Book-note">wiki</a> for details.}}""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/editable_code.js'
translation = [
    'placeholder: "{{Type the content of your code note here...}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/editable_text.js'
translation = [
    'placeholder: "{{Type the content of your note here ...}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/empty.js'
translation = [
    ">{{Open a note by typing the note's title into the input below or choose a note in the tree.}}<",
    '"{{search for a note by its name}}"',
    '{{Enter workspace}} ',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/image.js'
translation = [
    'title: "{{Copy reference to clipboard}}"',
    'title: "{{Copy image to clipboard}}"',
    'showMessage("{{Image copied to the clipboard}}"',
    'throw new Error(`{{Unrecognized command}}',
    '    toastService.showAndLogError("{{Could not copy the image to clipboard.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/file.js'
translation = [
    '{{File preview is not available for this file format.}}',
]

replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/protected_session.js'
translation = [
    '>{{Showing protected note requires entering your password:}}<',
    '>{{Start protected session }}<',
    '>{{enter}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/read_only_code.js'
translation = [
    'title="{{Edit this note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/read_only_text.js'
translation = [
    'title="{{Edit this note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/relation_map.js'
translation = [
    'title: "{{Open in new tab}}"',
    'title: "{{Remove note}}"',
    'title: "{{Edit title}}"',
    'title: "{{Rename note}}"',
    'title: "{{Remove relation}}"',
    'title="{{Create new child note and add it into this relation map}}"',
    'title="{{Reset pan & zoom to initial coordinates and magnification}}"',
    'title="{{Zoom In}}"',
    'title="{{Zoom Out}}"',
    'message: "{{Enter title of new note}}"',
    'message: "{{Enter new note title:}}"',
    'message: "{{Specify new relation name (allowed characters: alphanumeric, colon and underscore):}}"',
    'defaultValue: "{{new note}}"',
    'showMessage("{{Click on canvas to place new note}}"',
    '    {{Create child note}}',
    '''{{"Connection '" + name + "' between these notes already exists."}}''',
    '"{{Start dragging relations from here and drop them on another note.}}"',
    'showError(`{{Note "${note.title}" is already in the diagram.}}`',
    'throw new Error("{{Cannot match transform: }}"',
    '.confirm("{{Are you sure you want to remove the relation?}}"',
    '    logError(`{{Note ${noteId} not found!}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/render.js'
translation = [
    ">{{This help note is shown because this note of type Render HTML doesn't have required relation to function properly.}}<",
    """>{{Render HTML note type is used for <a class="external" href="https://github.com/zadam/trilium/wiki/Scripts">scripting</a>. In short, you have a HTML code note (optionally with some JavaScript) and this note will render it. To make it work, you need to define a <a class="external" href="https://github.com/zadam/trilium/wiki/Attributes">relation</a> called "renderNote" pointing to the HTML note to render.}}<""",
]
replace_in_file(file_path, translation)

#  ckeditor
file_path = 'libraries/ckeditor/ckeditor.js'
translation = [
    'label:"{{Black}}"',
    'label:"{{Dim grey}}"',
    'label:"{{Grey}}"',
    'label:"{{Light grey}}"',
    'label:"{{White}}"',
    'label:"{{Red}}"',
    'label:"{{Orange}}"',
    'label:"{{Yellow}}"',
    'label:"{{Light green}}"',
    'label:"{{Green}}"',
    'label:"{{Aquamarine}}"',
    'label:"{{Turquoise}}"',
    'label:"{{Light blue}}"',
    'label:"{{Blue}}"',
    'label:"{{Purple}}"',
    'label:"{{Plain text}}"',
    'label:"{{Diff}}"',
    'label:"{{include note widget}}"',
    'label:"{{Internal Trilium link}} (CTRL-L)"',
    'label:"{{Markdown import from clipboard}}"',
    'label:"{{Cut & paste selection to sub-note}}"',
    '''"%0 of %1":"{{%0 of %1}}"''',
    '''"Align cell text to the bottom":"{{Align cell text to the bottom}}"''',
    '''"Align cell text to the center":"{{Align cell text to the center}}"''',
    '''"Align cell text to the left":"{{Align cell text to the left}}"''',
    '''"Align cell text to the middle":"{{Align cell text to the middle}}"''',
    '''"Align cell text to the right":"{{Align cell text to the right}}"''',
    '''"Align cell text to the top":"{{Align cell text to the top}}"''',
    '''"Align table to the left":"{{Align table to the left}}"''',
    '''"Align table to the right":"{{Align table to the right}}"''',
    '''Alignment:"{{Alignment}}"''',
    '''Aquamarine:"{{Aquamarine}}"''',
    '''Background:"{{Background}}"''',
    '''Big:"{{Big}}"''',
    '''Black:"{{Black}}"''',
    '''"Block quote":"{{Block quote}}"''',
    '''Blue:"{{Blue}}"''',
    '''Bold:"{{Bold}}"''',
    '''Border:"{{Border}}"''',
    '''"Bulleted List":"{{Bulleted List}}"''',
    '''"Bulleted list styles toolbar":"{{Bulleted list styles toolbar}}"''',
    '''Cancel:"{{Cancel}}"''',
    '''"Cannot upload file:":"{{Cannot upload file:}}"''',
    '''"Cell properties":"{{Cell properties}}"''',
    '''"Center table":"{{Center table}}"''',
    '''"Centered image":"{{Centered image}}"''',
    '''"Change image text alternative":"{{Change image text alternative}}"''',
    '''"Choose heading":"{{Choose heading}}"''',
    '''Circle:"{{Circle}}"''',
    '''"Click to edit block":"{{Click to edit block}}"''',
    '''Code:"{{Code}}"''',
    '''Color:"{{Color}}"''',
    '''"Color picker":"{{Color picker}}"''',
    '''Column:"{{Column}}"''',
    '''Dashed:"{{Dashed}}"''',
    '''Decimal:"{{Decimal}}"''',
    '''"Decimal with leading zero":"{{Decimal with leading zero}}"''',
    '''"Decrease indent":"{{Decrease indent}}"''',
    '''Default:"{{Default}}"''',
    '''"Delete column":"{{Delete column}}"''',
    '''"Delete row":"{{Delete row}}"''',
    '''"Dim grey":"{{Dim grey}}"''',
    '''Dimensions:"{{Dimensions}}"''',
    '''Disc:"{{Disc}}"''',
    '''"Document colors":"{{Document colors}}"''',
    '''Dotted:"{{Dotted}}"''',
    '''Double:"{{Double}}"''',
    '''Downloadable:"{{Downloadable}}"''',
    '''"Drag to move":"{{Drag to move}}"''',
    '''"Dropdown toolbar":"{{Dropdown toolbar}}"''',
    '''"Edit block":"{{Edit block}}"''',
    '''"Edit link":"{{Edit link}}"''',
    '''"Editor toolbar":"{{Editor toolbar}}"''',
    '''"Enter image caption":"{{Enter image caption}}"''',
    '''"Font Background Color":"{{Font Background Color}}"''',
    '''"Font Color":"{{Font Color}}"''',
    '''"Font Family":"{{Font Family}}"''',
    '''"Font Size":"{{Font Size}}"''',
    '''"Full size image":"{{Full size image}}"''',
    '''Green:"{{Green}}"''',
    '''Grey:"{{Grey}}"''',
    '''Groove:"{{Groove}}"''',
    '''"Header column":"{{Header column}}"''',
    '''"Header row":"{{Header row}}"''',
    '''Heading:"{{Heading}}"''',
    '''"Heading 1":"{{Heading 1}}"''',
    '''"Heading 2":"{{Heading 2}}"''',
    '''"Heading 3":"{{Heading 3}}"''',
    '''"Heading 4":"{{Heading 4}}"''',
    '''"Heading 5":"{{Heading 5}}"''',
    '''"Heading 6":"{{Heading 6}}"''',
    '''Height:"{{Height}}"''',
    '''"Horizontal line":"{{Horizontal line}}"''',
    '''"Horizontal text alignment toolbar":"{{Horizontal text alignment toolbar}}"''',
    '''Huge:"{{Huge}}"''',
    '''"Image resize list":"{{Image resize list}}"''',
    '''"Image toolbar":"{{Image toolbar}}"''',
    '''"image widget":"{{image widget}}"''',
    '''"Increase indent":"{{Increase indent}}"''',
    '''"Insert code block":"{{Insert code block}}"''',
    '''"Insert column left":"{{Insert column left}}"''',
    '''"Insert column right":"{{Insert column right}}"''',
    '''"Insert image":"{{Insert image}}"''',
    '''"Insert paragraph after block":"{{Insert paragraph after block}}"''',
    '''"Insert paragraph before block":"{{Insert paragraph before block}}"''',
    '''"Insert row above":"{{Insert row above}}"''',
    '''"Insert row below":"{{Insert row below}}"''',
    '''"Insert table":"{{Insert table}}"''',
    '''Inset:"{{Inset}}"''',
    '''Italic:"{{Italic}}"''',
    '''"Justify cell text":"{{Justify cell text}}"''',
    '''"Left aligned image":"{{Left aligned image}}"''',
    '''"Light blue":"{{Light blue}}"''',
    '''"Light green":"{{Light green}}"''',
    '''"Light grey":"{{Light grey}}"''',
    '''Link:"{{Link}}"''',
    '''"Link URL":"{{Link URL}}"''',
    '''"List properties":"{{List properties}}"''',
    '''"Lower-latin":"{{Lower-latin}}"''',
    '''"Lower–roman":"{{Lower–roman}}"''',
    '''"Merge cell down":"{{Merge cell down}}"''',
    '''"Merge cell left":"{{Merge cell left}}"''',
    '''"Merge cell right":"{{Merge cell right}}"''',
    '''"Merge cell up":"{{Merge cell up}}"''',
    '''"Merge cells":"{{Merge cells}}"''',
    '''Next:"{{Next}}"''',
    '''None:"{{None}}"''',
    '''"Numbered List":"{{Numbered List}}"''',
    '''"Numbered list styles toolbar":"{{Numbered list styles toolbar}}"''',
    '''"Open in a new tab":"{{Open in a new tab}}"''',
    '''"Open link in new tab":"{{Open link in new tab}}"''',
    '''Orange:"{{Orange}}"''',
    '''Original:"{{Original}}"''',
    '''Outset:"{{Outset}}"''',
    '''Padding:"{{Padding}}"''',
    '''Paragraph:"{{Paragraph}}"''',
    '''"Plain text":"{{Plain text}}"''',
    '''Previous:"{{Previous}}"''',
    '''Purple:"{{Purple}}"''',
    '''Red:"{{Red}}"''',
    '''Redo:"{{Redo}}"''',
    '''"Remove color":"{{Remove color}}"''',
    '''"Remove Format":"{{Remove Format}}"''',
    '''"Resize image":"{{Resize image}}"''',
    '''"Resize image to %0":"{{Resize image to %0}}"''',
    '''"Resize image to the original size":"{{Resize image to the original size}}"''',
    '''"Restore default":"{{Restore default}}"''',
    '''"Reversed order":"{{Reversed order}}"''',
    '''"Rich Text Editor":"{{Rich Text Editor}}"''',
    '''"Rich Text Editor %0":"{{Rich Text Editor %0}}"''',
    '''Ridge:"{{Ridge}}"''',
    '''"Right aligned image":"{{Right aligned image}}"''',
    '''Row:"{{Row}}"''',
    '''Save:"{{Save}}"''',
    '''"Select all":"{{Select all}}"''',
    '''"Select column":"{{Select column}}"''',
    '''"Select row":"{{Select row}}"''',
    '''"Show more items":"{{Show more items}}"''',
    '''"Side image":"{{Side image}}"''',
    '''Small:"{{Small}}"''',
    '''Solid:"{{Solid}}"''',
    '''"Split cell horizontally":"{{Split cell horizontally}}"''',
    '''"Split cell vertically":"{{Split cell vertically}}"''',
    '''Square:"{{Square}}"''',
    '''"Start at":"{{Start at}}"''',
    '''Strikethrough:"{{Strikethrough}}"''',
    '''Style:"{{Style}}"''',
    '''Subscript:"{{Subscript}}"''',
    '''Superscript:"{{Superscript}}"''',
    '''"Table alignment toolbar":"{{Table alignment toolbar}}"''',
    '''"Table cell text alignment":"{{Table cell text alignment}}"''',
    '''"Table properties":"{{Table properties}}"''',
    '''"Table toolbar":"{{Table toolbar}}"''',
    '''"Text alternative":"{{Text alternative}}"''',
    '''"This link has no URL":"{{This link has no URL}}"''',
    '''Tiny:"{{Tiny}}"''',
    '''"To-do List":"{{To-do List}}"''',
    '''"Toggle the circle list style":"{{Toggle the circle list style}}"''',
    '''"Toggle the decimal list style":"{{Toggle the decimal list style}}"''',
    '''"Toggle the decimal with leading zero list style":"{{Toggle the decimal with leading zero list style}}"''',
    '''"Toggle the disc list style":"{{Toggle the disc list style}}"''',
    '''"Toggle the lower–latin list style":"{{Toggle the lower–latin list style}}"''',
    '''"Toggle the lower–roman list style":"{{Toggle the lower–roman list style}}"''',
    '''"Toggle the square list style":"{{Toggle the square list style}}"''',
    '''"Toggle the upper–latin list style":"{{Toggle the upper–latin list style}}"''',
    '''"Toggle the upper–roman list style":"{{Toggle the upper–roman list style}}"''',
    '''Turquoise:"{{Turquoise}}"''',
    '''Underline:"{{Underline}}"''',
    '''Undo:"{{Undo}}"''',
    '''Unlink:"{{Unlink}}"''',
    '''"Upload failed":"{{Upload failed}}"''',
    '''"Upload in progress":"{{Upload in progress}}"''',
    '''"Upper-latin":"{{Upper-latin}}"''',
    '''"Upper-roman":"{{Upper-roman}}"''',
    '''"Vertical text alignment toolbar":"{{Vertical text alignment toolbar}}"''',
    '''White:"{{White}}"''',
    '''"Widget toolbar":"{{Widget toolbar}}"''',
    '''Width:"{{Width}}"''',
    '''Yellow:"{{Yellow}}"''',
    '"{{Include note}}"',
    '"{{Insert math}}"',
    '"{{Insert equation in TeX format.}}"',
    '"{{Display mode}}"',
    '"{{Equation preview}}"',
    ':"{{Find and replace}}"',
    ':"{{Find in text…}}"',
    ':"{{Text to find must not be empty.}}"',
    ':"{{Find}}"',
    ':"{{Previous result}}"',
    ':"{{Next result}}"',
    ':"{{Replace with…}}"',
    ':"{{Show options}}"',
    ':"{{Match case}}"',
    ':"{{Whole words only}}"',
    ':"{{Replace}}"',
    ':"{{Replace all}}"',
    '"In line":"{{In line}}",',
    '"Toggle caption off":"{{Toggle caption off}}"',
    '"Toggle caption on":"{{Toggle caption on}}",',
    '"Upload image from computer":"{{Upload image from computer}}"',
    '"Special characters":"{{Special characters}}"',
    '"Character categories":"{{Character categories}}"',
    'Currency:"{{Currency}}"',
    ',Text:"{{Text}}",',
    'Mathematical:"{{Mathematical}}",',
    'Arrows:"{{Arrows}}"',
    'Latin:"{{Latin}}"',
    'All:"{{All}}",',
    '"Advanced options":"{{Advanced options}}",',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/widgets/type_widgets/web_view.js'
translation = [
    '>{{Web View}}<',
    '{{Note of type Web View allow you to embed websites into Trilium.}}',
    '{{To start, please create a label with a URL address you want to embed, e.g. <code>#webViewSrc="http://www.google.com"</code>}}',
    '{{Disclaimer on the experimental status}}',
    '{{Web View is an experimental note type, and it might be removed or substantially changed in the future. Web View works also only in the desktop build.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/watched_file_update_status.js'
translation = [
    '>{{File <code class="file-path"></code> has been last modified on <span class="file-last-modified"></span>.}}<',
    '>{{Upload modified file}}<',
    '>{{Ignore this change}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/services/export/opml.js'
translation = [
    '>{{Trilium export}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/export/zip.js'
translation = [
    r'''`<p>{{This is a clone of a note. Go to its <a href="${targetUrl}">primary location</a>.}}</p>`''',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/hidden_subtree.js'
translation = [
    '''title: "{{Open Today's Journal Note}}"''',
    "title: '{{Hidden Notes}}",
    "title: '{{Search History}}",
    "title: '{{Note Map}}",
    "title: '{{SQL Console History}}",
    "title: '{{Shared Notes}}",
    "title: '{{Bulk Action}}",
    "title: '{{Backend Log}}",
    "title: '{{User Hidden}}",
    "title: '{{Launch Bar Templates}}",
    "title: '{{Base Abstract Launcher}}",
    "title: '{{Command Launcher}}",
    "title: '{{Note Launcher}}",
    "title: '{{Script Launcher}}",
    "title: '{{Built-in Widget}}",
    "title: '{{Spacer}}",
    "title: '{{Custom Widget}}",
    "title: '{{Launch Bar}}",
    "title: '{{Available Launchers}}",
    "title: '{{Go to Previous Note}}",
    "title: '{{Go to Next Note}}",
    "title: '{{Visible Launchers}}",
    "title: '{{New Note}}",
    "title: '{{Search Notes}}",
    "title: '{{Jump to Note}}",
    "title: '{{Calendar}}",
    "title: '{{Recent Changes}}",
    "title: '{{Bookmarks}}",
    "title: '{{Protected Session}}",
    "title: '{{Sync Status}}",
    "title: '{{Options}}",
    "title: '{{Appearance}}",
    "title: '{{Shortcuts}}",
    "title: '{{Text Notes}}",
    "title: '{{Code Notes}}",
    "title: '{{Images}}",
    "title: '{{Spellcheck}}",
    "title: '{{Password}}",
    "title: '{{ETAPI}}",
    "title: '{{Backup}}",
    "title: '{{Sync}}",
    "title: '{{Other}}",
    "title: '{{Advanced}}",
    '',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/window.js'
translation = [
    "title: '{{Trilium Notes Setup}}",
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/services/attribute_parser.js'
translation = [
    '("{{Attribute name is empty, please fill the name.}}")',
    '{{`Invalid attribute "${text}" in ${context(i)}`}}',
    '`{{Attribute name "${attrName}" contains disallowed characters, only alphanumeric characters, colon and underscore are allowed.}}`',
    '{{`Missing value for label "${text}" in ${context(i)}`}}',
    '`{{Relation "${text}" in ${context(i)} should point to a note.}}`',
]

if TRANSLATE_NOTE_TAG:
    translation.extend(
        [
            "=== '{{inheritable}}'",
        ]
    )

replace_in_file(file_path, translation)

file_path = 'src/public/app/services/attribute_renderer.js'
translation = []
if TRANSLATE_NOTE_TAG:
    translation.extend(
        [
            ' `({{inheritable}})` ',
        ]
    )

replace_in_file(file_path, translation)

file_path = 'src/public/app/services/branches.js'
translation = [
    'title: "{{Delete status}}"',
    '"{{Delete notes in progress:}} "',
    '"{{Delete finished successfully.}}"',
    '"{{Undeleting notes finished successfully.}}"',
    "    alert('{{Cannot move notes before root note.}}'",
    "    alert('{{Cannot move notes after root note.}}'",
    '"{{Undeleting notes in progress:}} "',
    "'{{Cannot move notes here.}}'",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/bulk_action.js'
translation = [
    "title: '{{Labels}}',",
    "title: '{{Relations}}',",
    "title: '{{Notes}}',",
    "title: '{{Other}}',",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_autocomplete.js'
translation = [
    '`{{Create and link child note "${utils.escapeHtml(term)}"}}`',
    '`{{Insert external link to "${utils.escapeHtml(term)}"}}`',
    '"{{Clear text field}}"',
    '"{{Show recent notes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/services/date_notes.js'
translation = [
    "title: '{{Calendar}}",
    "'{{Sunday}}'",
    "'{{Monday}}'",
    "'{{Tuesday}}'",
    "'{{Wednesday}}'",
    "'{{Thursday}}'",
    "'{{Friday}}'",
    "'{{Saturday}}'",
    "'{{January}}'",
    "'{{February}}'",
    "'{{March}}'",
    "'{{April}}'",
    "'{{May}}'",
    "'{{June}}'",
    "'{{July}}'",
    "'{{August}}'",
    "'{{September}}'",
    "'{{October}}'",
    "'{{November}}'",
    "'{{December}}'",
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/keyboard_actions.js'
translation = [
    'separator: "{{Note navigation}}"',
    'separator: "{{Creating and moving notes}}"',
    'separator: "{{Note clipboard}}"',
    'separator: "{{Tabs & Windows}}"',
    'separator: "{{Dialogs}}"',
    'separator: "{{Text note operations}}"',
    'separator: "{{Attributes (labels & relations)}}"',
    'separator: "{{Ribbon tabs}}"',
    'separator: "{{Other}}"',
    """description: '{{Open "Jump to note" dialog}}'""",
    '''description: "{{Search for notes in the active note's subtree}}"''',
    'description: "{{Expand subtree of current note}}"',
    'description: "{{Collapses the complete note tree}}"',
    'description: "{{Collapses subtree of current note}}"',
    'description: "{{Sort child notes}}"',
    'description: "{{Create and open in the inbox (if defined) or day note}}"',
    'description: "{{Delete note}}"',
    'description: "{{Move note up}}"',
    'description: "{{Move note down}}"',
    'description: "{{Move note up in hierarchy}}"',
    'description: "{{Move note down in hierarchy}}"',
    'description: "{{Jump from tree to the note detail and edit title}}"',
    'description: "{{Show Edit branch prefix dialog}}"',
    'description: "{{Copy selected notes to the clipboard}}"',
    'description: "{{Paste notes from the clipboard into active note}}"',
    'description: "{{Cut selected notes to the clipboard}}"',
    'description: "{{Select all notes from the current note level}}"',
    'description: "{{Add note above to the selection}}"',
    'description: "{{Duplicate subtree}}"',
    'description: "{{Opens new tab}}"',
    'description: "{{Closes active tab}}"',
    'description: "{{Repoens the last closed tab}}"',
    'description: "{{Activates tab on the right}}"',
    'description: "{{Activates tab on the left}}"',
    'description: "{{Open new empty window}}"',
    'description: "{{Shows/hides the application from the system tray}}"',
    'description: "{{Activates the first tab in the list}}"',
    'description: "{{Activates the second tab in the list}}"',
    'description: "{{Activates the third tab in the list}}"',
    'description: "{{Activates the fourth tab in the list}}"',
    'description: "{{Activates the fifth tab in the list}}"',
    'description: "{{Activates the sixth tab in the list}}"',
    'description: "{{Activates the seventh tab in the list}}"',
    'description: "{{Activates the eigth tab in the list}}"',
    'description: "{{Activates the ninth tab in the list}}"',
    'description: "{{Activates the last tab in the list}}"',
    'description: "{{Shows Note Info dialog}}"',
    'description: "{{Shows Note Source dialog}}"',
    'description: "{{Shows Link Map dialog}}"',
    'description: "{{Shows Options dialog}}"',
    'description: "{{Shows Note Revisions dialog}}"',
    'description: "{{Shows Recent Changes dialog}}"',
    'description: "{{Shows SQL Console dialog}}"',
    'description: "{{Shows Backend Log dialog}}"',
    'description: "{{Shows built-in Help / cheatsheet}}"',
    'description: "{{Open dialog to add link to the text}}"',
    'description: "{{Follow link within which the caret is placed}}"',
    'description: "{{Insert current date & time into text}}"',
    'description: "{{Pastes Markdown from clipboard into text note}}"',
    'description: "{{Cuts the selection from the current note and creates subnote with the selected text}}"',
    'description: "{{Opens the dialog to include a note}}"',
    'description: "{{Edit a read-only note}}"',
    'description: "{{Put focus into attribute editor}}"',
    'description: "{{Create new label}}"',
    'description: "{{Create new relation}}"',
    'description: "{{Toggle Basic Properties}}"',
    'description: "{{Toggle Book Properties}}"',
    'description: "{{Toggle File Properties}}"',
    'description: "{{Toggle Image Properties}}"',
    'description: "{{Toggle Owned Attributes}}"',
    'description: "{{Toggle Inherited Attributes}}"',
    'description: "{{Toggle Promoted Attributes}}"',
    'description: "{{Toggle Link Map}}"',
    'description: "{{Toggle Note Info}}"',
    'description: "{{Toggle Note Paths}}"',
    'description: "{{Toggle Similar Notes}}"',
    'description: "{{Open note as a file with default application}}"',
    'description: "{{Render (re-render) active note}}"',
    'description: "{{Run active JavaScript (frontend/backend) code note}}"',
    'description: "{{Toggles note hoisting of active note}}"',
    'description: "{{Unhoist from anywhere}}"',
    'description: "{{Reload frontend App}}"',
    'description: "{{Open dev tools}}"',
    'description: "{{Toggle left (note tree) panel}}"',
    'description: "{{Toggle full screen}}"',
    'description: "{{Zoom Out}}"',
    'description: "{{Zoom In}}"',
    'description: "{{Reset zoom level}}"',
    'description: "{{Copy selected text without formatting}}"',
    'description: "{{Force creating / saving new note revision of the active note}}",',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/routes/api/image.js'
translation = [
    'message: "{{Unknown image type: }}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/routes/api/login.js'
translation = [
    '''message: "{{DB schema does not exist, can't sync.}}"''',
    '''message: "{{Sync login credentials are incorrect. It looks like you're trying to sync two different initialized documents which is not possible.}}"''',
    '''message: "{{Given current password doesn't match hash}}"''',
    """message: '{{Auth request time is out of sync, please check that both client and server have correct time.}}'""",
    'message: `{{Non-matching sync versions, local is version ${appInfo.syncVersion}, remote is ${syncVersion}. It is recommended to run same version of Trilium on both sides of sync.}}`',
    '{{Incorrect password}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/routes/api/sync.js'
translation = [
    'message: "{{Sync server host is not configured. Please configure sync first.}}"',
    'message: "{{Sync server handshake has been successful, sync has been started.}}"',
    'throw new Error(`{{Partial request ${requestId}, index ${pageIndex} of ${pageCount} of pages does not have expected record.}}`',
]
replace_in_file(file_path, translation, TARGET_PATH)

# 0.48
file_path = 'src/services/special_notes.js'
translation = [
    "title: '{{hidden}}',",
    "title: '{{search}}',",
    "title: '{{singles}}'",
    "title: '{{Global Note Map}}'",
    "title: '{{SQL Console}}'",
    "title: '{{Search}}: '",
    "title: '{{Shared notes}}',",
    "title: '{{SQL Console}} - '",
    'title: "{{Script Launcher}}",',
    'title: "{{Note Launcher}}",',
    'title: "{{Widget Launcher}}",',
    'title: "{{Spacer}}",',
]
replace_in_file(file_path, translation)
replace_in_file(file_path, translation, TARGET_PATH)

# 0.58.2 doc_notes
file_path = 'src/public/app/doc_notes/hidden.html'
translation = [
    '>{{Hidden tree is used to record various application-level data which can stay most of the time hidden from the user view.}}<',
    ">{{Make sure you know what you're doing. Incorrect changes in this subtree might potentially crash the application.}}<",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_command_launcher.html'
translation = [
    '>{{Keyboard shortcut for this launcher action can be configured in Options -> Shortcuts.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_history_navigation.html'
translation = [
    '>{{Back and Forward buttons allow you to move in the navigation history.}}<',
    '>{{These launchers are active only in the desktop build and will be ignored in the server edition where you can use the native browser navigation buttons instead.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_intro.html'
translation = [
    '>{{Welcome to the Launchbar configuration.}}<',
    '>{{You can do the following things here:}}<',
    '>{{Move available launchers to the visible list (thus putting them into the launchbar) by dragging them}}<',
    '>{{Move visible launchers to the available list (thus hiding them from the launchbar) by dragging them}}<',
    '>{{You can reorder the items in the lists by dragging}}<',
    '>{{You can create new launchers by right-clicking on the "Visible launchers" folder}}<',
    '>{{If you want to get back to the default setup, you can find "reset" in the context menu.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_note_launcher.html'
translation = [
    '>{{You can define the following attributes:}}<',
    # '>{{target}}<',
    '>{{ - note which should be opened upon activating the launcher}}<',
    # '>{{hoistedNote}}<',
    '>{{ - optional, will change the hoisted note before opening the target note}}<',
    # '>{{keyboardLauncher}}<',
    '>{{ - optional, pressing the keyboard shortcut will open the note}}<',
    '>{{Launchbar displays the title / icon from the launcher, which does not necessarily mirror those of the target note.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_script_launcher.html'
translation = [
    '>{{Script launcher can execute a script (code note) connected via }}<',
    # '>{{~script}}<',
    '>{{ relation.}}<',
    # '>{{script}}<',
    '>{{ - relation to the script note which should be executed upon launcher activation}}<',
    # '>{{keyboardLauncher}}<',
    '>{{ - optional, pressing the keyboard shortcut will activate the launcher}}<',
    '>{{Example script}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_spacer.html'
translation = [
    '>{{Spacer allows you to visually group launchers. You can configure it in the promoted attributes:}}<',
    # '>{{baseSize}}<',
    ">{{ - defines size in pixels (if there's enough space)}}<",
    # '>{{growthFactor}}<',
    '>{{ - set to 0 if you want the spacer to be of constant <code>baseSize</code>, with positive value it will grow.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/launchbar_widget_launcher.html'
translation = [
    '>{{Please define the target widget note in the promoted attributes. The widget will be used to render the launchbar icon.}}<',
    '>{{Example launchbar widget}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/share.html'
translation = [
    '>{{Here you can find all shared notes.}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/doc_notes/user_hidden.html'
translation = [
    '>{{This note serves as a subtree reserved for data produced by user scripts which should otherwise not freely create data in the hidden subtree.}}<',
]
replace_in_file(file_path, translation)

# 0.52
# 使用 Excalidraw 内置的语言文件
# use Excalidraw built-in language file
# https://github.com/excalidraw/excalidraw/blob/master/src/packages/excalidraw/README.md#langCode
file_path = 'src/public/app/widgets/type_widgets/canvas.js'
file_full_path = os.path.join(BASE_PATH, file_path)
if not os.path.exists(file_full_path):
    missing_files.append(file_full_path)
else:
    with open(file_full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not 'langCode' in content:
        content = content.replace(
            'excalidrawAPI: api => { this.excalidrawApi = api; },', 'excalidrawAPI: api => { this.excalidrawApi = api; },\n                    langCode: "zh-CN",'
        )
    with open(file_full_path, 'w') as f:
        f.write(content)

# 应用补丁
# apply patch
print(f'switch to dir: {BASE_PATH}')
os.chdir(BASE_PATH)
# os.system('npm install webpack --save-dev')
# os.system('npm run webpack')

# nvm managed environment
if os.path.exists('/usr/share/nvm/init-nvm.sh'):
    os.system('source /usr/share/nvm/init-nvm.sh && which webpack && webpack -c webpack.config.js')
else:
    os.system('which webpack')
    os.system('webpack -c webpack.config.js')

# 把编译好的文件复制到客户端里
# copy compiled file to the client
os.system(f'''cp -r {BASE_PATH}src/public/app-dist {CLIENT_PATH}resources/app/src/public/''')

# 你自己打开客户端看看翻译是否生效
# start the client MANUALLY BY YOURSELF to see if it works

# 创建补丁文件, 可以直接用在其它release里
# make patch files, which can be used by other platform release
if os.path.exists(PATCH_FOLDER):
    shutil.rmtree(PATCH_FOLDER)
os.mkdir(PATCH_FOLDER)

# src/public 目录下的要用node重新编译的文件
# src/public requires recompiled file with nodejs
shutil.copytree(f'{BASE_PATH}src/public/app-dist', f'{PATCH_FOLDER}/src/public/app-dist')
# doc notes
shutil.copytree(
    f'{BASE_PATH}src/public/app/doc_notes', f'{PATCH_FOLDER}/src/public/app-dist/doc_notes/'
)

# 其它目录直接用release版本的
# others can use the release client's file directly
shutil.copytree(f'{CLIENT_PATH}resources/app/src/views/', f'{PATCH_FOLDER}/src/views/')

shutil.copytree(f'{CLIENT_PATH}resources/app/src/services/', f'{PATCH_FOLDER}/src/services/')

shutil.copytree(f'{CLIENT_PATH}resources/app/src/routes/', f'{PATCH_FOLDER}/src/routes/')

# ckeditor
src_path = f'{CLIENT_PATH}resources/app/libraries/ckeditor/ckeditor.js'
dest_path = f'{PATCH_FOLDER}/libraries/ckeditor/ckeditor.js'
os.makedirs(os.path.dirname(dest_path), exist_ok=True)
shutil.copy(src_path, dest_path)
with open(dest_path, 'r') as f:
    content = f.read()

    # ckeditor 代码块通过中文的 · 触发
    # ckeditor code block trigger by chinese ·
    target_element = '/^```$/'
    new_element = '/^(```|···|｀｀｀)$/'
    if target_element in content:
        content = content.replace(target_element, new_element)

    # ckeditor 引用通过中文的 》 触发
    # ckeditor block quote trigger by chinese 》
    target_element = '/^>\\s$/'
    new_element = '/^(>|》)\\s$/'
    if target_element in content:
        content = content.replace(target_element, new_element)

with open(dest_path, 'w') as f:
    f.write(content)

# excalidraw 自定义字体
# excalidraw custom font
src_path = f'{script_path}/font/muyao-shouxie.ttf'
dest_path = (
    f'{PATCH_FOLDER}/node_modules/@excalidraw/excalidraw/dist/excalidraw-assets/Virgil.woff2'
)
os.makedirs(os.path.dirname(dest_path), exist_ok=True)
shutil.copy(src_path, dest_path)

if LANG == 'cn':
    # 内置文档
    # built-in demo notes
    os.chdir(script_path)
    if os.path.exists('demo-cn.zip'):
        os.system('rm -f demo-cn.zip')
    # trilium需要读取unicode格式的zip文件名, 否则会出现乱码
    os.system('cd demo-cn && 7z -scsutf-8 a demo-cn.zip ./* && mv demo-cn.zip ../')
    src_path = f'demo-cn.zip'
    dest_path = f'{PATCH_FOLDER}/db/demo.zip'
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy(src_path, dest_path)

print('=====================================')
if missing_files:
    print('missing_files! \n')
    for x in missing_files:
        print(x)
else:
    print('no missing file, good!')
print('=====================================')
unused_translations = [key for key in translation_dict if key and key not in used_translations]
if unused_translations:
    print('unused_translations! \n')
    for x in unused_translations:
        print(x)
else:
    print('no unused translation, good!')
print('=====================================')
if missing_translations:
    print('missing_translations! \n')
    for x in missing_translations:
        print(x)
else:
    print('no missing translation, good!')
print('=====================================')

# 尝试删除electron的缓存, 避免代码修改不生效的问题
# try delete electron cache, avoid code change does not take effect
try:
    shutil.rmtree(os.path.expanduser('~/.config/Trilium Notes/'))
except:
    pass

print('finished!')
