def generate_email_content(news):
    """Generate dynamic email content with news summaries."""
    content = "Here are today's AI news updates:\n\n"
    for article in news:
        content += f"{article['title']}\n{article['summary_en']}\nLink: {article['link']}\n\n"
    return content