"""
Attributes
----------
loaded : dict
    Dictionary of the record styles that were successfully imported. The
    dictionary keys are the database style names, and the values are the
    loaded modules.
failed : dict
    Dictionary listing the record styles that failed import. Values
    contain the error messages thrown by the style.
"""
from ..tools import dynamic_import
from .Record import Record
from .CalculationRecord import CalculationRecord

ignorelist = ['Record', 'CalculationRecord']
loaded, failed = dynamic_import(__name__, ignorelist=ignorelist)

def load_record(style, name=None, content=None):
    """
    Loads a Record subclass associated with a given record style

    Parameters
    ----------
    style : str
        The record style
    name : str
        The name to give to the specific record
    content : 
        The record's data model content
    
    Returns
    -------
    subclass of iprPy.record.Record 
        A Record object for the style
    """
    return loaded[style](name=name, content=content)

__all__ = ['Record', 'load_record', 'failed', 'loaded']