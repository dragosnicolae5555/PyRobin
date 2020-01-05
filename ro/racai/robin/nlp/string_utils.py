
class StringUtils:
    """
    <p>Class dealing with string-related useful functions.</p>
    """
    @staticmethod
    def is_none_empty_or_blank(input):
        return input in (None, "") or not input.strip()
