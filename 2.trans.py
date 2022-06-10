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

missing_files = []


def translate(m):
    # print(m)
    trans = translation_dict.get(m.group(1), m.group(1))
    if not trans:
        trans = m.group(1)
    return trans


def replace_in_file(file_path, translation, base_path=BASE_PATH):
    file_full_path = os.path.join(base_path, file_path)
    if not os.path.exists(file_full_path):
        missing_files.append(file_full_path)
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
about_file_path = f'{TARGET_PATH}src/views/dialogs/about.ejs'
with open(about_file_path, 'r') as f:
    content = f.read()
    if TRANSLATOR_LABEL not in content:
        content = content.replace('                </table>',
                                  f'\n                    <tr>\n                        <th>{TRANSLATOR_LABEL}:</th>\n                        <td><a href="{TRANSLATOR_URL}" class="external">{TRANSLATOR_URL}</a></td>\n                    </tr>\n                </table>')
with open(about_file_path, 'w') as f:
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
    "{{I'm a new user, and I want to create new Trilium document for my notes}}",
    '{{I have desktop instance already, and I want to set up sync with it}}',
    '{{I have server instance already, and I want to set up sync with it}}',
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
    '    {{parent: }}<'
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/desktop.js'
translation = [
    'title: `{{Add "${params.misspelledWord}" to dictionary}}`',
    'title: `{{Cut}}',
    'title: `{{Copy}}',
    'title: `{{Copy link}}`',
    'title: `{{Paste as plain text}}',
    'title: `{{Paste}}',
    'title: `{{Search for "${shortenedSelection}" with DuckDuckGo}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/views/dialogs/about.ejs'
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
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/add_link.ejs'
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
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/backend_log.ejs'
translation = [
    '>{{Backend log}}<',
    '>{{Refresh}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/branch_prefix.ejs'
translation = [
    '>{{Edit branch prefix}}<',
    '>{{Prefix}}: <',
    '>{{Save}}<',
    'title="{{Help on Tree prefix}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/clone_to.ejs'
translation = [
    '>{{Clone notes to ...}}<',
    '>{{Notes to clone}}<',
    '>{{Target parent note}}<',
    '>{{Prefix (optional)}}<',
    '>{{Clone to selected note }}<',
    '>{{enter}}<',
    'title="{{Help on links}}"',
    'title="{{Cloned note will be shown in note tree with given prefix}}"',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/confirm.ejs'
translation = [
    '>{{Confirmation}}<',
    '>{{Cancel}}<',
    '>{{OK}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/delete_notes.ejs'
translation = [
    '>{{Delete notes preview}}<',
    '>{{Following notes will be deleted (}}<',
    '>{{Following relations will be broken and deleted (}}<',
    '>{{Cancel}}<',
    '>{{OK}}<',
    '    {{delete also all clones}}',
    '''title="{{Normal (soft) deletion only marks the notes as deleted and they can be undeleted (in recent changes dialog) within a period of time. Checking this option will erase the notes immediatelly and it won't be possible to undelete the notes.}}"''',
    '''        {{erase notes permanently (can't be undone). This will force application reload.}}''',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/export.ejs'
translation = [
    '>{{Export note "}}<',
    '>{{this note and all of its descendants}}<',
    '>{{HTML in ZIP archive - this is recommended since this preserves all the formatting.}}<',
    '>{{OPML v1.0 - plain text only}}<',
    '>{{OMPL v2.0 - allows also HTML}}<',
    '>{{only this note without its descendants}}<',
    '>{{HTML - this is recommended since this preserves all the formatting.}}<',
    '>{{Export}}<',
    '{{this preserves most of the formatting.}}',
    '{{outliner interchange format for text only. Formatting, images and files are not included.}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/help.ejs'
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
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/import.ejs'
translation = [
    '>{{Import into note}}<',
    '>{{Choose import file}}<',
    '>{{Content of the file will be imported as child note(s) into }}<',
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
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/include_note.ejs'
translation = [
    '>{{Include note}}<',
    '>{{Note}}<',
    '>{{Include note }}<',
    '>{{enter}}<',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/info.ejs'
translation = [
    '>{{Info message}}<',
    '>{{OK}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/jump_to_note.ejs'
translation = [
    '>{{Jump to note}}<',
    '>{{Note}}<',
    '>{{Search in full text }}<',
    '>{{Ctrl+Enter}}<',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/link_map.ejs'
translation = [
    '>{{Link map}}<',
    '>{{max notes:}}<',
    'title="{{Max number of displayed notes}}"',
    'title="{{Help on Link map}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/markdown_import.ejs'
translation = [
    '>{{Markdown import}}<',
    ">{{Because of browser sandbox it's not possible to directly read clipboard from JavaScript. Please paste the Markdown to import to textarea below and click on Import button}}<",
    '>{{Import }}<',
    '>{{Ctrl+Enter}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/move_to.ejs'
translation = [
    '>{{Move notes to ...}}<',
    '>{{Notes to move}}<',
    '>{{Target parent note}}<',
    '>{{Move to selected note }}<',
    '>{{enter}}<',
    '{{search for note by its name}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/note_info.ejs'
translation = [
    '>{{Note info}}<',
    '>{{Note ID}}<',
    '>{{Date created}}<',
    '>{{Date modified}}<',
    '>{{Type}}<',
    '>{{MIME}}<',
    '>{{OK}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/note_revisions.ejs'
translation = [
    '>{{Note revisions}}<',
    '>{{Delete all revisions}}<',
    '>{{Dropdown trigger}}<',
    'title="{{Delete all revisions of this note}}"',
    'title="{{Help on Note revisions}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/note_source.ejs'
translation = [
    '>{{Note source}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/options.ejs'
translation = [
    '>{{Options}}<',
    '>{{Appearance}}<',
    '>{{Shortcuts}}<',
    '>{{Keyboard shortcuts}}<',
    '>{{Code notes}}<',
    # removed from 0.50
    # '>{{Username & password}}<',
    '>{{Password}}<',
    '>{{ETAPI}}<',
    '>{{Backup}}<',
    '>{{Sync}}<',
    '>{{Other}}<',
    '>{{Advanced}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/password_not_set.ejs'
translation = [
    '>{{Password is not set}}<',
    '{{Protected notes are encrypted using a user password, but password has not been set yet.}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/prompt.ejs'
translation = [
    '>{{Prompt}}<',
    '>{{OK }}<',
    '>{{enter}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/protected_session_password.ejs'
translation = [
    '>{{Protected session}}<',
    '>{{To proceed with requested action you need to start protected session by entering password:}}<',
    '>{{Start protected session }}<',
    '>{{enter}}<',
    'title="{{Help on Protected notes}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/recent_changes.ejs'
translation = [
    '>{{Recent changes}}<',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/views/dialogs/sort_child_notes.ejs'
translation = [
    '>{{Sort children by ...}}<',
    '>{{Sorting criteria}}<',
    '>{{Sorting direction}}<',
    '>{{Sort }}<',
    '>{{enter}}<',
    '    {{title}}',
    '    {{date created}}',
    '    {{date modified}}',
    '    {{ascending}}',
    '    {{descending}}',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/dialogs/add_link.js'
translation = [
    '    logError("{{No link to add.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/clone_to.js'
translation = [
    '{{`Note "${clonedNote.title}" has been cloned into ${targetNote.title}`}}',
    '    logError("{{No path to clone to.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/confirm.js'
translation = [
    '{{Are you sure you want to remove the note "${title}" from relation map?}}',
    "{{If you don't check this, note will be only removed from relation map, but will stay as a note.}}",
    '{{Also delete note}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/delete_notes.js'
translation = [
    '{{Note}} ',
    '` {{(to be deleted) is referenced by relation <code>${attr.name}</code> originating from}} `',

]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/advanced.js'
translation = [
    '>{{Sync}}<',
    '>{{Force full sync}}<',
    '>{{Fill entity changes records}}<',
    '>{{Database integrity check}}<',
    '>{{This will check that the database is not corrupted on the SQLite level. It might take some time, depending on the DB size.}}<',
    '>{{Check database integrity}}<',
    '>{{Consistency checks}}<',
    '>{{Find and fix consistency issues}}<',
    '>{{Anonymize database}}<',
    '>{{Full anonymization}}<',
    '>{{Save fully anonymized database}}<',
    '>{{Light anonymization}}<',
    '>{{This action will create a new copy of the database and do a light anonymization on it - specifically only content of all notes will be removed, but titles and attributes will remaing. Additionally, custom JS frontend/backend script notes and custom widgets will remain. This provides more context to debug the issues.}}<',
    '>{{You can decide yourself if you want to provide fully or lightly anonymized database. Even fully anonymized DB is very useful, however in some cases lightly anonymized database can speed up the process of bug identification and fixing.}}<',
    '>{{Save lightly anonymized database}}<',
    '>{{Save anonymized database}}<',
    '>{{Backup database}}<',
    '>{{Trilium has automatic backup (daily, weekly, monthly), but you can also trigger a manual backup here.}}<',
    '>{{Backup database now}}<',
    '>{{Vacuum database}}<',
    '>{{This will rebuild the database which will typically result in a smaller database file. No data will be actually changed.}}<',
    '>{{Vacuum database}}<',
    '{{This action will create a new copy of the database and anonymize it}}',
    '{{remove all note content and leave only structure and some non-sensitive metadata}}',
    '{{for sharing online for debugging purposes without fear of leaking your personal data.}}',
    'showMessage(`{{Created fully anonymized database in ${resp.anonymizedFilePath}}}`',
    'showMessage(`{{Created lightly anonymized database in ${resp.anonymizedFilePath}}}`',
    'showMessage("{{Full sync triggered}}"',
    'showMessage("{{Sync rows filled successfully}}"',
    'showMessage("{{Database has been backed up to }}"',
    'showMessage("{{Database has been vacuumed}}"',
    'showMessage("{{Consistency issues should be fixed.}}"',
    'showError("{{Could not create anonymized database, check backend logs for details}}"',
    'showMessage("{{Integrity check succeeded - no problems found.}}"',
    'showMessage("{{Integrity check failed: }}"',
    'showMessage({{`Created anonymized database in ${resp.anonymizedFilePath}`}}',

]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/appearance.js'
translation = [
    '>{{Theme}}<',
    '{{Settings on this options tab are saved automatically after each change.}}',
    '>{{Zoom factor (desktop build only)}}<',
    '>{{Native title bar (requires app restart)}}<',
    '>{{enabled}}<',
    '>{{disabled}}<',
    '>{{Heading style}}<',
    '>{{Zooming can be controlled with CTRL+- and CTRL+= shortcuts as well.}}<',
    '>{{Font sizes}}<',
    '>{{Main font size}}<',
    '>{{Note tree font size}}<',
    '>{{Note detail font size}}<',
    '>{{Note that tree and detail font sizing is relative to the main font size setting.}}<',
    "title: '{{White}}'",
    "title: '{{Dark}}'",
    "title: '{{Black}}'",
    '>{{Plain}}<',
    '>{{Markdown-style}}<',
    '>{{Underline}}<',
    '>{{Override theme fonts}}<',
    '>{{Fonts}}<',
    '>{{Main font}}<',
    '>{{Font family}}<',
    '>{{Size}}<',
    '>{{%}}<',
    '>{{Note tree font}}<',
    '>{{Note detail font}}<',
    '>{{Monospace font}}<',
    '>{{Not all listed fonts may be available on your system.}}<',
    '>{{reload frontend}}<',
    "title: '{{Light}}",
    '"{{Theme defined}}"',
    '        {{To apply font changes, click on}}',
    '>{{Content width}}<',
    '>{{Trilium by default limits max content width to improve readability for maximized screens on wide screens.}}<',
    '>{{Max content width in pixels}}<',
    '        {{To content width changes, click on}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/backup.js'
translation = [
    '>{{Automatic backup}}<',
    '>{{Trilium can back up the database automatically:}}<',
    '>{{Enable daily backup}}<',
    '>{{Enable weekly backup}}<',
    '>{{Enable monthly backup}}<',
    '''>{{It's recommended to keep the backup turned on, but this can make application startup slow with large databases and/or slow storage devices.}}<''',
    '>{{Backup now}}<',
    '>{{Backup database now}}<',
    'showMessage("{{Database has been backed up to }}"',
    'showMessage("{{Options changed have been saved.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/recent_changes.js'
translation = [
    '{{No changes yet ...}}',
    '{{Do you want to undelete this note and its sub-notes?}}',
    'text("{{undelete}}")',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/branch_prefix.js'
translation = [
    'showMessage("{{Branch prefix has been saved.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/export.js'
translation = [
    'title: "{{Export status}}"',
    'throw new Error("{{Unrecognized type }}"',
    '    alert("{{Choose export type first please}}"',
    '"{{Export in progress:}} "',
    '"{{Export finished successfully.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/include_note.js'
translation = [
    '    logError("{{No noteId to include.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/markdown_import.js'
translation = [
    'showMessage("{{Markdown content has been imported into the document.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/move_to.js'
translation = [
    'showMessage({{`Selected notes have been moved into ${parentNote.title}`}}',
    '    logError("{{No path to move to.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/note_revisions.js'
translation = [
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

file_path = 'src/public/app/dialogs/options/code_notes.js'
translation = [
    '>{{Use vim keybindings in CodeNotes (no ex mode)}}<',
    '>{{Enable Vim Keybindings}}<',
    '>{{Available MIME types in the dropdown}}<',
    'showMessage("{{Options change have been saved.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/etapi.js'
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
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/credentials.js'
translation = [
    '>{{Username}}<',
    '>{{Your username is}} <',
    '>{{Change password}}<',
    '>{{Old password}}<',
    '>{{New password}}<',
    '>{{New password Confirmation}}<',
    '{{Please take care to remember your new password. Password is used to encrypt protected notes. If you forget your password, then all your protected notes are forever lost with no recovery options.}}',
    '"{{New passwords are not the same.}}"',
    '{{Password has been changed. Trilium will be reloaded after you press OK.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/keyboard_shortcuts.js'
translation = [
    '>{{Keyboard shortcuts}}<',
    '>{{Multiple shortcuts for the same action can be separated by comma.}}<',
    '>{{Action name}}<',
    '>{{Shortcuts}}<',
    '>{{Default shortcuts}}<',
    '>{{Description}}<',
    '>{{Reload app to apply changes}}<',
    '>{{Set all shortcuts to the default}}<',
    'placeholder="{{Type text to filter shortcuts...}}"',
    'confirmDialog.confirm("{{Do you really want to reset all keyboard shortcuts to the default?}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/other.js'
translation = [
    '>{{Spell check}}<',
    '>{{These options apply only for desktop builds, browsers will use their own native spell check. App restart is required after change.}}<',
    '>{{Enable spellcheck}}<',
    '>{{Language code(s)}}<',
    '>{{Multiple languages can be separated by comma, e.g. }}<',
    '>{{Changes to the spell check options will take effect after application restart}}<',
    '>{{Available language codes: }}<',
    '>{{Images}}<',
    '>{{Download images automatically for offline use.}}<',
    '>{{(pasted HTML can contain references to online images, Trilium will find those references and download the images so that they are available offline)}}<',
    '>{{Image compression}}<',
    '>{{Enable image compression}}<',
    '>{{Max width / height of an image in pixels (image will be resized if it exceeds this setting).}}<',
    '>{{JPEG quality (10 - worst quality, 100 best quality, 50 - 85 is recommended)}}<',
    '>{{Note erasure timeout}}<',
    '>{{Erase notes after X seconds}}<',
    '>{{You can also trigger erasing manually:}}<',
    '>{{Erase deleted notes now}}<',
    '>{{Protected session timeout}}<',
    '>{{Protected session timeout (in seconds)}}<',
    '>{{Note revisions snapshot interval}}<',
    '>{{Note revision snapshot time interval is time in seconds after which a new note revision will be created for the note. See }}<',
    '>{{Note revision snapshot time interval (in seconds)}}<',
    '>{{Deleted notes (and attributes, revisions...) are at first only marked as deleted and it is possible to recover them \n    from Recent Notes dialog. After a period of time, deleted notes are "erased" which means \n    their content is not recoverable anymore. This setting allows you to configure the length \n    of the period between deleting and erasing the note.}}<',
    "{{Protected session timeout is a time period after which the protected session is wiped from\n        the browser's memory. This is measured from the last interaction with protected notes. See}}",
    '{{for more info.}}',
    '>. {{Changes to the spell check options will take effect after application restart.}}<',
    'showMessage("{{Options changed have been saved.}}"',
    'showMessage("{{Deleted notes have been erased.}}"',
    '>{{Automatic readonly size}}<',
    '>{{Automatic readonly note size is the size after which notes will be displayed in a readonly mode (for performance reasons).}}<',
    '>{{Automatic readonly size (text notes)}}<',
    '>{{Automatic readonly size (code notes)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/password.js'
translation = [
    '>{{click here to reset it}}<',
    '>{{Old password}}<',
    '>{{New password}}<',
    '>{{New password Confirmation}}<',
    '>{{Change password}}<',
    '    alert("{{Password has been reset. Please set new password}}"',
    '    alert("{{New passwords are not the same.}}"',
    '    alert("{{Password has been changed. Trilium will be reloaded after you press OK.}}"',
    '{{Please take care to remember your new password. Password is used to encrypt protected notes. }}',
    '{{If you forget your password, then all your protected notes are forever lost.}}',
    '{{In case you did forget your password}}',
    '"{{By resetting the password you will forever lose access to all your existing protected notes. Do you really want to reset the password?}}"',
    "'{{Change password}}' : '{{Set password}}')",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/shortcuts.js'
translation = [
    '>{{Keyboard shortcuts}}<',
    '>{{Multiple shortcuts for the same action can be separated by comma.}}<',
    '>{{Action name}}<',
    '>{{Shortcuts}}<',
    '>{{Default shortcuts}}<',
    '>{{Description}}<',
    '>{{Reload app to apply changes}}<',
    '>{{Set all shortcuts to the default}}<',
    'confirmDialog.confirm("{{Do you really want to reset all keyboard shortcuts to the default?}}"',
    '{{Type text to filter shortcuts...}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/dialogs/options/sync.js'
translation = [
    '>{{Sync configuration}}<',
    '>{{Server instance address}}<',
    '>{{Sync timeout (milliseconds)}}<',
    '>{{Sync proxy server (optional)}}<',
    '>{{Note:}}<',
    '> {{If you leave the proxy setting blank, the system proxy will be used (applies to desktop/electron build only)}}<',
    '>{{Save}}<',
    '>{{Help}}<',
    '>{{Sync test}}<',
    ">{{This will test the connection and handshake to the sync server. If the sync server isn't initialized, this will set it up to sync with the local document.}}<",
    '>{{Test sync}}<',
    'showMessage("{{Options changed have been saved.}}"',
    '"{{Sync server handshake failed, error:}} "',
]
replace_in_file(file_path, translation)

file_path = 'src/services/change_password.js'
translation = [
    '''message: "{{Given current password doesn't match hash}}"''',
]
replace_in_file(file_path, translation, TARGET_PATH)

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

# no need for translate for now
file_path = 'src/services/search/services/search.js'
translation = [
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/services/sql_init.js'
translation = [
    "title: '{{root}}",
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

file_path = 'src/public/app/entities/note_short.js'
translation = [
    'throw new Error(`{{Note ${this.noteId} is of type ${this.type} and mime ${this.mime} and thus cannot be executed}}`',
    'throw new Error({{`Unrecognized env type ${env} for note ${this.noteId}`}}',
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

file_path = 'src/public/app/services/app_context.js'
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

file_path = 'src/public/app/services/entrypoints.js'
translation = [
    "title: '{{new note}}",
    'showMessage("{{Note executed}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/froca.js'
translation = [
    'throw new Error(`{{Search note ${note.noteId} failed: ${searchResultNoteIds}}}`',
    'throw new Error("{{Empty noteId}}"',
    '    logError(`{{Not existing branch ${branchId}}}`',
    '    logError(`{{Could not find branchId for parent=${parentNoteId}, child=${childNoteId} since child does not exist}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/froca_updater.js'
translation = [
    'throw new Error(`{{Unknown entityName ${ec.entityName}}}`',
    """throw new Error(`{{Can't process entity ${JSON.stringify(ec)} with error ${e.message} ${e.stack}}}`""",
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

file_path = 'src/public/app/services/tab_manager.js'
translation = [
    """throw new Error(`{{Cannot find noteContext id='${ntxId}'}}`""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/tab_context.js'
translation = [
    '    logError({{`Cannot resolve note path ${inputNotePath}`}}',
    """    logError(`{{Cannot find tabContext's note id='${this.noteId}'}}`""",
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
    'confirmDialog.confirm("{{Requested note is outside of hoisted note subtree and you must unhoist to access the note. Do you want to proceed with unhoisting?}}"',
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

file_path = 'src/public/app/services/link_context_menu.js'
translation = [
    'title: "{{Open note in a new tab}}"',
    'title: "{{Open note in a new split}}"',
    'title: "{{Open note in a new window}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/entrypoints.js'
translation = [
    "title: '{{new note}}",
    'showMessage("{{Note executed}}"',
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

file_path = 'src/public/app/services/note_content_renderer.js'
translation = [
    '>{{Download}}<',
    '>{{Open}}<',
    '>{{The diagram could not displayed.}}<',
    '>{{ Enter protected session}}<',
    '>{{This note is protected and to access it you need to enter password.}}<',
    '>{{Content of this note cannot be displayed in the book format}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_context.js'
translation = [
    '    logError(`{{Cannot resolve note path ${inputNotePath}}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_list_renderer.js'
translation = [
    'title="{{Collapse all notes}}"',
    'title="{{Expand all children}}"',
    'title="{{List view}}"',
    'title="{{Grid view}}"',
    'throw new Error({{`Invalid view type ${type}`}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/note_tooltip.js'
translation = [
    '>{{Note has been deleted.}}<',
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

file_path = 'src/public/app/services/tree_cache.js'
translation = [
    'throw new Error({{`Search note ${note.noteId} failed: ${searchResultNoteIds}`}}',
    'throw new Error("{{Empty noteId}}"',
    '    logError({{`Not existing branch ${branchId}`}}',
    '    logError(`{{Could not find branchId for parent=${parentNoteId}, child=${childNoteId} since child does not exist}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/services/tree_context_menu.js'
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
    # special colon
    "title: `{{Duplicate subtree}}",
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
    "{{new search notes will be created as children of this note when hoisted to some ancestor of this note}}",
    "{{new search notes will be created as children of this note}}",
    "{{default inbox location for new notes when hoisted to some ancestor of this note}}",
    "{{default inbox location for new notes}}",
    "{{default location of SQL console notes}}",
    "{{note with this label will appear in bookmarks as folder (allowing access to its children)}}",
    "{{note with this label will appear in bookmarks}}",
    "{{this note is hidden from left navigation tree, but still accessible with its URL}}",
    "{{define an alias using which the note will be available under https://your_trilium_host/share/[your_alias]}}",
    "{{default share page CSS will be omitted. Use when you make extensive styling changes.}}",
    "{{marks note which is served on /share root.}}",
    "{{note will be served in its raw format, without HTML wrapper}}",
    "{{will forbid robot indexing of this note via <code>X-Robots-Tag: noindex</code> header}}",
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
    "{{<code>\${parentNote.getLabelValue('authorName')}'s literary works</code>}}",
    "{{<code>Log for \${now.format('YYYY-MM-DD HH:mm:ss')}</code>}}",
    '{{See <a href="https://github.com/zadam/trilium/wiki/Default-note-title">wiki with details</a>, API docs for <a href="https://zadam.github.io/trilium/backend_api/Note.html">parentNote</a> and <a href="https://day.js.org/docs/en/display/format">now</a> for details.}}',
    "'{{see}} <",
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
    '"{{Hide panel.}}"',
    '"{{Open panel.}}"',
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

file_path = 'src/public/app/widgets/backlinks.js'
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
    '            {{Open new window}}',
    '            {{Open Dev Tools}}',
    '            {{Open SQL Console}}',
    '            {{Show backend log}}',
    '            {{Reload frontend}}',
    'title="{{Reload can help with some visual glitches without restarting the whole app.}}"',
    '            {{Toggle fullscreen}}',
    '            {{Show Help}}',
    '            {{About Trilium Notes}}',
    '            {{Logout}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/note_actions.js'
translation = [
    '>{{ Re-render note}}<',
    '>{{Search in note }}<',
    '>{{ Note source}}<',
    '>{{ Open note externally}}<',
    '>{{Import files}}<',
    '>{{Export note}}<',
    '>{{ Print note}}<',
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

file_path = 'src/public/app/widgets/buttons/show_note_source.js'
translation = [
    'title("{{Show Note Source}}")',

]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/buttons/update_available.js'
translation = [
    'title="{{Update available}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/calendar.js'
translation = [
    '"{{Calendar}}"',
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
    '>{{Mon}}<',
    '>{{Tue}}<',
    '>{{Wed}}<',
    '>{{Thu}}<',
    '>{{Fri}}<',
    '>{{Sat}}<',
    '>{{Sun}}<',
    '"{{Cannot find day note}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widget.js'
translation = [
    '{{Collapsible Group Item}}',
    '"{{Untitled widget}}"',
    'title="{{Minimize/maximize widget}}"',
    '"title", "{{Hide}}"',
    '"title", "{{Show}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/edited_notes.js'
translation = [
    '"{{Edited notes on this day}}"',
    '>{{No edited notes on this day yet ...}}<',
    'title: "{{This contains a list of notes created or updated on this day.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/link_map.js'
translation = [
    '"{{Link map}}"',
    'title: "{{Link map shows incoming and outgoing links from/to the current note.}}"',
    "'{{Show full link map}}'",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/note_info.js'
translation = [
    '"{{Note info}}"',
    '>{{Note ID}}:<',
    '>{{Type:}}</',
    '>{{Created}}:<',
    '>{{Modified}}:<',
    '>{{Note size}}:<',
    'span> {{calculate}}',
    '''"{{Note size provides rough estimate of storage requirements for this note. It takes into account note's content and content of its note revisions.}}"''',
    '"({{subtree size}}: "',
    r'` {{in ${subTreeResp.subTreeNoteCount} notes)}}`',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/note_revisions.js'
translation = [
    '"{{Note revisions}}"',
    '"{{No revisions yet...}}"',
    "'{{This revision was last edited on}} '",
    '"{{Note revisions track changes in the note across the time.}}"',
    "'{{Show Note revisions dialog}}'",
    "title: '{{This revision was last edited on}} ",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/collapsible_widgets/what_links_here.js'
translation = [
    '"{{What links here}}"',
    '"{{Nothing links here yet ...}}"',
    'title: "{{This list contains all notes which link to this note through links and relations.}}"',
    '{{more links ...}}`',
    "'{{Show full link map}}'",
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

file_path = 'src/public/app/widgets/mobile_widgets/mobile_global_buttons.js'
translation = [
    '>{{No plugin buttons loaded yet.}}<',
    '> {{Switch to desktop version}}<',
    '> {{Logout}}<',
    'title="{{New note}}"',
    'title="{{Collapse note tree}}"',
    'title="{{Scroll to active note}}"',
    'title="{{Plugin buttons}}"',
    'title="{{Global actions}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/delete_label.js'
translation = [
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/delete_note.js'
translation = [
    '    {{Delete matched notes}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/delete_note_revisions.js'
translation = [
    '    {{Delete note revisions}}',
    "{{All past note revisions of matched notes will be deleted. Note itself will be fully preserved. In other terms, note's history will be removed.}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/delete_relation.js'
translation = [
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    '{{Delete relation:}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/execute_script.js'
translation = [
    '{{Execute script:}}',
    '{{You can execute simple scripts on the matched notes.}}',
    "{{For example to append a string to a note's title, use this small script:}}",
    "{{More complex example would be deleting all matched note's attributes:}}",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/move_note.js'
translation = [
    '>{{Move note}}<',
    '>{{to}}<',
    '>{{On all matched notes:}}<',
    '>{{move note to the new parent if note has only one parent (i.e. the old placement is removed and new placement into the new parent is created)}}<',
    ">{{clone note to the new parent if note has multiple clones/placements (it's not clear which placement should be removed)}} <",
    '>{{nothing will happen if note cannot be moved to the target note (i.e. this would create a tree cycle)}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/rename_label.js'
translation = [
    '>{{Rename label from:}}<',
    '>{{To:}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/rename_relation.js'
translation = [
    '>{{Rename relation from:}}<',
    '>{{To:}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/set_label_value.js'
translation = [
    '>{{Set label}}<',
    '>{{to value}}<',
    '>{{On all matched notes:}}<',
    ">{{create given label if note doesn't have one yet}}<",
    '>{{or change value of the existing label}}<',
    '>{{You can also call this method without value, in such case label will be assigned to the note without value.}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_actions/set_relation_target.js'
translation = [
    '>{{Set relation}}<',
    '>{{to}}<',
    '>{{On all matched notes:}}<',
    ">{{create given relation if note doesn't have one yet}} <",
    '>{{or change target note of the existing relation}}<',
    'title="{{Alphanumeric characters, underscore and colon are allowed characters.}}"',
    ">{{create given relation if note doesn't have one yet}}<",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/search_options/ancestor.js'
translation = [
    '>{{Ancestor:}}<',
    '{{search for note by its name}}',
    '>{{depth:}}<',
    ">{{doesn't mattter}}<",
    '>{{is exactly 1 (direct children)}}<',
    '>{{is exactly 2}}<',
    '>{{is exactly 3}}<',
    '>{{is exactly 4}}<',
    '>{{is exactly 5}}<',
    '>{{is exactly 6}}<',
    '>{{is exactly 7}}<',
    '>{{is exactly 8}}<',
    '>{{is exactly 9}}<',
    '>{{is greater than 1}}<',
    '>{{is greater than 2}}<',
    '>{{is greater than 3}}<',
    '>{{is greater than 4}}<',
    '>{{is greater than 5}}<',
    '>{{is greater than 6}}<',
    '>{{is greater than 7}}<',
    '>{{is greater than 8}}<',
    '>{{is greater than 9}}<',
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

file_path = 'src/public/app/widgets/global_menu.js'
translation = [
    '    {{Options}}',
    '    {{Open new window}}',
    '    {{Open Dev Tools}}',
    '    {{Open SQL Console}}',
    '    {{Show backend log}}',
    '    {{Reload frontend}}',
    '    {{Toggle Zen mode}}',
    '    {{Toggle fullscreen}}',
    '    {{Show Help}}',
    '    {{About Trilium Notes}}',
    '    {{Logout}}',
    'title="{{Menu}}"',
    'title="{{Reload can help with some visual glitches without restarting the whole app.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/history_navigation.js'
translation = [
    'title="{{Go to previous note.}}"',
    'title="{{Go to next note.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/mermaid.js'
translation = [
    '>{{The diagram could not displayed. See }}<',
    '>{{help and examples}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_actions.js'
translation = [
    '>{{ Re-render note}}<',
    '>{{Search in note }}<',
    '>{{Revisions}}<',
    '>{{ Link map}}<',
    '>{{ Note source}}<',
    '>{{ Open note externally}}<',
    '>{{Import files}}<',
    '>{{Export note}}<',
    '>{{ Print note}}<',
    '>{{ Note info}}<',
    'title="{{Note is not protected, click to make it protected}}"',
    'title="{{Note is protected, click to make it unprotected}}"',
    '        {{Actions}}',
    '        {{Protect the note}}',
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

file_path = 'src/public/app/widgets/note_paths.js'
translation = [
    'title="{{Note paths}}"',
    'title="{{This path is outside of hoisted note and you would have to unhoist.}}"',
    'title="{{Archived}}"',
    'title="{{Search}}"',
    '{{This note is placed into the following paths:}}',
    '{{Clone note to new location...}}',
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

]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_type.js'
translation = [
    'title: "{{File}}"',
    'title: "{{Image}}"',
    # dirty
    'title: "{{Saved search}}"',
    'title: "{{Note Map}}"',
    'title: "{{Text}}"',
    'title: "{{Relation Map}}"',
    'title: "{{Render Note}}"',
    'title: "{{Canvas}}"',
    'title: "{{Book}}"',
    'title: "{{Mermaid Diagram}}"',
    'title: "{{Code}}"',
    '    {{Type:}} <span',
    'confirmDialog.confirm("{{It is not recommended to change note type when note content is not empty. Do you want to continue anyway?}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/note_update_status.js'
translation = [
    '>{{File }}<',
    '>{{ has been last modified on }}<',
    '>{{Upload modified file}}<',
    '>{{Ignore this change}}<',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/protected_note_switch.js'
translation = [
    '"title", "{{Note is not protected, click to make it protected}}"',
    '"title", "{{Note is protected, click to make it unprotected}}"',
    '"{{Protect the note}}"',
    '"{{Unprotect the note}}"',
]
replace_in_file(file_path, translation)
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/public/app/widgets/quick_search.js'
translation = [
    # 0.47
    '>{{Searching ...}}<',
    # 0.48
    '>{{ Searching ...}}<',
    '>{{No results found}}<',
    '>{{... and ${resultNoteIds.length - MAX_DISPLAYED_NOTES} more results.}}<',
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
    'throw new Error(`{{Invalid view type ${type}}}`',
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
    '>{{Upload new revision}}<',
    "title: '{{Image}}",
    'showMessage("{{New image revision has been uploaded.}}"',
    'showError("{{Upload of a new image revision failed: }}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/inherited_attribute_list.js'
translation = [
    'title: "{{Inherited attributes}}"',
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
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/owned_attribute_list.js'
translation = [
    'title: "{{Owned attributes}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/ribbon_widgets/promoted_attributes.js'
translation = [
    'title: "{{Promoted attributes}}"',
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
    "title: '{{Search parameters}}",
    'showMessage("{{Search note has been saved into }}"',
    "showMessage('{{Actions have been executed.}}'",
    '    logError(`{{Unknown search option ${searchOptionName}}}`',
    """    logError(`{{Parsing of attribute: '${actionAttr.value}' failed with error: ${e.message}}}`""",
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

file_path = 'src/public/app/widgets/search_actions/abstract_search_action.js'
translation = [
    '{{Remove this search action}}',
    '    logError({{`Failed rendering search action: ${JSON.stringify(this.attribute.dto)} with error: ${e.message} ${e.stack}`}}',
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

file_path = 'src/public/app/widgets/side_pane_toggles.js'
translation = [
    'title="{{Hide sidebar}}"',
    'title="{{Show sidebar}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/similar_notes.js'
translation = [
    r'''{{`${similarNotes.length} similar note${similarNotes.length === 1 ? '': "s"}`}}''',
    'title="{{This list contains notes which might be similar to the current note based on textual similarity of note title, its labels and relations.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/standard_top_widget.js'
translation = [
    '    {{New note}}',
    '    {{Jump to note}}',
    '    {{Search}}',
    '    {{Recent changes}}',
    '    {{Enter protected session}}',
    '    {{Leave protected session}}',
    'title="{{Enter protected session to be able to find and view protected notes}}"',
    'title="{{Leave protected session so that protected notes are not accessible any more.}}"',
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

file_path = 'src/public/app/widgets/type_property_widgets/file_properties.js'
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

file_path = 'src/public/app/widgets/type_property_widgets/image_properties.js'
translation = [
    '>{{Original file name:}}<',
    '>{{File type:}}<',
    '>{{File size:}}<',
    '>{{Download}}<',
    '>{{Open}}<',
    '>{{Copy to clipboard}}<',
    '>{{Upload new revision}}<',
    "title: '{{Image}}",
    'showMessage("{{New image revision has been uploaded.}}"',
    'showError("{{Upload of a new image revision failed:}} "',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_property_widgets/inherited_attribute_list.js'
translation = [
    '`{{Inherited attrs}} (',
    '"{{No inherited attributes.}}"',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_property_widgets/note_properties.js'
translation = [
    "title: '{{Info}}",
    '{{This note was originally taken from}}: <',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_property_widgets/owned_attribute_list.js'
translation = [
    '`{{Owned attrs}} (',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_property_widgets/promoted_attributes.js'
translation = [
    '`{{Promoted attrs}} (',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_property_widgets/search_definition.js'
translation = [
    '>{{Add search option:}}<',
    '>{{enter}}<',
    "title: '{{Search}}",
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
    '        {{Search & Execute actions}}',
    '        {{Search}}',
    'title="{{Fast search option disables full text search of note contents which might speed up searching in large databases.}}"',
    'title="{{Archived notes are by default excluded from search results, with this option they will be included.}}"',
    'title="{{Limit number of results}}"',
    'title="{{Debug will print extra debugging information into the console to aid in debugging complex queries}}"',
    '{{Actions have been executed.}}',

    '    logError({{`Unknown search option ${searchOptionName}`}}',
    """    logError({{`Parsing of attribute: '${actionAttr.value}' failed with error: ${e.message}`}}""",
    """    logError(`{{No action class for '${actionDef.name}' found.}}`""",

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
    ", '{{New tab}}')",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/book.js'
translation = [
    """{{This note of type Book doesn't have any child notes so there's nothing to display. See <a href="https://github.com/zadam/trilium/wiki/Book-note">wiki</a> for details.}}""",
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/deleted.js'
translation = [
    '{{This note has been deleted.}}',
]
replace_in_file(file_path, translation)

file_path = 'src/public/app/widgets/type_widgets/editable_code.js'
translation = [
    'title="{{Open Trilium API docs}}"',
    'showMessage("{{SQL Console note has been saved into }}"',
    '{{Execute}} <k',
    '{{Save to note}}</k',
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

file_path = 'src/public/app/widgets/type_widgets/file.js'
translation = [
    '{{File preview is not available for this file format.}}',
]

replace_in_file(file_path, translation)
file_path = 'src/public/app/widgets/type_widgets/image.js'
translation = [
    'showMessage("{{Image copied to the clipboard}}"',
    '    toastService.showAndLogError("{{Could not copy the image to clipboard.}}"',
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
    'confirmDialog.confirm("{{Are you sure you want to remove the relation?}}"',
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
]
replace_in_file(file_path, translation, TARGET_PATH)

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
    translation.extend(["=== '{{inheritable}}'", ])

replace_in_file(file_path, translation)

file_path = 'src/public/app/services/attribute_renderer.js'
translation = [
]
if TRANSLATE_NOTE_TAG:
    translation.extend([' `({{inheritable}})` ', ])

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
    'description: "{{Copy selected text without formatting}}"',
]
replace_in_file(file_path, translation, TARGET_PATH)

file_path = 'src/routes/api/date_notes.js'
translation = [
    "title: '{{Search:}} '",
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
]
replace_in_file(file_path, translation)
replace_in_file(file_path, translation, TARGET_PATH)

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
        content = content.replace('ref: excalidrawRef,', 'ref: excalidrawRef,\n                    langCode: "zh-CN",')
    with open(file_full_path, 'w') as f:
        f.write(content)

# 应用补丁
# apply patch
os.chdir(BASE_PATH)
os.system('npm run webpack')

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

# excalidraw 自定义字体
# excalidraw custom font
src_path = f'{script_path}/font/muyao-shouxie.ttf'
dest_path = f'{PATCH_FOLDER}/node_modules/@excalidraw/excalidraw/dist/excalidraw-assets/Virgil.woff2'
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

if missing_files:
    print('missing_files!')
    for x in missing_files:
        print(x)

print('finished!')
