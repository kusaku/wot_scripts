# Embedded file name: scripts/common/pydev/_pydev_bundle/_pydev_completer.py
import pydevconsole
try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

try:
    False
    True
except NameError:
    setattr(__builtin__, 'True', 1)
    setattr(__builtin__, 'False', 0)

try:
    import java.lang
    from _pydev_bundle import _pydev_jy_imports_tipper
    _pydev_imports_tipper = _pydev_jy_imports_tipper
except ImportError:
    IS_JYTHON = False
    from _pydev_bundle import _pydev_imports_tipper

from _pydevd_bundle import pydevd_vars
dir2 = _pydev_imports_tipper.generate_imports_tip_for_module

class _StartsWithFilter:
    """
        Used because we can't create a lambda that'll use an outer scope in jython 2.1 
    """

    def __init__(self, start_with):
        self.start_with = start_with.lower()

    def __call__(self, name):
        return name.lower().startswith(self.start_with)


class Completer:

    def __init__(self, namespace = None, global_namespace = None):
        """Create a new completer for the command line.
        
        Completer([namespace,global_namespace]) -> completer instance.
        
        If unspecified, the default namespace where completions are performed
        is __main__ (technically, __main__.__dict__). Namespaces should be
        given as dictionaries.
        
        An optional second namespace can be given.  This allows the completer
        to handle cases where both the local and global scopes need to be
        distinguished.
        
        Completer instances should be used as the completion mechanism of
        readline via the set_completer() call:
        
        readline.set_completer(Completer(my_namespace).complete)
        """
        if namespace is None:
            self.use_main_ns = 1
        else:
            self.use_main_ns = 0
            self.namespace = namespace
        if global_namespace is None:
            self.global_namespace = {}
        else:
            self.global_namespace = global_namespace
        return

    def complete(self, text):
        """Return the next possible completion for 'text'.
        
        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.
        
        """
        if self.use_main_ns:
            raise RuntimeError('Namespace must be provided!')
            self.namespace = __main__.__dict__
        if '.' in text:
            return self.attr_matches(text)
        else:
            return self.global_matches(text)

    def global_matches(self, text):
        """Compute matches when text is a simple name.
        
        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace or self.global_namespace that match.
        
        """

        def get_item(obj, attr):
            return obj[attr]

        a = {}
        for dict_with_comps in [__builtin__.__dict__, self.namespace, self.global_namespace]:
            a.update(dict_with_comps)

        filter = _StartsWithFilter(text)
        return dir2(a, a.keys(), get_item, filter)

    def attr_matches(self, text):
        """Compute matches when text contains a dot.
        
        Assuming the text is of the form NAME.NAME....[NAME], and is
        evaluatable in self.namespace or self.global_namespace, it will be
        evaluated and its attributes (as revealed by dir()) are used as
        possible completions.  (For class instances, class members are are
        also considered.)
        
        WARNING: this can still invoke arbitrary C code, if an object
        with a __getattr__ hook is evaluated.
        
        """
        import re
        m = re.match('(\\S+(\\.\\w+)*)\\.(\\w*)$', text)
        if not m:
            return []
        expr, attr = m.group(1, 3)
        try:
            obj = eval(expr, self.namespace)
        except:
            try:
                obj = eval(expr, self.global_namespace)
            except:
                return []

        filter = _StartsWithFilter(attr)
        words = dir2(obj, filter=filter)
        return words


def generate_completions_as_xml(frame, act_tok):
    if frame is None:
        return '<xml></xml>'
    else:
        updated_globals = {}
        updated_globals.update(frame.f_globals)
        updated_globals.update(frame.f_locals)
        if pydevconsole.IPYTHON:
            completions = pydevconsole.get_completions(act_tok, act_tok, updated_globals, frame.f_locals)
        else:
            completer = Completer(updated_globals, None)
            completions = completer.complete(act_tok)
        valid_xml = pydevd_vars.make_valid_xml_value
        quote = pydevd_vars.quote
        msg = ['<xml>']
        for comp in completions:
            msg.append('<comp p0="')
            msg.append(valid_xml(quote(comp[0], '/>_= \t')))
            msg.append('" p1="')
            msg.append(valid_xml(quote(comp[1], '/>_= \t')))
            msg.append('" p2="')
            msg.append(valid_xml(quote(comp[2], '/>_= \t')))
            msg.append('" p3="')
            msg.append(valid_xml(quote(comp[3], '/>_= \t')))
            msg.append('"/>')

        msg.append('</xml>')
        return ''.join(msg)