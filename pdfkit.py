import pdfkit

# configure pdfkit to point to our installation of wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# download Wikipedia main page as a PDF file
pdfkit.from_url("https://en.wikipedia.org/wiki/Main_Page", "sample_url_pdf.pdf", configuration=config)

s = """<h1><strong>Sample PDF file from HTML</strong></h1>
       <br></br>
       <p>First line...</p>
       <p>Second line...</p>
       <p>Third line...</p>"""

pdfkit.from_string(s, output_path = "new_file.pdf", configuration = config)