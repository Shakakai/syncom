import pytest
from pydantic.fields import Field, ClassVar

from syncom import TypedTemplate


class StringTemplate(TypedTemplate):
    template_string: ClassVar[str] = "Hello, {{ name }}!"
    name: str = Field(description="Person's name.", required=True)


class FileTemplate(TypedTemplate):
    template_file: ClassVar[str] = "test_template.txt"
    name: str = Field(description="Person's name.", required=True)


def test_string_template():
    template = StringTemplate(name="Todd")
    result = template.render()
    assert result == "Hello, Todd!"


def test_file_template():
    template = FileTemplate(name="Todd")
    result = template.render()
    assert result == "Hello, Todd!"


def test_template_failure():
    with pytest.raises(Exception):
        template = StringTemplate()
        assert False, "Should throw an error due to missing name property"


def test_template_failure_property_change():
    with pytest.raises(Exception):
        template = StringTemplate(name="Todd")
        template.name = None
        template.render()
        assert False, "Render should throw an error due to missing name property"
