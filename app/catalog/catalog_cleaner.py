import re

def parse_course_block(course_block: dict):
    """
    course_block is already structured:
    {
      title: str,
      description: str,
      level: str
    }
    """
    return {
        "title": course_block.get("title"),
        "description": course_block.get("description"),
        "level": course_block.get("level", "Graduate")
    }

