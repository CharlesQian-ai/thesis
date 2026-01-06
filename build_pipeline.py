import os
import sys
import time
import subprocess

# 尝试导入 Playwright
try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

# 导入我们的工具脚本
import generate_printable
import pdf_to_ppt

def step_1_gen_html():
    print("\n" + "="*40)
    print("[1/3] Regenerating HTML (print.html)...")
    print("="*40)
    generate_printable.generate_print_html()

def step_2_gen_pdf(html_path, pdf_path):
    print("\n" + "="*40)
    print("[2/3] Converting HTML to PDF...")
    print("="*40)
    
    # 确保旧的 PDF 被删除，避免误判
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except:
            pass

    success = False
    
    # 尝试自动生成
    if HAS_PLAYWRIGHT:
        print("🚀 Attempting automatic generation using Playwright...")
        try:
            with sync_playwright() as p:
                # 尝试启动浏览器，如果未安装可能会失败
                browser = p.chromium.launch()
                page = browser.new_page()
                
                # 转换为 file URL
                file_url = f"file:///{html_path.replace(os.sep, '/')}"
                print(f"Loading: {file_url}")
                
                page.goto(file_url)
                page.wait_for_load_state("networkidle")
                
                # 导出 PDF (与打印设置一致)
                page.pdf(
                    path=pdf_path, 
                    width="1280px", 
                    height="720px", 
                    print_background=True,
                    margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}
                )
                browser.close()
            
            if os.path.exists(pdf_path):
                print("✅ Auto-generation successful!")
                success = True
        except Exception as e:
            print(f"❌ Auto-generation failed: {e}")
            print("Falling back to manual mode...")
            success = False
    else:
        print("ℹ️  Playwright not installed/configured. Using manual mode.")

    # 如果自动失败，进入手动模式
    if not success:
        print("\n" + "!"*50)
        print("⚠️  MANUAL INTERVENTION REQUIRED")
        print("!"*50)
        print("Automatic PDF generation is not available. Please do the following:")
        print(f"1. Open this file in your browser:\n   {html_path}")
        print("2. Press Ctrl+P (Print)")
        print("3. Settings:")
        print("   - Printer: 'Save as PDF' (另存为 PDF)")
        print("   - Layout: Landscape (横向)")
        print("   - Margins: None (无)")
        print("   - Background graphics: Checked (背景图形: 勾选)")
        print(f"4. SAVE THE FILE AS:\n   {pdf_path}")
        print("-" * 50)
        
        # 循环检测文件是否存在
        while not os.path.exists(pdf_path):
            user_input = input(f"Waiting for {os.path.basename(pdf_path)}... (Press Enter after saving, or 'q' to quit): ")
            if user_input.lower() == 'q':
                print("Operation cancelled.")
                return False
            
            if os.path.exists(pdf_path):
                print("✅ File detected!")
                break
            else:
                print("❌ File still not found. Please save it to the exact path above.")
    
    return True

def step_3_gen_ppt(pdf_path, ppt_path):
    print("\n" + "="*40)
    print("[3/3] Converting PDF to PPTX...")
    print("="*40)
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Source PDF not found: {pdf_path}")
        return

    pdf_to_ppt.convert_pdf_to_ppt(pdf_path, ppt_path)

if __name__ == "__main__":
    # 路径配置
    BASE_DIR = r"d:\Projects\开题答辩PPT"
    
    # 输入/输出文件
    HTML_FILE = os.path.join(BASE_DIR, "proposal", "thesis_proposal_ppt", "print.html")
    # 直接生成到最终目录
    FINAL_PDF = os.path.join(BASE_DIR, "proposal", "docs", "Final_Presentation.pdf")
    FINAL_PPT = os.path.join(BASE_DIR, "proposal", "docs", "Final_Presentation.pptx")
    
    print("🎬 Starting PPT Build Pipeline...")
    print(f"Targets: \n  - {FINAL_PDF}\n  - {FINAL_PPT}")
    
    # 1. 生成 HTML
    step_1_gen_html()
    
    # 2. 生成 PDF
    if step_2_gen_pdf(HTML_FILE, FINAL_PDF):
        # 3. 生成 PPT
        step_3_gen_ppt(FINAL_PDF, FINAL_PPT)
        
        print("\n" + "★"*40)
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"📂 Output Files:\n  - {FINAL_PDF}\n  - {FINAL_PPT}")
        print("★"*40)
    else:
        print("\n❌ Pipeline aborted.")
