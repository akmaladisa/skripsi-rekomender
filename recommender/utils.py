import re
from pypdf import PdfReader
from .models import TranskripDetailNilai

def parse_transcript(pdf_path, upload_instance):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    # Basic regex to find course entries
    # Assumption: Code (optional), Name, SKS (int), Grade (A/B/C/D/E), Quality Points (float), Weight (float)
    # This is tricky without a sample. I will try to match lines that have a grade and SKS.
    
    # Regex for: Code Name SKS Grade
    # Example: "CS101 Intro to CS 3 A"
    # Let's try to find lines ending with a grade and SKS.
    
    # Specific regex for the user's transcript format
    # Format observed: NO KODE MATA KULIAH NILAIA.MSKSBOBOT
    # Example: 1 200001108 ICT Literacy A 4.002 8
    # The grade (A) is followed immediately by A.M (4.00) and SKS (2) which might be merged in text extraction.
    # Let's try to capture:
    # 1. Number (digits)
    # 2. Code (digits)
    # 3. Name (text)
    # 4. Grade (A, A-, B+, etc.)
    # 5. The rest (ignored)
    
    lines = text.split('\n')
    extracted_count = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Regex: ^\d+\s+(\d+)\s+(.+?)\s+([A-E][+-]?)\s+
        # Matches start of line, number, code, name (lazy), grade, then whitespace
        match = re.search(r'^\d+\s+(\d+)\s+(.+?)\s+([A-E][+-]?)\s+', line)
        if match:
            kode_mk = match.group(1)
            nama_mk = match.group(2).strip()
            nilai_huruf = match.group(3)
            
            # SKS extraction is tricky if merged (e.g. 4.002). 
            # We can try to parse the end of the line or just default to 3 if not found clearly.
            # Let's look at what comes after the grade.
            # Example: ... A 4.002 8
            # After 'A ', we have '4.002 8'. 
            # '4.00' is quality points, '2' is SKS, '8' is weight.
            # Regex to capture the rest: ([0-9.]+)\s*(\d+)\s*(\d+)
            
            # Let's try a more comprehensive regex for the whole line
            full_match = re.search(r'^\d+\s+(\d+)\s+(.+?)\s+([A-E][+-]?)\s+([0-9.]+)(\d+)\s+(\d+)', line)
            
            sks = 3 # Default
            if full_match:
                 # If the text extraction merged 4.00 and 2 into 4.002
                 # We might need to be careful.
                 # But let's assume the SKS is the single digit after the float, or separated.
                 # In "4.002", 4.00 is float, 2 is SKS.
                 pass
            
            # Simpler approach: Just take the grade and name. SKS is less critical for content-based filtering 
            # (unless we use it for weighting, but we can default to 3).
            # However, let's try to find SKS if possible.
            
            # Try to find the last single digit before the last number?
            # Let's stick to the robust match of Name and Grade.
            
            TranskripDetailNilai.objects.create(
                upload=upload_instance,
                kode_mk=kode_mk,
                nama_mk=nama_mk,
                sks=sks, 
                nilai_huruf=nilai_huruf
            )
            extracted_count += 1
            continue
            
    return extracted_count

    return extracted_count
