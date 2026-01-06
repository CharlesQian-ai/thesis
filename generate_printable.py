import os
import re

# 配置路径
BASE_DIR = r"d:\Projects\开题答辩PPT\proposal\thesis_proposal_ppt"
SLIDES_DIR = os.path.join(BASE_DIR, "slides")
OUTPUT_FILE = os.path.join(BASE_DIR, "print.html")

# 幻灯片顺序
SLIDE_FILES = [
    "slide1.html",
    "slide2.html",
    "slide3.html",
    "slide4.html",
    "slide_challenge.html",
    "slide5.html",
    "slide6.html",
    "slide_experiment.html",
    "slide7.html",
    "slide8.html",
    "slide9.html",
    "slide10.html",
    "slide11.html"
]

def scope_css(css_content, scope_id):
    """
    极简 CSS Scoper：给选择器加上 #scope_id 前缀
    """
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    new_css = []
    i = 0
    length = len(css_content)
    while i < length:
        if css_content[i:].startswith('@media'):
            balance = 0
            found_start = False
            j = i
            while j < length:
                if css_content[j] == '{':
                    balance += 1
                    found_start = True
                elif css_content[j] == '}':
                    balance -= 1
                    if found_start and balance == 0:
                        j += 1
                        break
                j += 1
            i = j 
        else:
            new_css.append(css_content[i])
            i += 1
    
    css_clean = "".join(new_css)
    scoped_rules = []
    css_clean = css_clean.replace('\r\n', '\n')
    buffer = ""
    in_selector = True
    
    for char in css_clean:
        if char == '{':
            selectors = buffer.strip().split(',')
            scoped_selectors = []
            for sel in selectors:
                sel = sel.strip()
                if not sel: continue
                if 'body' in sel:
                    sel = sel.replace('body', f'#{scope_id}')
                else:
                    sel = f'#{scope_id} {sel}'
                scoped_selectors.append(sel)
            
            scoped_rules.append(", ".join(scoped_selectors))
            scoped_rules.append(" {")
            buffer = ""
            in_selector = False
        elif char == '}':
            scoped_rules.append(buffer)
            scoped_rules.append("}\n")
            buffer = ""
            in_selector = True
        else:
            buffer += char
            
    return "".join(scoped_rules)

def process_content(html_content, slide_id):
    """提取并处理内容"""
    html_content = re.sub(r'src=["\']images/', 'src="slides/images/', html_content)
    html_content = re.sub(r'url\([\'"]?images/', 'url(\'slides/images/', html_content)
    
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    
    style_content = style_match.group(1) if style_match else ""
    body_content = body_match.group(1) if body_match else ""
    
    scope_name = f"slide-{slide_id}"
    scoped_style = scope_css(style_content, scope_name)
    
    return scoped_style, body_content

def generate_print_html():
    combined_html = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>开题答辩PPT - 打印版 (无边框)</title>
    <style>
        /* 全局重置 */
        * { box-sizing: border-box; }
        
        html, body { 
            margin: 0; 
            padding: 0; 
            background: white; 
            width: 100%;
        }
        
        /* 预览时的容器 */
        .print-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background: #f0f0f0;
        }

        /* 每一页幻灯片 */
        .slide-page {
            width: 1280px;
            height: 720px;
            background: white;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            
            /* 强制分页 */
            page-break-after: always;
            break-after: page;
        }

        /* 打印专用样式 */
        @media print {
            /* 
               关键设置：定义页面尺寸为幻灯片原尺寸 (1280px x 720px)
               这会让 "另存为 PDF" 直接生成该尺寸的文档，从而没有白边。
            */
            @page {
                size: 1280px 720px;
                margin: 0;
            }

            .print-container {
                padding: 0;
                background: white;
                display: block;
            }
            
            body {
                background: white;
                margin: 0;
            }

            .slide-page {
                margin: 0;
                box-shadow: none;
                border: none;
                width: 1280px;
                height: 720px;
                
                page-break-inside: avoid;
                page-break-after: always;
                break-after: page;

                /* 不再需要缩放，因为页面尺寸已经匹配内容 */
                zoom: 1; 
                
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            
            .slide-page:last-child {
                page-break-after: auto;
                break-after: auto;
            }
        }
    </style>
</head>
<body>
    <div class="print-container">
"""

    for i, filename in enumerate(SLIDE_FILES):
        file_path = os.path.join(SLIDES_DIR, filename)
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        slide_id = i + 1
        style, body = process_content(content, slide_id)
        
        slide_html = f"""
        <!-- Slide {slide_id}: {filename} -->
        <div class="slide-page" id="slide-{slide_id}">
            <style>
{style}
            </style>
            {body}
        </div>
"""
        combined_html += slide_html

    combined_html += """
    </div>
</body>
</html>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(combined_html)
    
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_print_html()
