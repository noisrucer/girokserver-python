def read_and_format_html(
    replacements: dict[str, str],
    html_path: str = "src/infrastructure/external_services/email_service/verification_template.html",
):
    f = open(html_path)
    content = f.read()
    for target, val in replacements.items():
        content = content.replace(target, val)
    f.close()
    return content
