import asyncio
import os
from instructor import OpenAISchema
from pydantic import BaseModel, Field
from typing import ClassVar, List, Dict, Any
from syncom import (
    AIModel,
    TemplatePromptStep,
    TypedTemplate,
    make_pipeline,
    run_pipeline,
    LLMStep,
    RunnableConfig,
    configure_engine, LogStep, FunctionalStep
)


class BlogPost(OpenAISchema):
    """
    This is the core schema used to generate and refine a blog post.
    The LLM will return an instance of this schema.
    """
    title: str = Field(description="Title of the blog post. Must be less than 100 characters.")
    content: str = Field(description="Content of the blog post. Must be written in markdown.")
    summary: str = Field(
        description="Summary of the blog post in plain text. Must be less than 200 characters."
    )
    image_prompt: str = Field(
        description="Prompt to generate the header image for this blog post via Dall-E or Stable Diffusion. "
                    "Must be at least 100 characters. Must include visual langauge to generate a compelling image."
    )


class Article(BaseModel):
    """
    This is a schema for an article.
    Files from disk are used to create instances of this schema.
    """
    title: str = Field(description="Title of the article.")
    content: str = Field(description="Content of the article.")


class BlogAuthorPrompt(TypedTemplate):
    """
    This is the Prompt used to write the initial version of the blog post.
    The prompt is found in ./templates/author.md
    """
    template_file: ClassVar[str] = "author.md"

    concept: str = Field(description="The concept for the new blog post")
    articles: List[Article] = Field(description="The research articles to use for the post")


class BlogEditorPrompt(TypedTemplate):
    """
    This is the Prompt used to edit a blog post to improve readability and the quality of the writing.
    The prompt is found in ./templates/editor.md
    """
    template_file: ClassVar[str] = "editor.md"

    concept: str = Field(description="The concept for the new blog post")
    articles: List[Article] = Field(description="The research articles to use for the post")
    title: str = Field(description="Title of the blog post. Must be less than 100 characters.")
    content: str = Field(description="Content of the blog post. Must be written in markdown.")
    summary: str = Field(
        description="Summary of the blog post in plain text. Must be less than 200 characters."
    )
    image_prompt: str = Field(
        description="Prompt to generate the header image for this blog post via Dall-E or Stable Diffusion. "
                    "Must be at least 100 characters. Must include visual langauge to generate a compelling image."
    )


def create_article(file_path: str) -> Article:
    """
    Read file from disk and create an instance of an Article.
    :param file_path:
    :return: Article
    """
    with open(file_path, "r") as file:
        content = file.read()
    return Article(title=os.path.basename(file_path), content=content)


def sub_directory_path(file_path: str) -> str:
    """
    Get the relative path to the file.
    :param file_path:
    :return: Relative path
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_directory, file_path)


def load_articles():
    """
    Load the articles from disk.
    Reads all the articles from the sample_articles directory and creates a list of Article objects.
    :return: A list of articles
    """
    articles = []
    sample_dir = sub_directory_path("sample_articles")
    for f in os.listdir(sample_dir):
        file_path = os.path.join(sample_dir, f)
        art = create_article(file_path)
        articles.append(art)
    return articles


async def build_template_vars(post: BlogPost, context: Dict[str, Any]):
    """
    Combines the current step data with additional context data.
    :param post: This comes from the previous step in the pipeline.
    :param context: This is static data provided at pipeline creation.
    :return: A dictionary to create a BlogEditorPrompt in the next step in the pipeline.
    """
    return {**post.dict(), **context}


async def build_blog_post():
    """
    We have all the components. Let's connect them up!
    :return:
    """

    # tell the template engine where to find the templates
    # You must call this if you are using TypedTemplates in your pipeline
    # It configures the django template engine for usage
    dirs = [sub_directory_path("templates")]
    configure_engine(dirs=dirs, debug=True)

    # Select the LLM model to use
    model = AIModel(
        name="gpt-4-0125-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # This is the input data to start the pipeline
    # You'll note this dictionary matches the required data for the BlogAuthorPrompt
    # The first step in the pipeline
    input_data = {
        "concept": "Write a blog post about the best prompt engineering practices according to the articles provided.",
        "articles": load_articles()
    }

    # Finally, we define the actually steps in the pipeline
    steps = (
        TemplatePromptStep(
            "You are an AI journalist. "
            "You must write high-quality articles that could be "
            "published in the New York Times or Wall Street Journal.",
            BlogAuthorPrompt
        ),
        LogStep("After BlogAuthorPrompt"),
        LLMStep(model, BlogPost),
        FunctionalStep(build_template_vars, input_data),
        TemplatePromptStep(
            "You are an AI Editor. "
            "Take the provided article(s) and improve them by editing individual sentences and paragraphs.",
            BlogEditorPrompt
        ),
        LogStep("After BlogEditorPrompt"),
        LLMStep(model, BlogPost),
    )

    # Create the pipeline and run it
    pipeline = make_pipeline(RunnableConfig(verbose=True), *steps)
    result: BlogPost = await run_pipeline(pipeline, input_data)
    print("RESULT "+"-"*50)
    print(f"Title: {result.title}")
    print(f"Content: {result.content}")
    print(f"Summary: {result.summary}")
    print(f"Image Prompt: {result.image_prompt}")


if __name__ == "__main__":
    asyncio.run(build_blog_post())
