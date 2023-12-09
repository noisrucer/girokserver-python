import aiohttp


class EmailManager:
    def __init__(self, mailgun_api_key: str, mailgun_domain: str):
        self.mailgun_api_key = mailgun_api_key
        self.mailgun_domain = mailgun_domain

    async def send_email(self, recipient: str, subject: str, content: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.mailgun_domain,
                auth=aiohttp.BasicAuth("api", self.mailgun_api_key),
                data={"from": "girok <admin@girok.org>", "to": [recipient], "subject": subject, "html": content},
            ) as resp:
                if resp.status != 200:
                    print("Email Error")

    def read_and_format_html(
        self,
        replacements: dict[str, str],
        html_path: str = "girok/core/email/verification_template.html",
    ) -> str:
        f = open(html_path)
        content = f.read()
        for target, val in replacements.items():
            content = content.replace(target, val)
        f.close()
        return content
