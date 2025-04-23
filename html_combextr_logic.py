# File: html_logic.py

from bs4 import BeautifulSoup

def combine_html_css_js(html_content, css_content, js_content):
    """
    Combines separate HTML, CSS, and JavaScript code into a single HTML string.
    (Code from the previous answer - Keep it identical)
    """
    if not html_content:
        html_content = "<!DOCTYPE html>\n<html>\n<head>\n<title>Combined Page</title>\n</head>\n<body>\n</body>\n</html>"

    soup = BeautifulSoup(html_content, 'html.parser')

    # --- Embed CSS ---
    if css_content:
        head = soup.find('head')
        if not head:
            html_tag = soup.find('html')
            if html_tag:
                head = soup.new_tag('head')
                html_tag.insert(0, head)
                if not head.find('title'):
                     title_tag = soup.new_tag('title')
                     title_tag.string = "Combined Page"
                     head.append(title_tag)
            else:
                 print("Warning: Could not find <html> tag to insert <head>.")
                 style_tag = soup.new_tag('style')
                 style_tag.string = css_content
                 soup.insert(0, style_tag)

        if head:
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            head.append(style_tag)

    # --- Embed JavaScript ---
    if js_content:
        body = soup.find('body')
        if not body:
            html_tag = soup.find('html')
            if html_tag:
                body = soup.new_tag('body')
                html_tag.append(body)
            else:
                print("Warning: Could not find <html> tag to insert <body>.")
                script_tag = soup.new_tag('script')
                script_tag.string = js_content
                soup.append(script_tag)

        if body:
            script_tag = soup.new_tag('script')
            script_tag.string = js_content
            body.append(script_tag)

    return soup.prettify()

def extract_html_css_js(combined_html):
    """
    Extracts HTML structure, CSS, and JavaScript from a single HTML string.
    (Code from the previous answer - Keep it identical)
    """
    if not combined_html:
        return ("", "", "")

    soup = BeautifulSoup(combined_html, 'html.parser')
    extracted_css = []
    extracted_js = []

    # --- Extract CSS from <style> tags within <head> ---
    head = soup.find('head')
    if head:
        style_tags = head.find_all('style')
        for style_tag in style_tags:
            if style_tag.string:
                 extracted_css.append(style_tag.string.strip())
            style_tag.decompose()

    # --- Extract JavaScript from <script> tags (anywhere) ---
    script_tags = soup.find_all('script')
    for script_tag in script_tags:
        if not script_tag.has_attr('src'):
             if script_tag.string:
                 extracted_js.append(script_tag.string.strip())
        script_tag.decompose()

    html_structure = soup.prettify()
    final_css = "\n\n".join(extracted_css)
    final_js = "\n\n".join(extracted_js)

    return html_structure, final_css, final_js