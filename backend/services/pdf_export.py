import io
import logging

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_INSTALLED = True
    WEASYPRINT_ERROR = ""
except (ImportError, OSError) as e:
    WEASYPRINT_INSTALLED = False
    WEASYPRINT_ERROR = str(e)

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    if not WEASYPRINT_INSTALLED:
        raise ImportError(
            f"WeasyPrint is not fully configured: {WEASYPRINT_ERROR}. "
            "On Windows, WeasyPrint requires the GTK+ libraries to be installed. "
            "Please download the GTK3 installer for Windows or install MSYS2 (see https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)."
        )
        
    documents = []
    
    # Render all 3 HTML strings to WeasyPrint Document objects
    for name, html_str in html_docs.items():
        doc = HTML(string=html_str).render()
        documents.append(doc)
    
    # Merge them into the first document
    first_doc = documents[0]
    for other_doc in documents[1:]:
        for page in other_doc.pages:
            first_doc.pages.append(page)
            
    # Write combined PDF bytes
    pdf_bytes = first_doc.write_pdf()
    return pdf_bytes
