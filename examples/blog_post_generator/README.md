

# Blog Post Generator

In this example, we generate a blog post based on a concept (a short text explain the nature of the blog post) and a list of articles.


# File Structure

Here's file structure of this example:
- main.py: All of the python/syncom code to create the blog generation pipeline.
- templates: This folder contains the prompt templates referenced in main.py.
- sample_articles: This folder contains the research articles referenced in main.py.

# TODO

This is a list of things that could make the example better:
- Add additional steps to make GPT-4 create an article outline first and then write each section from the outline.
  - This would be a more structured approach to generating the article.
  - The Editor could then review both the outline and the full article compiled from the individual sections.
- Make this easier to run by adding arguments to the script for OpenAI key, concept, and article folder.