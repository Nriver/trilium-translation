import os
import re
import shutil

from settings import BASE_FOLDER, PATCH_FOLDER, TRANSLATOR_URL, LANG
from translations import translation_dict

script_path = os.path.dirname(os.path.abspath(__file__))

BASE_PATH = f'{BASE_FOLDER}trilium-src/'
CLIENT_PATH = f'{BASE_FOLDER}TriliumNext Notes-linux-x64/'
PATCH_FOLDER = PATCH_FOLDER

TARGET_PATH = f'{CLIENT_PATH}resources/app/'
os.chdir(BASE_PATH)

TRANSLATOR_LABEL = translation_dict['translator']

if not os.path.exists(f'{TARGET_PATH}src/public/'):
    os.system(f'cd "{CLIENT_PATH}resources" && asar extract app.asar ./app/')

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


file_path = 'src/public/app/services/attribute_parser.js'
translation = [
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

if os.path.exists('/usr/share/nvm/init-nvm.sh'):
    print('nvm managed environment')
    os.system('which node')
    os.system('source /usr/share/nvm/init-nvm.sh && proxychains npm install')
    os.system('source /usr/share/nvm/init-nvm.sh && which npm && proxychains npm run webpack')
else:
    os.system('which webpack')
    os.system('npm install')
    os.system('npm run webpack')

# 把编译好的文件复制到客户端里
# copy compiled file to the client
os.system(f'''cp -r "{BASE_PATH}src/public/app-dist" "{CLIENT_PATH}resources/app/src/public/"''')

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
shutil.copytree(f'{CLIENT_PATH}resources/app/dist/src/views/', f'{PATCH_FOLDER}/src/views/')
shutil.copytree(f'{CLIENT_PATH}resources/app/dist/src/services/', f'{PATCH_FOLDER}/src/services/')
shutil.copytree(f'{CLIENT_PATH}resources/app/dist/src/routes/', f'{PATCH_FOLDER}/src/routes/')

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
    shutil.rmtree(os.path.expanduser('~/.config/TriliumNext Notes/'))
except:
    pass

print('finished!')
