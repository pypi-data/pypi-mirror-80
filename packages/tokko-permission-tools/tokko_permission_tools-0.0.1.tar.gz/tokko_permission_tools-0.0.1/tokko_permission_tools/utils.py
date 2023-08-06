from jinja2 import Environment, BaseLoader


def render(flat_template: str, **data) -> str:
    template = Environment(loader=BaseLoader).from_string(flat_template)
    return template.render(**data)
