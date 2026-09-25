"""Imports"""
import re


"""Functions"""
def create_slug(title: str) -> str:
    """Converts a title into a URL/filename-friendly slug."""
    new_title = re.sub(r"[^\w\d]+", "-", title)
    return new_title.lower().strip("-")

print(create_slug("Ginning"))
print(create_slug("Traditional Weaving Process"))
print(create_slug("Eri Silk - Reeling"))