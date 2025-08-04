calibration_guide = """
SCORING CALIBRATION GUIDE - Use these benchmarks for accurate differentiation:

EXPERIENCE MATCH (0-30 points):
- 28-30: Exceeds role requirements, clear career progression, directly relevant experience
- 24-27: Strong alignment, meets 80%+ requirements, relevant industry background  
- 20-23: Good match, meets 60-79% requirements, some transferable experience
- 15-19: Partial relevance, meets 40-59% requirements, significant experience gaps
- 10-14: Limited alignment, meets 20-39% requirements, mostly irrelevant experience
- 0-9: Poor fit, meets <20% requirements, completely unrelated background

SKILLS & KEYWORDS (0-25 points):
- 23-25: 90%+ required skills present, perfect keyword density, natural integration
- 20-22: 75-89% skills match, strong keyword coverage, good ATS optimization
- 17-19: 60-74% skills match, adequate keyword presence, minor gaps
- 13-16: 40-59% skills match, poor keyword optimization, missing critical skills
- 8-12: 20-39% skills match, minimal relevant keywords, major skill gaps
- 0-7: <20% skills match, no relevant keywords, completely misaligned

ACHIEVEMENTS & IMPACT (0-25 points):
- 23-25: Multiple quantified achievements with clear ROI/business impact
- 20-22: Several quantified results, demonstrates measurable value
- 17-19: Some quantified accomplishments, shows results-oriented approach
- 13-16: Basic achievements, limited quantification, unclear impact
- 8-12: Vague accomplishments, no metrics, minimal value demonstration
- 0-7: Only job duties listed, no achievements or measurable impact

PRESENTATION & ATS (0-20 points):
- 18-20: Flawless formatting, perfect ATS compatibility, exceptional readability
- 15-17: Professional presentation, good ATS optimization, minor formatting issues
- 12-14: Adequate structure, some ATS concerns, acceptable readability
- 9-11: Poor formatting, significant ATS problems, hard to scan
- 5-8: Major presentation issues, ATS-incompatible, unprofessional appearance
- 0-4: Severely flawed formatting, completely ATS-unfriendly, unreadable

ROLE-SPECIFIC ANALYSIS FRAMEWORK:
Before scoring, determine role category and apply appropriate lens:
- TECHNICAL ROLES: Emphasize technical skills, project complexity, problem-solving
- LEADERSHIP ROLES: Focus on team management, strategic thinking, business impact
- CREATIVE ROLES: Highlight portfolio, creative problem-solving, innovation
- SALES/BUSINESS: Prioritize metrics, revenue impact, relationship building
- ENTRY-LEVEL: Focus on potential, education, internships, relevant coursework

COMPETITIVE BENCHMARKING:
"Among 100 qualified applicants for this specific role, where would this resume rank?"
- Top 5% (Elite): 90-100 points - Would definitely get interviews at top companies
- Top 15% (Excellent): 80-89 points - Strong candidate, likely to advance
- Top 35% (Good): 70-79 points - Competitive, decent interview chances
- Average (50%): 60-69 points - Needs improvement to stand out
- Below Average: 50-59 points - Significant gaps, unlikely to advance
- Poor: 0-49 points - Major overhaul needed

CRITICAL SCORING PRINCIPLES:
1. Be ruthless with accuracy - avoid "safe" middle scores
2. Consider role seniority level in expectations
3. Factor in current job market competitiveness
4. Differentiate between similar candidates based on subtle quality indicators
5. Score based on likelihood of getting past initial screening AND interview performance
"""


def build_prompt(resume_text, job_input):
    # Analyze job input complexity and type
    word_count = len(job_input.split())
    is_full_description = word_count > 15

    # Extract role level and type
    role_level = determine_role_level(job_input)
    role_category = determine_role_category(job_input)

    if is_full_description:
        job_context = f"""
JOB ANALYSIS:
The user is applying to this specific job posting:
{job_input}

ANALYSIS REQUIREMENTS:
1. Extract and prioritize the top 10 must-have requirements from this job description
2. Identify industry-specific terminology and required certifications
3. Note any specific company culture indicators or unique requirements
4. Determine competitive level (entry/mid/senior/executive) from requirements
5. Focus evaluation on EXACT keyword matching and requirement fulfillment
"""
    else:
        job_context = f"""
ROLE TARGET ANALYSIS: 
The user is targeting a '{job_input}' position.

INDUSTRY RESEARCH REQUIRED:
1. Apply current market standards for {job_input} roles in 2025
2. Consider typical requirements for {role_level} level positions
3. Use industry benchmarks for {role_category} roles
4. Factor in current job market competitiveness for this role type
5. Reference standard qualifications, skills, and experience expectations
"""

    prompt = f"""
You are an expert ATS systems analyst and senior recruiter with 15+ years of experience hiring for roles across industries. You have intimate knowledge of what separates top 10% candidates from average ones.

{job_context}

{calibration_guide}

RESUME TO ANALYZE:
{resume_text}

MANDATORY ANALYSIS FRAMEWORK:

**STEP 1: JOB-RESUME FIT ANALYSIS**
Before scoring, complete this critical analysis:
- What are the 5 most critical requirements for this role?
- How well does this resume address each critical requirement?
- What would make someone an IDEAL candidate for this specific position?
- Where does this candidate fall short of the ideal?

**STEP 2: COMPETITIVE POSITIONING**
- In the current job market, how competitive is this role?
- What caliber of candidates typically apply?
- What would make a resume stand out from 100+ similar applications?

**STEP 3: SCORING WITH EVIDENCE**
Use the calibration guide to score each component. For each score, provide:
- Specific evidence from the resume
- Direct comparison to job requirements
- Clear reasoning for why this score vs. higher/lower

REQUIRED OUTPUT FORMAT:

## 1. **RELEVANCE SCORE: ___/100**

### Detailed Scoring Breakdown:
**Experience Match: ___/30**
- Evidence: [Quote specific experience sections]
- Gap Analysis: [What's missing for this specific role]
- Competitive Positioning: [How this compares to typical candidates]

**Skills & Keywords: ___/25**
- Critical Skills Present: [List with resume evidence]
- Missing Keywords: [Specific to this job posting/role]
- ATS Optimization Level: [Technical assessment]

**Achievements & Impact: ___/25**
- Quantified Results: [Quote specific metrics]
- Business Impact: [Relevance to target role]
- Achievement Quality: [Compared to role expectations]

**Presentation & ATS: ___/20**
- Formatting Assessment: [Specific issues/strengths]
- ATS Compatibility: [Technical evaluation]
- Professional Presentation: [Readability and structure]

**MATHEMATICAL VERIFICATION:** [Sum of components] = [Relevance Score]

## 2. **COMPETITIVE ANALYSIS**

### Market Positioning:
- **Candidate Tier:** [Top 5% / Top 15% / Top 35% / Average / Below Average / Poor]
- **Interview Likelihood:** [High/Medium/Low with reasoning]
- **Key Differentiators:** [What makes this candidate unique]
- **Fatal Flaws:** [Deal-breakers that would eliminate consideration]

## 3. **ROLE-SPECIFIC STRENGTHS**
[Minimum 3 strengths with direct job relevance]
- **Strength 1:** [Quote + why it matters for THIS role]
- **Strength 2:** [Quote + specific relevance]
- **Strength 3:** [Quote + competitive advantage]

## 4. **CRITICAL GAPS & RED FLAGS**
[Prioritized by impact on hiring decision]
- **Critical Gap 1:** [Specific missing requirement + impact]
- **Critical Gap 2:** [Missing skill/experience + why it matters]
- **Red Flag:** [Any concerning elements]

## 5. **STRATEGIC IMPROVEMENT ROADMAP**

### High-Impact Changes (Implement First):
1. **[Specific Change]:** 
   - Before: [Current resume language]
   - After: [Improved version]
   - Impact: [Why this matters]

### Missing Keywords Integration:
- **Must-Add Keywords:** [5-7 role-specific terms]
- **Integration Strategy:** [How to naturally incorporate]
- **Remove/Replace:** [Outdated or weak terms]

### Format & ATS Optimization:
- **Technical Fixes:** [Specific formatting issues]
- **Section Improvements:** [Restructuring recommendations]

## 6. **90+ SCORE BENCHMARK**

### Profile of Ideal Candidate:
- **Experience:** [Specific years and type needed]
- **Skills:** [Technical and soft skills for excellence]
- **Achievements:** [Types and scale of accomplishments]
- **Background:** [Education, certifications, company types]

### Gap to Excellence:
[Specific steps to reach top-tier candidate status]

ANALYSIS QUALITY REQUIREMENTS:
✅ Every score backed by specific resume evidence
✅ Job requirements directly addressed
✅ Competitive market context included
✅ Actionable, specific improvement suggestions
✅ Mathematical accuracy in scoring
✅ Honest assessment without false encouragement
✅ ATS and human recruiter perspectives balanced

Remember: Your goal is to provide brutally honest, actionable feedback that helps this candidate compete effectively for this specific role in today's competitive market.
"""

    return prompt


def determine_role_level(job_input):
    # Determine experience level from job input
    job_lower = job_input.lower()
    if any(term in job_lower for term in ['senior', 'lead', 'principal', 'staff', 'architect']):
        return 'senior'
    elif any(term in job_lower for term in ['junior', 'entry', 'associate', 'graduate', 'intern']):
        return 'entry'
    elif any(term in job_lower for term in ['director', 'vp', 'head of', 'manager', 'chief']):
        return 'executive'
    else:
        return 'mid'


def determine_role_category(job_input):
    # Determine role category for specialized analysis
    job_lower = job_input.lower()
    if any(term in job_lower for term in ['engineer', 'developer', 'programmer', 'technical', 'software', 'data']):
        return 'technical'
    elif any(term in job_lower for term in ['manager', 'director', 'lead', 'head', 'supervisor']):
        return 'leadership'
    elif any(term in job_lower for term in ['sales', 'business development', 'account', 'revenue']):
        return 'sales'
    elif any(term in job_lower for term in ['designer', 'creative', 'marketing', 'content', 'brand']):
        return 'creative'
    else:
        return 'general'

def analyze_resume(client, text, job):
    prompt = build_prompt(text, job)

    response = client.responses.create(
        model="gpt-4.1-nano",
        input = prompt,
        temperature=0.3  # Lower temperature = more factual, less creative
    )

    return response.output_text


#-------------------------------------------------------------
import re

def parse_resume_analysis(text: str) -> dict:
    def extract_score(label):
        # More flexible pattern that handles different formats
        pattern = rf"{re.escape(label)}:\s*(\d+)/\d+"
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None

    total_score = re.search(r"RELEVANCE SCORE:\s*(\d+(?:\.\d+)?)/100", text)
    total_score = extract_score("RELEVANCE SCORE")
    return {
        "total_score": total_score,
        "breakdown": {
            "Experience Match": extract_score("Experience Match"),
            "Skills & Keywords": extract_score("Skills & Keywords"),
            "Achievements & Impact": extract_score("Achievements & Impact"),
            "Presentation & ATS": extract_score("Presentation & ATS"),
        }
    }