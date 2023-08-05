
import sys
from .languages import languages


def llck(lang, processors, options = {}):
    """[summary]

    Args:
        lang (str): ISO language naming
        processors (list): List for processing processors
        options (dict, optional): options used by the processores. Defaults to {}.

    Returns:
        class: class corosponding to the language
    """
    return languages[lang](processors, options)


sys.modules[__name__] = llck
