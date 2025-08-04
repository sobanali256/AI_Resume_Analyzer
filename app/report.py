# Separating Suggestions and Recommendations

def parse_gpt_response(response_text):
    rewrite_pairs = []
    tips = []

    lines = response_text.strip().splitlines()
    current_pair = {}
    in_recommendations = False

    for line in lines:
        if line.strip().lower().startswith("general recommendations"):
            in_recommendations = True
            continue

        if not in_recommendations:
            if line.lower().startswith("original:"):
                current_pair['original'] = line.split("Original:", 1)[1].strip()
            elif line.lower().startswith("improved:"):
                current_pair['improved'] = line.split("Improved:", 1)[1].strip()
                if current_pair.get('original'):
                    rewrite_pairs.append(current_pair)
                    current_pair = {}
        else:
            # Clean up bullet points or dashes
            clean_tip = line.strip().lstrip("-• ").strip()
            if clean_tip:
                tips.append(clean_tip)

    return rewrite_pairs, tips

#-------------------------------------------------------------------------------------------------

def generate_vagueness_report(rewritten_output, resume_text=None):
    import re

    rewrite_pairs, recommendations = parse_gpt_response(rewritten_output)

    # Estimate total number of resume points
    if resume_text:
        bullet_points = re.findall(r'^\s*[-•*]\s+', resume_text, flags=re.MULTILINE)
        sentences = re.findall(r'[.!?]\s+', resume_text)
        total_phrases = max(len(bullet_points), len(sentences), len(rewrite_pairs))
    else:
        total_phrases = len(rewrite_pairs)

    vague_count = len(rewrite_pairs)

    report = ["Resume Vagueness & Clarity Report", "-" * 40, "", "Summary:",
              f"• Total Phrases Analyzed: {total_phrases}", f"• Vague or Generic Phrases Rewritten: {vague_count}", "",
              "Rewrite Suggestions:"]

    for idx, pair in enumerate(rewrite_pairs, 1):
        report.append(f"{idx}.\"{pair['original']}\"")
        report.append(f" Suggestion: \"{pair['improved']}\"")
        report.append("")

    report.append("Tailored Writing Tips:")
    for tip in recommendations:
        report.append(f"• {tip}")

    return "\n".join(report)

