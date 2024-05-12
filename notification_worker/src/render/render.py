import logging

from jinja2 import BaseLoader, Environment, TemplateSyntaxError, UndefinedError


async def render_template(template_content: str, context: dict) -> str:
    """
    Рендерит шаблон Jinja2 с данными из context.

    :param template_content: Строка содержимого шаблона Jinja2.
    :param context: Словарь с переменными, которые будут доступны в шаблоне.
    :return: Отрендеренный шаблон в виде строки.
    """
    env = Environment(loader=BaseLoader())
    try:
        template = env.from_string(template_content)
        return template.render(context)
    except (TemplateSyntaxError, UndefinedError) as e:
        logging.error(f"Ошибка при рендеринге шаблона: {e}")
