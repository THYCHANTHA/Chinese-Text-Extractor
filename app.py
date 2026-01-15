# from flask import Flask, request, render_template_string
# import requests
# from bs4 import BeautifulSoup
# import re

# app = Flask(__name__)

# # HTML template in English
# HTML_TEMPLATE = '''
# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Chinese Text Extractor</title>
#     <style>
#         body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
#         h1, h2 { text-align: center; }
#         input[type="text"] { width: 100%; padding: 10px; font-size: 16px; }
#         input[type="submit"] { padding: 10px 20px; font-size: 16px; margin-top: 10px; }
#         pre { background: #f4f4f4; padding: 20px; border-radius: 8px; white-space: pre-wrap; }
#     </style>
# </head>
# <body>
#     <h1>Extract Chinese Text from Audio</h1>
#     <p>Enter a URL (e.g., a CCTV video page) to extract the main Chinese text content.</p>
    
#     <form method="post">
#         <label for="url">URL:</label><br>
#         <input type="text" id="url" name="url" placeholder="https://tv.cctv.com/..." size="50" required><br><br>
#         <input type="submit" value="Extract Text">
#     </form>
    
#     {% if text %}
#     <h2>Extracted Chinese Text:</h2>
#     <pre>{{ text }}</pre>
#     {% endif %}
    
#     {% if text and '错误' in text %}
#     <p style="color: red;">An error occurred. Please check the URL and try again.</p>
#     {% endif %}
# </body>
# </html>
# '''

# @app.route('/', methods=['GET', 'POST'])
# def extract_text():
#     extracted_text = ''
#     if request.method == 'POST':
#         url = request.form['url'].strip()
#         try:
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'} 
#             response = requests.get(url, headers=headers, timeout=15)
#             response.raise_for_status()
#             response.encoding = 'utf-8'

#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Extract text from common content tags
#             all_text = []
#             for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'div']):
#                 text = tag.get_text(strip=True)
#                 if text and re.search(r'[\u4e00-\u9fff]', text):  # Contains Chinese characters
#                     all_text.append(text)

#             # Remove duplicates while preserving order
#             seen = set()
#             unique_text = []
#             for line in all_text:
#                 if line not in seen:
#                     seen.add(line)
#                     unique_text.append(line)

#             extracted_text = '\n\n'.join(unique_text)

#             if not extracted_text:
#                 extracted_text = "No Chinese text found on this page."

#         except requests.exceptions.RequestException as e:
#             extracted_text = f"Error fetching the page: {str(e)}"
#         except Exception as e:
#             extracted_text = f"Error processing the page: {str(e)}"

#     return render_template_string(HTML_TEMPLATE, text=extracted_text)

# if __name__ == '__main__':
#     app.run(debug=True)

# work but no style

# from flask import Flask, request, render_template_string, send_file
# import requests
# from bs4 import BeautifulSoup
# import re
# import io
# from PIL import Image
# from pyzbar.pyzbar import decode

# app = Flask(__name__)

# # HTML template in English with QR upload, copy, and download features
# HTML_TEMPLATE = '''
# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Chinese Text Extractor</title>
#     <style>
#         body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
#         h1, h2 { text-align: center; }
#         input[type="text"], input[type="file"] { width: 100%; padding: 10px; font-size: 16px; margin-bottom: 10px; }
#         input[type="submit"] { padding: 10px 20px; font-size: 16px; margin-top: 10px; }
#         textarea { width: 100%; height: 300px; padding: 10px; font-size: 14px; background: #f4f4f4; border: 1px solid #ccc; border-radius: 8px; }
#         .actions { margin-top: 10px; text-align: center; }
#         .actions button, .actions a { padding: 10px 20px; margin: 0 10px; font-size: 16px; text-decoration: none; color: white; background: #007bff; border: none; border-radius: 5px; cursor: pointer; }
#         .actions button:hover, .actions a:hover { background: #0056b3; }
#         .error { color: red; text-align: center; }
#     </style>
# </head>
# <body>
#     <h1>Extract Chinese Text from Video</h1>
#     <p>Enter a URL or upload a QR code image containing a video URL to extract the Chinese text.</p>
    
#     <form method="post" enctype="multipart/form-data">
#         <label for="url">URL (optional):</label><br>
#         <input type="text" id="url" name="url" placeholder="https://tv.cctv.com/..." size="50"><br><br>
        
#         <label for="qr_file">Upload QR Code Image:</label><br>
#         <input type="file" id="qr_file" name="qr_file" accept="image/*"><br><br>
        
#         <input type="submit" value="Extract Text">
#     </form>
    
#     {% if text %}
#     <h2>Extracted Chinese Text:</h2>
#     <textarea id="extractedText">{{ text }}</textarea>
#     <div class="actions">
#         <button onclick="copyText()">Copy Text</button>
#         <a href="/download" download="extracted_text.txt">Download Text</a>
#     </div>
#     <script>
#         function copyText() {
#             var textarea = document.getElementById('extractedText');
#             textarea.select();
#             document.execCommand('copy');
#             alert('Text copied to clipboard!');
#         }
#     </script>
#     {% endif %}
    
#     {% if error %}
#     <p class="error">{{ error }}</p>
#     {% endif %}
# </body>
# </html>
# '''

# # Global variable to store extracted text for download (simple, for demo)
# extracted_text_global = ''

# @app.route('/', methods=['GET', 'POST'])
# def extract_text():
#     global extracted_text_global
#     extracted_text = ''
#     error_msg = ''
#     url = ''

#     if request.method == 'POST':
#         try:
#             # Get URL from form or from QR code
#             url = request.form.get('url', '').strip()
            
#             if not url and 'qr_file' in request.files:
#                 qr_file = request.files['qr_file']
#                 if qr_file.filename:
#                     # Read image and decode QR
#                     img = Image.open(qr_file.stream)
#                     decoded_objects = decode(img)
#                     if decoded_objects:
#                         url = decoded_objects[0].data.decode('utf-8')
#                     else:
#                         raise ValueError("No QR code found in the uploaded image.")
#                 else:
#                     raise ValueError("No QR code file uploaded.")

#             if not url:
#                 raise ValueError("Please provide a URL or upload a QR code.")

#             # Fetch the page
#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
#             response = requests.get(url, headers=headers, timeout=15)
#             response.raise_for_status()
#             response.encoding = 'utf-8'

#             # Parse HTML
#             soup = BeautifulSoup(response.text, 'html.parser')

#             # Extract text from common content tags
#             all_text = []
#             for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'div']):
#                 text = tag.get_text(strip=True)
#                 if text and re.search(r'[\u4e00-\u9fff]', text):  # Contains Chinese characters
#                     all_text.append(text)

#             # Remove duplicates while preserving order
#             seen = set()
#             unique_text = []
#             for line in all_text:
#                 if line not in seen:
#                     seen.add(line)
#                     unique_text.append(line)

#             extracted_text = '\n\n'.join(unique_text)

#             if not extracted_text:
#                 extracted_text = "No Chinese text found on this page."

#             # Store for download
#             extracted_text_global = extracted_text

#         except requests.exceptions.RequestException as e:
#             error_msg = f"Error fetching the page: {str(e)}"
#         except ValueError as ve:
#             error_msg = str(ve)
#         except Exception as e:
#             error_msg = f"Error processing: {str(e)}"

#     return render_template_string(HTML_TEMPLATE, text=extracted_text, error=error_msg)

# @app.route('/download')
# def download_text():
#     global extracted_text_global
#     if not extracted_text_global:
#         return "No text to download.", 400
    
#     # Create in-memory file
#     buffer = io.BytesIO()
#     buffer.write(extracted_text_global.encode('utf-8'))
#     buffer.seek(0)
    
#     return send_file(buffer, as_attachment=True, download_name='extracted_text.txt', mimetype='text/plain')

# if __name__ == '__main__':
#     app.run(debug=True)

# Moderm UI

# from flask import Flask, request, render_template_string, send_file
# import requests
# from bs4 import BeautifulSoup
# import re
# import io
# from PIL import Image
# from pyzbar.pyzbar import decode

# app = Flask(__name__)

# # Modern UI HTML + Tailwind-inspired CSS (no external CDN needed)
# HTML_TEMPLATE = '''
# <!DOCTYPE html>
# <html lang="en" class="scroll-smooth">
# <head>
#     <meta charset="UTF-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
#     <title>Chinese Text Extractor</title>
#     <script src="https://cdn.tailwindcss.com"></script>
#     <script>
#         tailwind.config = {
#             theme: {
#                 extend: {
#                     colors: {
#                         primary: '#2563eb',
#                         primarydark: '#1d4ed8',
#                     }
#                 }
#             }
#         }
#     </script>
# </head>
# <body class="bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen font-sans antialiased">

#     <div class="container mx-auto px-4 py-10 max-w-4xl">
        
#         <!-- Header -->
#         <div class="text-center mb-10">
#             <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-3">
#                 Chinese Text Extractor
#             </h1>
#             <p class="text-lg text-gray-600">
#                 This website aims to extract Chinese textual content from videos obtained via website links or QR codes.
#             </p>
#         </div>

#         <!-- Main Card -->
#         <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
#             <div class="p-6 md:p-10">
#                 <form method="post" enctype="multipart/form-data" class="space-y-8">
#                     <!-- URL Input -->
#                     <div>
#                         <label for="url" class="block text-sm font-medium text-gray-700 mb-2">
#                             Website URL
#                         </label>
#                         <input 
#                             type="text" 
#                             id="url" 
#                             name="url" 
#                             placeholder="https://tv.cctv.com/..." 
#                             class="w-full px-5 py-4 rounded-xl border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all duration-200"
#                         >
#                     </div>

#                     <!-- QR Code Upload -->
#                     <div>
#                         <label for="qr_file" class="block text-sm font-medium text-gray-700 mb-2">
#                             Or upload QR Code containing the link
#                         </label>
#                         <div class="flex items-center justify-center w-full">
#                             <label class="flex flex-col w-full h-40 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-primary/50 transition-colors duration-200 bg-gray-50 hover:bg-gray-100">
#                                 <div class="flex flex-col items-center justify-center pt-10">
#                                     <svg class="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
#                                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
#                                     </svg>
#                                     <p class="text-sm text-gray-500">
#                                         <span class="font-semibold text-primary">Click to upload</span> or drag & drop
#                                     </p>
#                                     <p class="text-xs text-gray-400 mt-1">PNG, JPG, max 5MB</p>
#                                 </div>
#                                 <input type="file" id="qr_file" name="qr_file" accept="image/*" class="hidden" />
#                             </label>
#                         </div>
#                     </div>

#                     <!-- Submit Button -->
#                     <button type="submit"
#                             class="w-full py-4 px-6 bg-primary hover:bg-primarydark text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2">
#                         Extract Chinese Text
#                     </button>
#                 </form>
#             </div>

#             {% if text %}
#             <!-- Result Section -->
#             <div class="border-t border-gray-100 bg-gray-50 px-6 py-8 md:px-10">
#                 <div class="flex items-center justify-between mb-4">
#                     <h2 class="text-2xl font-bold text-gray-800">Extracted Text</h2>
#                     <div class="flex gap-3">
#                         <button onclick="copyText()" 
#                                 class="px-5 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 transition">
#                             📋 Copy
#                         </button>
#                         <a href="/download" download="chinese_text.txt"
#                            class="px-5 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 transition">
#                             ⬇ Download
#                         </a>
#                     </div>
#                 </div>
                
#                 <textarea id="extractedText"
#                           readonly
#                           class="w-full h-96 p-5 rounded-xl bg-white border border-gray-200 text-gray-800 font-mono text-sm resize-none shadow-inner focus:outline-none">
# {{ text }}
#                 </textarea>
#             </div>
#             {% endif %}

#             {% if error %}
#             <div class="border-t border-gray-100 bg-red-50 px-6 py-8 md:px-10">
#                 <p class="text-red-700 text-center font-medium">{{ error }}</p>
#             </div>
#             {% endif %}
#         </div>

#         <!-- Footer note -->
#         <p class="text-center text-sm text-gray-500 mt-10">
#             Powered by Flask • Works best with CCTV, news & video summary pages
#         </p>
#     </div>

#     <script>
#         function copyText() {
#             const textarea = document.getElementById('extractedText');
#             textarea.select();
#             textarea.setSelectionRange(0, 99999);
#             document.execCommand('copy');
#             alert('Text copied to clipboard! ✓');
#         }
#     </script>
# </body>
# </html>
# '''

# # Same backend logic as before
# extracted_text_global = ''

# @app.route('/', methods=['GET', 'POST'])
# def extract_text():
#     global extracted_text_global
#     extracted_text = ''
#     error_msg = ''
#     url = ''

#     if request.method == 'POST':
#         try:
#             url = request.form.get('url', '').strip()
            
#             if not url and 'qr_file' in request.files:
#                 qr_file = request.files['qr_file']
#                 if qr_file.filename:
#                     img = Image.open(qr_file.stream)
#                     decoded_objects = decode(img)
#                     if decoded_objects:
#                         url = decoded_objects[0].data.decode('utf-8')
#                     else:
#                         raise ValueError("No QR code detected in the image.")
#                 else:
#                     raise ValueError("No QR code file selected.")

#             if not url:
#                 raise ValueError("Please provide a URL or upload a QR code image.")

#             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#             response = requests.get(url, headers=headers, timeout=15)
#             response.raise_for_status()
#             response.encoding = 'utf-8'

#             soup = BeautifulSoup(response.text, 'html.parser')
#             all_text = []
#             for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'div']):
#                 text = tag.get_text(strip=True)
#                 if text and re.search(r'[\u4e00-\u9fff]', text):
#                     all_text.append(text)

#             seen = set()
#             unique_text = [x for x in all_text if not (x in seen or seen.add(x))]
#             extracted_text = '\n\n'.join(unique_text)

#             if not extracted_text:
#                 extracted_text = "No Chinese text found on this page."

#             extracted_text_global = extracted_text

#         except Exception as e:
#             error_msg = f"Error: {str(e)}"

#     return render_template_string(HTML_TEMPLATE, text=extracted_text, error=error_msg)

# @app.route('/download')
# def download_text():
#     global extracted_text_global
#     if not extracted_text_global:
#         return "No text available.", 400
    
#     buffer = io.BytesIO()
#     buffer.write(extracted_text_global.encode('utf-8'))
#     buffer.seek(0)
    
#     return send_file(buffer, as_attachment=True, download_name='chinese_text.txt', mimetype='text/plain')

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template_string, send_file
import requests
from bs4 import BeautifulSoup
import re
import io
from PIL import Image
from pyzbar.pyzbar import decode
import base64

app = Flask(__name__)

# Modern UI - inputs persist after extraction, clear only on demand
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Chinese Text Extractor</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#2563eb',
                        primarydark: '#1d4ed8',
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen font-sans antialiased">

    <div class="container mx-auto px-4 py-10 max-w-4xl">
        
        <div class="text-center mb-10">
            <h1 class="text-4xl md:text-5xl font-bold text-gray-800 mb-3">
                Chinese Text Extractor
            </h1>
            <p class="text-lg text-gray-600">
                This website aims to extract Chinese textual content from videos obtained via website links or QR codes.
            </p>
        </div>

        <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
            <div class="p-6 md:p-10">
                <form id="mainForm" method="post" enctype="multipart/form-data" class="space-y-8">
                    <!-- URL Input -->
                    <div>
                        <label for="url" class="block text-sm font-medium text-gray-700 mb-2">
                            Website URL
                        </label>
                        <input type="text" id="url" name="url" placeholder="https://tv.cctv.com/..." 
                               value="{{ url if url else '' }}"
                               class="w-full px-5 py-4 rounded-xl border border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all duration-200">
                    </div>

                    <!-- QR Code Upload with Preview -->
                    <div>
                        <label for="qr_file" class="block text-sm font-medium text-gray-700 mb-2">
                            Or upload QR Code
                        </label>
                        <div class="flex items-center justify-center w-full">
                            <label id="dropzone" class="flex flex-col w-full h-64 border-2 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-primary/50 transition-colors duration-200 bg-gray-50 hover:bg-gray-100 relative overflow-hidden">
                                <div id="previewContainer" class="{% if has_preview %}hidden{% else %}flex flex-col items-center justify-center{% endif %} absolute inset-0">
                                    <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                                    </svg>
                                    <p class="text-sm text-gray-500">
                                        <span class="font-semibold text-primary">Click to upload</span> or drag & drop
                                    </p>
                                    <p class="text-xs text-gray-400 mt-2">PNG, JPG, max 5MB</p>
                                </div>
                                <img id="preview" src="{{ preview_src if preview_src else '' }}" 
                                     class="{% if preview_src %}block w-full h-full object-contain{% else %}hidden{% endif %}" 
                                     alt="QR Code Preview">
                                <input type="file" id="qr_file" name="qr_file" accept="image/*" class="hidden" />
                            </label>
                        </div>
                    </div>

                    <!-- Submit Button -->
                    <button type="submit"
                            class="w-full py-4 px-6 bg-primary hover:bg-primarydark text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:ring-offset-2">
                        Extract Chinese Text
                    </button>
                </form>
            </div>

            {% if text or error %}
            <div class="border-t border-gray-100 {% if error %}bg-red-50{% else %}bg-gray-50{% endif %} px-6 py-8 md:px-10">
                {% if text %}
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-2xl font-bold text-gray-800">Extracted Text</h2>
                    <div class="flex gap-3 flex-wrap">
                        <button onclick="copyText()" 
                                class="px-5 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 transition">
                            📋 Copy
                        </button>
                        <a href="/download" download="chinese_text.txt"
                           class="px-5 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 text-gray-700 transition">
                            ⬇ Download
                        </a>
                        <button onclick="clearAll()" 
                                class="px-5 py-2 bg-white border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition">
                            Clear All
                        </button>
                    </div>
                </div>
                <textarea id="extractedText" readonly class="w-full h-96 p-5 rounded-xl bg-white border border-gray-200 text-gray-800 font-mono text-sm resize-none shadow-inner focus:outline-none">{{ text }}</textarea>
                {% endif %}
                {% if error %}
                <p class="text-red-700 text-center font-medium">{{ error }}</p>
                {% endif %}
            </div>
            {% endif %}
        </div>

        <p class="text-center text-sm text-gray-500 mt-10">
            Powered by InsightCode Academy
        </p>
    </div>

    <script>
        // Show uploaded image preview (client-side)
        document.getElementById('qr_file').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const preview = document.getElementById('preview');
                    const container = document.getElementById('previewContainer');
                    preview.src = event.target.result;
                    preview.classList.remove('hidden');
                    preview.classList.add('block');
                    container.classList.add('hidden');
                }
                reader.readAsDataURL(file);
            }
        });

        function copyText() {
            const textarea = document.getElementById('extractedText');
            textarea.select();
            document.execCommand('copy');
            alert('Text copied to clipboard! ✓');
        }

        function clearAll() {
            document.getElementById('mainForm').reset();
            document.getElementById('preview').classList.add('hidden');
            document.getElementById('preview').src = '';
            document.getElementById('previewContainer').classList.remove('hidden');
            // Force reload to remove result area
            window.location.href = window.location.pathname;
        }
    </script>
</body>
</html>
'''

# For storing last extracted text (simple global approach)
extracted_text_global = ''

@app.route('/', methods=['GET', 'POST'])
def extract_text():
    global extracted_text_global
    
    extracted_text = ''
    error_msg = ''
    input_url = ''
    preview_src = ''  # base64 data url for preview persistence

    if request.method == 'POST':
        input_url = request.form.get('url', '').strip()

        try:
            url = input_url
            
            # Handle QR upload (this request)
            if 'qr_file' in request.files and request.files['qr_file'].filename:
                qr_file = request.files['qr_file']
                # Reset stream position so we can read it twice
                qr_file.stream.seek(0)
                img = Image.open(qr_file.stream)
                
                decoded_objects = decode(img)
                if decoded_objects:
                    url = decoded_objects[0].data.decode('utf-8')
                    
                    # Create preview (base64) - now works because we imported base64
                    qr_file.stream.seek(0)  # Reset again
                    preview_bytes = qr_file.stream.read()
                    preview_src = f"data:image/jpeg;base64,{base64.b64encode(preview_bytes).decode('utf-8')}"
                else:
                    raise ValueError("No QR code detected in the image.")

            if not url:
                raise ValueError("Please provide a URL or upload a QR code image.")

            # Fetch and extract text (same as before)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            all_text = []
            for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'div']):
                text = tag.get_text(strip=True)
                if text and re.search(r'[\u4e00-\u9fff]', text):
                    all_text.append(text)

            seen = set()
            unique_text = [x for x in all_text if not (x in seen or seen.add(x))]
            extracted_text = '\n\n'.join(unique_text)

            if not extracted_text:
                extracted_text = "No Chinese text found on this page."

            # Store for download
            extracted_text_global = extracted_text

        except Exception as e:
            error_msg = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, 
                                 text=extracted_text, 
                                 error=error_msg,
                                 url=input_url,
                                 preview_src=preview_src,
                                 has_preview=bool(preview_src))

@app.route('/download')
def download_text():
    # You can keep global or use session - for simplicity we use global here
    # In real app better use session/flash
    global extracted_text_global
    if not extracted_text_global:
        return "No text available.", 400
    
    buffer = io.BytesIO()
    buffer.write(extracted_text_global.encode('utf-8'))
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name='chinese_text.txt', mimetype='text/plain')

# For download to work, we still need to store the last extracted text
extracted_text_global = ''

# Update global after successful extraction
# (add this inside the try block after successful extraction)
# extracted_text_global = extracted_text

if __name__ == '__main__':
    app.run(debug=True)