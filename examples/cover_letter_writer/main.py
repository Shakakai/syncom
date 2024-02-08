import asyncio
import os
from instructor import OpenAISchema
from pydantic import BaseModel, Field
from typing import ClassVar, List, Dict, Any, Optional
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


RESUME_ANALYSIS_SYSTEM_PROMPT = """
You are an AI resume analyst. 
You must extract information from a resume as accurately as possible.
"""

RESUME_WRITER_SYSTEM_PROMPT = """
You are an AI resume writer.
You must write the highest-quality resume possible.
"""


class Skill(BaseModel):
    name: str = Field(description="Name of the job skill. Should be a short but descriptive title for the skill.")
    description: str = Field(
        description="Why was this skill included in this list? Describe the skill and why it is important."
    )
    job: str = Field(description="Job from resume where the skill was previously used")


class Applicant(BaseModel):
    """
    This is a schema for an applicant.
    Files from disk are used to create instances of this schema.
    """
    name: str = Field(description="Name of the applicant.")
    email: str = Field(description="Email of the applicant.")
    phone: str = Field(description="Phone number of the applicant.")
    address: str = Field(description="Address of the applicant.")


class ResumeAnalysis(OpenAISchema):
    applicant: Applicant = Field(description="The individual referenced in the resume.")
    skills: List[Skill] = Field(description="These are the most impactful skills listed or implied in the resume.")


class CoverLetterResult(OpenAISchema):
    cover_letter: str = Field(description="This should be the whole text of the well-written cover letter.")
    notes: Optional[str] = Field(
        description="This should be any notes to the user about the cover letter. "
                    "For example, if there is anything missing in the cover letter that should be added."
    )


class ResumeAnalysisPrompt(TypedTemplate):
    template_file: ClassVar[str] = "resume_analysis_prompt.md"

    resume: str = Field(description="The user's resume")


class CoverLetterWriterPrompt(TypedTemplate):
    template_file: ClassVar[str] = "cover_letter_prompt.md"

    applicant: Applicant = Field(description="The individual referenced in the resume.")
    skills: List[Skill] = Field(description="These are the most impactful skills listed or implied in the resume.")
    job_description: str = Field(description="The job description for the job the user is applying for.")
    resume: str = Field(description="The user's resume")


def sub_directory_path(file_path: str) -> str:
    """
    Get the relative path to the file.
    :param file_path:
    :return: Relative path
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_directory, file_path)


def load_file(filename: str) -> str:
    """
    Read file from disk and return text content.
    :param filename:
    :return: text content
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "data", filename)
    with open(file_path, "r") as file:
        content = file.read()
    return content


async def build_template_vars(analysis: ResumeAnalysis, context: Dict[str, Any]):
    """
    Combines the current step data with additional context data.
    :param analysis: This is the data from the previous step in the pipeline.
    :param context: This is static data provided at pipeline creation.
    :return: A dictionary to create a CoverLetterWriterPrompt in the next step in the pipeline.
    """
    return {**analysis.dict(), **context}


async def write_cover_letter():
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

    # Load resume and job description from disk
    resume = load_file("resume.txt")
    job_description = load_file("job_description.txt")

    # Finally, we define the actually steps in the pipeline
    steps = (
        TemplatePromptStep(RESUME_ANALYSIS_SYSTEM_PROMPT, ResumeAnalysisPrompt),
        LogStep("ResumeAnalsyisPrompt"),
        LLMStep(model, ResumeAnalysis),
        LogStep("Resume Analysis"),
        FunctionalStep(build_template_vars, {"resume": resume, "job_description": job_description}),
        TemplatePromptStep(RESUME_WRITER_SYSTEM_PROMPT, CoverLetterWriterPrompt),
        LogStep("BlogEditorPrompt"),
        LLMStep(model, CoverLetterResult),
    )

    # Create the pipeline and run it
    pipeline = make_pipeline(RunnableConfig(verbose=True), *steps)
    result: CoverLetterResult = await run_pipeline(pipeline, {"resume": resume})
    print("RESULT "+"-"*50)
    print(f"Cover Letter: {result.cover_letter}")
    print(f"Notes: {result.notes}")


if __name__ == "__main__":
    asyncio.run(write_cover_letter())
