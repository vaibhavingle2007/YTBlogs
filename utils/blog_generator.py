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
        
        # Create the system and user prompts using the appropriate method
        system_prompt, user_prompt = self.templates[template](video_data, transcript)
        
        # Call the LLM service to generate the blog content
        return self.llm_service.generate_content(system_prompt, user_prompt)

    def _get_content_source(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Determines the best content source (transcript or description) to use for the prompt."""
        description = video_data.get('description', '')
        # Use transcript if it's substantial, otherwise fall back to description.
        if transcript and len(transcript.strip()) > 100:
            return transcript, "video transcript"
        return description, "video description"

    def _create_article_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Creates the system and user prompts for a standard article."""
        system_prompt = (
            "You are an expert blog writer specializing in creating engaging, well-structured articles from video content. "
            "Your tone should be informative yet accessible. You must use Markdown for formatting, including headings, "
            "subheadings, bold text for emphasis, and bullet points or numbered lists where appropriate."
        )
        
        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
        Please generate a high-quality blog article in Markdown format based on the following video information.

        **Video Title:** {video_data.get('title')}
        **Channel:** {video_data.get('channel_name')}
        **Content Source (from {source_type}):**
        ---
        {content_source[:4000]}
        ---
        
        **Instructions:**
        1.  Create a compelling headline from the video title.
        2.  Write a short, engaging introduction that hooks the reader and states the video's purpose.
        3.  Analyze the provided content source and identify 3-5 main themes, topics, or key takeaways.
        4.  For each key takeaway, create a well-defined section with a descriptive subheading. Elaborate on each point, providing context and explanation.
        5.  Write a thoughtful conclusion that summarizes the main points and provides a final thought for the reader.
        6.  Ensure the entire output is a single, complete blog post in Markdown format. Do not include any of your own commentary, preamble, or postamble.
        """
        return system_prompt, user_prompt

    def _create_tutorial_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Creates the system and user prompts for a tutorial."""
        system_prompt = (
            "You are a technical writer who excels at creating clear, step-by-step tutorials from video content. "
            "Your goal is to make complex processes easy to follow. You must use Markdown for formatting, especially "
            "numbered lists for steps, and code blocks for any code examples."
        )
        
        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
        Please generate a step-by-step tutorial in Markdown format based on the following video information.

        **Video Title:** {video_data.get('title')}
        **Channel:** {video_data.get('channel_name')}
        **Content Source (from {source_type}):**
        ---
        {content_source[:4000]}
        ---
        
        **Instructions:**
        1.  Create a clear, action-oriented headline.
        2.  Write a brief overview of what the tutorial covers and what the user will learn.
        3.  If applicable, list any prerequisites (e.g., software, prior knowledge).
        4.  Analyze the content source and break down the process into a logical sequence of numbered steps.
        5.  For each step, provide a clear heading and a concise explanation of the actions to take.
        6.  Conclude with a summary of what was accomplished.
        7.  Ensure the entire output is a single, complete tutorial in Markdown format.
        """
        return system_prompt, user_prompt

    def _create_review_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Creates the system and user prompts for a review."""
        system_prompt = (
            "You are a critical reviewer who writes balanced and insightful reviews of products, services, or media shown in videos. "
            "Your writing should be objective and well-supported. Use Markdown for structure, such as headings for different review criteria (e.g., Pros, Cons)."
        )

        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
        Please generate a detailed review in Markdown format based on the following video.

        **Video Title:** {video_data.get('title')}
        **Channel:** {video_data.get('channel_name')}
        **Content Source (from {source_type}):**
        ---
        {content_source[:4000]}
        ---
        
        **Instructions:**
        1.  Create a headline for the review.
        2.  Start with a summary of the item being reviewed.
        3.  Analyze the content to identify the key positive aspects (Pros) and negative aspects (Cons). Present these in bulleted lists under respective subheadings.
        4.  Include a section for your 'Verdict' or 'Final Thoughts'.
        5.  Assign a rating out of 5 stars if appropriate.
        6.  The final output must be a single, complete review in Markdown format.
        """
        return system_prompt, user_prompt

    def _create_summary_prompt(self, video_data: Dict[str, Any], transcript: Optional[str]) -> Tuple[str, str]:
        """Creates the system and user prompts for a summary."""
        system_prompt = (
            "You are an efficient assistant skilled at summarizing video content into concise, easy-to-digest key points. "
            "Your output should be structured and scannable. Use Markdown, especially bullet points."
        )

        content_source, source_type = self._get_content_source(video_data, transcript)

        user_prompt = f"""
        Please generate a concise summary in Markdown format of the following video.

        **Video Title:** {video_data.get('title')}
        **Channel:** {video_data.get('channel_name')}
        **Content Source (from {source_type}):**
        ---
        {content_source[:4000]}
        ---

        **Instructions:**
        1.  Use the video title as the main heading.
        2.  Provide a one-paragraph overview of the video's main topic.
        3.  Create a bulleted list of the most important key takeaways or highlights from the video. Aim for 5-7 points.
        4.  Keep the language clear and direct.
        5.  The final output must be a single, complete summary in Markdown format.
        """
        return system_prompt, user_prompt