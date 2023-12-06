import re


def camel_to_kebab(name: str):
    # Add a hyphen before each capital letter (except the first one if it's capital) and lowercases all characters
    kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    return kebab
