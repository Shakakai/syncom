from typing import ClassVar, Optional

import litellm
from django.conf import settings
from django.template import Engine, Context, Template
from pydantic import BaseModel
from pydantic.fields import PrivateAttr

engine: Optional[Engine] = None


def configure_engine(dirs=None, debug=True):
    settings.configure(
        DEBUG=debug,
        USE_L10N=False,
    )

    global engine

    engine = Engine(
        dirs=dirs,
        app_dirs=False,
        context_processors=None,
        debug=debug,
        loaders=None,
        string_if_invalid="",
        file_charset="utf-8",
        libraries=None,
        builtins=Engine.default_builtins,
        autoescape=False,
    )


def check_engine():
    if engine is None:
        raise Exception("Engine not configured. Must call configure_engine before usage.")


def template_from_string(raw_template: str) -> Template:
    check_engine()
    template = engine.from_string(raw_template)
    return template


def template_from_file(file_path: str) -> Template:
    check_engine()
    template = engine.get_template(file_path)
    return template


def render_template_from_string(raw_template: str, context: dict) -> str:
    template = template_from_string(raw_template)
    context = Context(context)
    return template.render(context)


class TypedTemplate(BaseModel):
    template_file: ClassVar[Optional[str]] = None
    template_string: ClassVar[Optional[str]] = None
    _template: Optional[Template] = PrivateAttr(default=None)

    def __init__(
            self,
            _template: Optional[Template] = None,
            **kwargs
    ):
        super().__init__(**kwargs)
        if _template is None:
            if hasattr(self, "template_string") and self.template_string is not None:
                _template = template_from_string(self.template_string)
            elif hasattr(self, "template_file") and self.template_file is not None:
                _template = template_from_file(self.template_file)
            else:
                raise Exception("No template provided or configured.")

        self._template = _template

    def get_context(self, context: dict) -> Context:
        ctx = {**self.dict(), **context}
        self.model_validate(ctx)
        return Context(ctx)

    def render(self, context: dict = None) -> str:
        context = context if context is not None else {}
        ctx = self.get_context(context)
        result = self._template.render(ctx)
        return result
