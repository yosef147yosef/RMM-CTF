from flask import Flask, request, Response, render_template_string
import os

app = Flask(__name__)

REFERER = "www.SuperSecretSite.IRAN.gov.com"
PASSWORD_SUM = 57
HTML_FILE_PATH = '//home//yosef147yosef//mysite//form.html'
JPG_FILE_PATH = '//home//yosef147yosef//mysite//secret.jpg'

def read_file(file_path):
    """Read file content."""
    with open(file_path, 'r') as file:
        return file.read()

def read_binary_file(file_path):
    """Read binary file content."""
    with open(file_path, 'rb') as file:
        return file.read()

def check_referer():
    referer = request.headers.get('Referer', '')
    if REFERER not in referer:
        return False, "Sorry, you didnt got from our secure site. Only Iranin with very high clearnes can insert to that site, and only from this site this site can be reached"
    return True, ""

def check_language():
    accept_language = request.headers.get('Accept-Language', '')
    if 'fa' not in accept_language:
        return False, "Good try Mosad. But I see you didnt learn our langue yet!!"
    return True, ""
def send_jpg():
    try:
        jpg_data = read_binary_file(JPG_FILE_PATH)
    except FileNotFoundError:
        return "Error: JPG file not found", 500

    response = Response(jpg_data, mimetype='image/jpeg')
    response.headers['Content-Disposition'] = 'attachment; filename="secret.jpg"'
    return response
@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        referer_check, referer_message = check_referer()
        if  not referer_check:
            return referer_message, 403

        language_check, language_message = check_language()
        if  not language_check:
            return language_message, 403

        html_content = read_file(HTML_FILE_PATH)
        return render_template_string(html_content)

    elif request.method == 'POST':
        referer_check, referer_message = check_referer()
        if  not referer_check:
            return referer_message, 403

        language_check, language_message = check_language()
        if not  language_check:
            return language_message, 403

        password = request.form.get('password', '').strip()
        if password=="Pointy":
            return send_jpg()
        else:
            return "Access denied: Invalid password", 403




