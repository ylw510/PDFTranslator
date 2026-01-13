import pdfplumber
from typing import List, Dict

class PDFParser:
    """PDF文件解析器"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pages = []

    def extract_text(self) -> Dict[str, any]:
        """
        提取PDF文本内容
        返回包含页面文本和元数据的字典
        """
        text_content = []

        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                total_pages = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        text_content.append({
                            'page': page_num,
                            'text': text.strip(),
                            'bbox': page.bbox
                        })

                return {
                    'total_pages': total_pages,
                    'pages': text_content,
                    'full_text': '\n\n'.join([p['text'] for p in text_content])
                }
        except Exception as e:
            raise Exception(f"PDF解析失败: {str(e)}")

    def extract_by_pages(self, page_numbers: List[int] = None) -> str:
        """
        提取指定页面的文本
        """
        result = self.extract_text()

        if page_numbers:
            pages = [p for p in result['pages'] if p['page'] in page_numbers]
            return '\n\n'.join([p['text'] for p in pages])

        return result['full_text']
