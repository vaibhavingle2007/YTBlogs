from typing import Dict, Any, List, Tuple, Optional
from backend.llm_service import LLMService

class BlogGenerator:
    """
    Generates blog content by creating prompts for an LLM 
    and using the LLMService to get the generated content.
    """
    
    def __init__(self):
        """Initializes the BlogGenerator and the LLMService."""
        try:
            self.llm_service = LLMService()
            self.llm_enabled = True
        except ValueError:
            self.llm_service = None
            self.llm_enabled = False
            print("⚠️ WARNING: LLM Service not initialized. NEBIUS_API_KEY may be missing.")

        self.templates = {
            "article": self._create_article_prompt,
            "tutorial": self._create_tutorial_prompt,
            "review": self._create_review_prompt,
            "summary": self._create_summary_prompt
        }
    
    def generate_blog(self, video_data: Dict[str, Any], template: str, transcript: Optional[str]) -> str:
        """Generate blog content based on template and video data using an LLM."""
        if not self.llm_enabled:
            return "## LLM Service Not Available\n\nPlease ensure your `NEBIUS_API_KEY` is correctly set in your `.env` file and restart the server."

        if template not in self.templates:
            raise ValueError(f"Unknown template: {template}")
        
        system_prompt, user_prompt = self.templates[template](video_data, transcript)
        
        return self.llm_service.generate_content(system_prompt, user_prompt)

    def _get_content_source(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Determines the best content source (transcript or description) to use for the prompt."""
        description = video_data.get('description', '')
        if transcript and len(transcript.strip()) > 100:
            return transcript, "video transcript"
        return description, "video description"

    # --------------------------------------------------------
    # ARTICLE PROMPT (Refined)
    # --------------------------------------------------------
    def _create_article_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        system_prompt = (
            "You are an expert blog writer who turns video content into rich, well-structured, SEO-friendly articles. "
            "Write with clarity, depth, and flow. Use Markdown formatting, including headings, subheadings, bold, "
            "lists, and examples when useful. Maintain an informative but engaging tone throughout."
        )
        
        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
Please generate a comprehensive blog article in Markdown format based on the video information below.

**Video Title:** {video_data.get('title')}
**Channel:** {video_data.get('channel_name')}
**Content Source (from {source_type}):**
---
{content_source[:4000]}
---

**Instructions:**
1. Create a compelling headline inspired by the video title.
2. Write an introduction that explains the topic, why it matters, and what readers will learn.
3. Identify the 3–6 main themes or takeaways from the content.
4. For each theme, create a detailed section with a descriptive subheading. Expand clearly with explanations, insights, and helpful context.
5. Add examples or clarifications when they improve reader understanding.
6. Conclude with a meaningful summary and final insight.
7. Produce a polished Markdown article with no meta commentary.
"""
        return system_prompt, user_prompt

    # --------------------------------------------------------
    # TUTORIAL PROMPT (Refined)
    # --------------------------------------------------------
    def _create_tutorial_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        system_prompt = (
            "You are a technical writer who creates clear, structured, deeply detailed tutorials from video content. "
            "Write step-by-step, with explanations that make each step easy to follow. Use Markdown formatting, "
            "numbered steps, subheadings, and code blocks when helpful."
        )
        
        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
Please generate a detailed step-by-step tutorial in Markdown format using the information below.

**Video Title:** {video_data.get('title')}
**Channel:** {video_data.get('channel_name')}
**Content Source (from {source_type}):**
---
{content_source[:4000]}
---

**Instructions:**
1. Create an action-focused headline.
2. Write an overview explaining what the tutorial teaches and the final result.
3. Add prerequisites if necessary (tools, software, knowledge).
4. Break the process into a sequence of detailed, logical steps.
5. For each step:
   - Add a subheading.
   - Explain what to do and why it matters.
   - Add warnings, notes, or tips where useful.
   - Include code blocks if applicable.
6. Conclude with what the user accomplished and optional next steps.
7. Output the whole tutorial in clean Markdown.
"""
        return system_prompt, user_prompt

    # --------------------------------------------------------
    # REVIEW PROMPT (Refined)
    # --------------------------------------------------------
    def _create_review_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        system_prompt = (
            "You are a professional reviewer who writes balanced, in-depth evaluations of products, tools, or content "
            "explained in videos. Your reviews should feel structured, fair, and insightful. Use Markdown formatting, "
            "with sections like Overview, Pros, Cons, Performance, and Final Verdict."
        )

        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
Please generate a detailed and balanced review in Markdown format based on the video content.

**Video Title:** {video_data.get('title')}
**Channel:** {video_data.get('channel_name')}
**Content Source (from {source_type}):**
---
{content_source[:4000]}
---

**Instructions:**
1. Create a strong review headline.
2. Begin with an overview of the product/topic and what it aims to achieve.
3. Provide a deeper analysis covering features, performance, usability, strengths, and weaknesses.
4. Add the following sections:
   - **Pros:** meaningful positive points in bullets.
   - **Cons:** realistic drawbacks, not generic filler.
5. Include a **Final Verdict** summarizing who it is for and whether it is worth considering.
6. Add a star rating out of 5 with a one-line justification.
7. Output the result as a clean Markdown review.
"""
        return system_prompt, user_prompt

    # --------------------------------------------------------
    # SUMMARY PROMPT (Refined)
    # --------------------------------------------------------
    def _create_summary_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        system_prompt = (
            "You are an efficient summarizer who extracts the most important insights from video content. "
            "Write summaries that are short but meaningful, structured, and easy to skim. Use Markdown headings and bullet points."
        )

        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
Please produce a clear and slightly detailed summary in Markdown format.

**Video Title:** {video_data.get('title')}
**Channel:** {video_data.get('channel_name')}
**Content Source (from {source_type}):**
---
{content_source[:4000]}
---

**Instructions:**
1. Use the video title as the main heading.
2. Write a one-paragraph overview explaining the main idea and purpose of the video.
3. Provide a bulleted list of the 6–10 most important insights, lessons, or events.
4. Keep the language simple, clear, and direct.
5. Deliver the final result as a complete Markdown summary.
"""
        return system_prompt, user_prompt
