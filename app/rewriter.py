

import re

def extract_sentences(text):
    # Basic sentence splitter using punctuation
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if len(s.split()) > 3]


def rewrite_sentences(client, resume_text):
    sentences = extract_sentences(resume_text)
    prompt = f"""
You are a professional resume editor and career advisor in {2025}. Your job is to review the resume below and:

1. Rewrite only the sentences that are:
   - Vague
   - Passive
   - Lacking measurable impact
   - Too generic or redundant

2. Provide general writing recommendations based on the patterns you observed in the rewrites.

💡 Rules:
- DO NOT rewrite sentences that are already strong, specific, and well-written.
- Preserve the original tone and structure where possible.
- Use strong action verbs and quantify results where applicable.
- DO NOT invent any information not clearly present in the original.
- Only output rewrites where a meaningful improvement is possible.
- Do not use bold headings
- Avoid the use of emojis

✍️ Format your response like this:

Rewrite Pairs:
Original: [original sentence]  
Improved: [rewritten sentence]  

...

General Recommendations:
- [tip 1]
- [tip 2]
- ...
- [tip N]

Sentences:
{chr(10).join(sentences)}
    """
    response = client.responses.create(
        model="gpt-4.1-nano",  # GPT-4.1-nano / turbo
        input = prompt,
        temperature=0.3  # Lower temperature = more factual, less creative
    )

    return response.output_text
