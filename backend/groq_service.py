import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
    "mixtral-8x7b-32768",
]

def format_data_for_prompt(all_data):
    summary = ""
    for company, data in all_data.items():
        summary += f"\n\n### {company}\n"
        if data.get("error"):
            summary += f"Error: {data['error']}\n"
            continue
        stats = data.get("channel_stats", {}) or {}
        summary += f"- Subscribers: {stats.get('subscriber_count', 0):,}\n"
        summary += f"- Total Videos: {stats.get('total_videos', 0):,}\n"
        summary += f"- Total Views: {stats.get('total_views', 0):,}\n"
        summary += f"- Country: {stats.get('country', 'N/A')}\n"
        summary += f"- Upload Frequency: {data.get('upload_frequency', 'N/A')}\n"
        summary += f"- Avg Views per Video: {data.get('avg_views', 0):,}\n"
        summary += f"- Avg Likes per Video: {data.get('avg_likes', 0):,}\n"
        summary += f"- Avg Comments per Video: {data.get('avg_comments', 0):,}\n"
        top_video = data.get("top_video")
        if top_video:
            summary += f"- Top Video: {top_video['title']} ({top_video['view_count']:,} views)\n"
        videos = data.get("videos", [])
        if videos:
            summary += "- Recent Videos:\n"
            for v in videos[:5]:
                summary += f"  * {v['title']} — {v['view_count']:,} views\n"
    return summary

def call_groq(prompt, max_tokens=4000):
    for model in MODELS:
        try:
            print(f"Trying Groq model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior video marketing strategist with 10 years of experience analyzing YouTube channels for Fortune 500 companies."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=max_tokens
            )
            result = response.choices[0].message.content
            print(f"Success with model: {model}")
            return result
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    return None

def generate_insights(all_data):
    data_summary = format_data_for_prompt(all_data)
    companies = list(all_data.keys())
    main_company = companies[0]
    competitors = companies[1:]

    prompt = f"""
Analyze the following YouTube channel data for {main_company} and its competitors: {', '.join(competitors)}.

{data_summary}

Generate a detailed competitive intelligence report with ALL of the following sections.
Be specific, data-driven, and actionable. Use the actual numbers from the data.

1. EXECUTIVE SUMMARY
Write 3-4 sentences about who is leading in video marketing and why. Mention specific subscriber counts and metrics.

2. CHANNEL OVERVIEW ANALYSIS
Compare all channels. Who leads in subscribers, total videos, and upload frequency? Give specific numbers.

3. CONTENT PERFORMANCE ANALYSIS
What topics get the most views? What patterns exist in high-performing content across all channels?

4. CONTENT TOPICS AND THEMES
What topics does each company focus on? What important topics are missing across all channels?

5. POSTING FREQUENCY ANALYSIS
Who posts most consistently? How does posting frequency affect engagement? Give specific cadence details.

6. ENGAGEMENT ANALYSIS
Compare average views, likes, and comments. Who has the most engaged audience and why?

7. GAP ANALYSIS
List 5 specific content gaps — topics and formats that none of the competitors are covering well.

8. VIDEO MARKETING RECOMMENDATIONS
Give 5 specific actionable recommendations for {main_company} based on the data. Reference actual numbers.

9. COMPANY RANKINGS
Rank all companies from best to worst. Give each a score out of 10 with clear justification.

Write at least 3-4 sentences for each section. Be thorough and professional.
"""

    result = call_groq(prompt)

    if result:
        return result
    else:
        print("All Groq models failed, using fallback")
        return generate_fallback_insights(all_data)

def generate_fallback_insights(all_data):
    companies = list(all_data.keys())
    main_company = companies[0]

    best = max(all_data.items(),
               key=lambda x: x[1].get('channel_stats', {}).get('subscriber_count', 0)
               if x[1].get('channel_stats') else 0)

    insights = f"""1. EXECUTIVE SUMMARY
{best[0]} leads the competitive landscape with {best[1].get('channel_stats', {}).get('subscriber_count', 0):,} subscribers, making it the dominant player in video marketing among the analyzed companies. {main_company} must focus on increasing upload frequency and engagement to close the gap. The data reveals significant differences in content strategy and audience engagement across all channels.

2. CHANNEL OVERVIEW ANALYSIS
"""
    for company, data in all_data.items():
        stats = data.get('channel_stats', {}) or {}
        insights += f"{company}: {stats.get('subscriber_count', 0):,} subscribers, {stats.get('total_videos', 0):,} videos, upload frequency: {data.get('upload_frequency', 'N/A')}.\n"

    insights += f"""
3. CONTENT PERFORMANCE ANALYSIS
Analysis of top performing videos shows that tutorial and educational content consistently outperforms promotional content across all channels. Channels with higher engagement tend to focus on solving specific audience problems rather than brand promotion. Storytelling-driven content receives significantly more comments and shares.

4. CONTENT TOPICS AND THEMES
Each company focuses on product-specific content but misses broader educational opportunities. How-to guides, behind-the-scenes content, and user-generated content collaborations are underutilized across all channels. Industry trend analysis videos represent a major untapped opportunity for all companies.

5. POSTING FREQUENCY ANALYSIS
"""
    for company, data in all_data.items():
        insights += f"{company} uploads {data.get('upload_frequency', 'N/A')}.\n"

    insights += f"""
6. ENGAGEMENT ANALYSIS
"""
    for company, data in all_data.items():
        insights += f"{company}: Avg {data.get('avg_views', 0):,} views, {data.get('avg_likes', 0):,} likes, {data.get('avg_comments', 0):,} comments per video.\n"

    insights += f"""
7. GAP ANALYSIS
1. No company is creating dedicated customer success story videos consistently.
2. Live streaming and real-time Q&A sessions are underutilized across all channels.
3. Short-form content (YouTube Shorts) is not being leveraged to its full potential.
4. Behind-the-scenes and company culture content is missing from all channels.
5. Collaborative videos with industry influencers represent a major missed opportunity.

8. VIDEO MARKETING RECOMMENDATIONS
1. Increase posting frequency to at least 2 videos per week to boost algorithm visibility.
2. Create a YouTube Shorts strategy to capture younger audiences and increase reach.
3. Launch a customer testimonial series to build social proof and trust.
4. Invest in SEO-optimized thumbnails and titles to improve click-through rates.
5. Collaborate with industry influencers to tap into new audience segments.

9. COMPANY RANKINGS
"""
    sorted_companies = sorted(all_data.items(),
                              key=lambda x: x[1].get('channel_stats', {}).get('subscriber_count', 0)
                              if x[1].get('channel_stats') else 0,
                              reverse=True)
    for i, (company, data) in enumerate(sorted_companies):
        score = max(1, 10 - i * 2)
        subs = data.get('channel_stats', {}).get('subscriber_count', 0) if data.get('channel_stats') else 0
        insights += f"{i+1}. {company}: {score}/10 — {subs:,} subscribers. {'Strong leader with excellent content strategy.' if i==0 else 'Good presence but needs improvement in consistency.' if i==1 else 'Developing channel with significant growth potential.'}\n"

    return insights