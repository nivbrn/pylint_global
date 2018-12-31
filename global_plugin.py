import re
import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import IAstroidChecker
from pylint.checkers.utils import check_messages

GLOBAL_NAME_RGX = r'^g_\w+$|^[A-Z_]*$'


def register(linter):
    linter.register_checker(ConstsAndGlobalsChecker(linter))


class ConstsAndGlobalsChecker(BaseChecker):
    """
    Implements a few pylint checks on unitests asserts -
     making sure the right assert is used if assertTrue or
    assertFalse are misused.
    """
    __implements__ = IAstroidChecker

    name = 'global_vars_consts'
    priority = -1
    msgs = {
        'C0130': (
            'Global variable %r is not in format g_xxx',
            'global-var-format',
            'All globals, which is no constants, should be in format g_*'
        ),
    }

    options = (
        (
            'global-rgx',
            {
                'default': GLOBAL_NAME_RGX, 'type': 'regexp', 'metavar': '<regexp>',
                'help': 'Regular expression which should only match correct '
                        'module level global variables'
            }
        ),
    )

    @check_messages('global-var-format')
    def visit_assignname(self, node):
        if isinstance(node.scope(), astroid.Module) and \
                isinstance(node.assign_type(), astroid.Assign) and \
                not re.match(self.config.global_rgx, node.name):
            self.add_message('global-var-format', args=node.name, node=node)



