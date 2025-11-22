from PyPDF2 import PdfReader


def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def draw_multiline_text(pdf, text, x, y, max_width):
    if not text or not text.strip():
        return y
    
    lines, words, current_line = [], text.split(" "), ""
    for word in words:
        if not word.strip():  # Skip empty words
            continue
            
        test_line = f"{current_line} {word}".strip()
        
        # Handle very long words that exceed max_width
        if pdf.stringWidth(word, "Helvetica", 12) > max_width:
            if current_line:
                lines.append(current_line)
                current_line = ""
            # Truncate the word if it's too long
            lines.append(word[:50] + "..." if len(word) > 50 else word)
        elif pdf.stringWidth(test_line, "Helvetica", 12) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    for line in lines:
        if line.strip():  # Only draw non-empty lines
            pdf.drawString(x, y, line)
            y -= 14
    
    return y
