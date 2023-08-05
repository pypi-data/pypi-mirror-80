hint = 'However if your program needn\'t this package,this warning is neglectable.'
try:
    from .matplotlib.qt5agg import PMMatplotlibQt5Widget
except:
    import warnings

    warnings.warn('matplotlib is not installed. ' + hint)
    pass
try:
    from .browser.browser import QWebEngineView
except:
    import warnings

    warnings.warn('QWebengine is not installed. ' + hint)
    pass
