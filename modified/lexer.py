#-------------------------------------------------------------------------------
# lexer.py
#
# A generic regex-based Lexer/tokenizer tool.
# See the if __main__ section in the bottom for an example.
#
# Eli Bendersky (eliben@gmail.com)
# This code is in the public domain
# Last modified: August 2010
#-------------------------------------------------------------------------------
import re
import sys
import cyk_parser


class Token(object):
    """ A simple Token structure.
        Contains the token type, value and position.
    """
    def __init__(self, type, val, pos):
        self.type = type

    def __str__(self):
        return '%s' % (self.type)


class LexerError(Exception):
    """ Lexer error exception.
        pos:
            Position in the input line where the error occurred.
    """
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    """ A simple regex-based lexer/tokenizer.
        See below for an example of usage.
    """
    def __init__(self, rules, skip_whitespace=True):
        """ Create a lexer.
            rules:
                A list of rules. Each rule is a `regex, type`
                pair, where `regex` is the regular expression used
                to recognize the token and `type` is the type
                of the token to return when it's recognized.
            skip_whitespace:
                If True, whitespace (\s+) will be skipped and not
                reported by the lexer. Otherwise, you have to
                specify your rules for whitespace, or it will be
                flagged as an error.
        """
        # All the regexes are concatenated into a single one
        # with named groups. Since the group names must be valid
        # Python identifiers, but the token types used by the
        # user are arbitrary strings, we auto-generate the group
        # names and map them to token types.
        #
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        """ Initialize the lexer with a buffer as input.
        """
        self.buf = buf
        self.pos = 0

    def token(self):
        """ Return the next token (a Token object) found in the
            input buffer. None is returned if the end of the
            buffer was reached.
            In case of a lexing error (the current chunk of the
            buffer matches no rule), a LexerError is raised with
            the position of the error.
        """
        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        """ Returns an iterator to the tokens found in the buffer.
        """
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok


if __name__ == '__main__':
    rules = [
        # RESERVED WORDS
        (r'False',           'FALSE'),
        (r'None',            'NONE'),
        (r'True',            'TRUE'),
        (r'and',             'AND'),
        (r'as',              'AS'),
        (r'break',           'BREAK'),
        (r'class',           'CLASS'),
        (r'continue',        'CONTINUE'),
        (r'def',             'DEF'),
        (r'elif',            'ELIF'),
        (r'else',            'ELSE'),
        (r'for',             'FOR'),
        (r'from',            'FROM'),
        (r'if',              'IF'),
        (r'import',          'IMPORT'),
        (r'in',              'IN'),
        (r'is',              'IS'),
        (r'not',             'NOT'),
        (r'or',              'OR'),
        (r'pass',            'PASS'),
        (r'raise',           'RAISE'),
        (r'return',          'RETURN'),
        (r'while',           'WHILE'),
        (r'with',            'WITH'),
        (r'is',              'COMPARE'),
        (r'not',             'COMPARE'),
        ('\d+',             'NUMBER'),
        ('[a-zA-Z_]\w+',    'IDENTIFIER'),
        (r'==',                'COMPARE'),
        ('[!=]',              'COMPARE'),
        ('>',                 'COMPARE'),
        ('<',                 'COMPARE'),
        ('[>=]',              'COMPARE'),
        ('[<=]',              'COMPARE'),        
        (r"[+=]",              'ASSIGN'),
        (r'[-=]',              'ASSIGN'),
        ('[*=]',              'ASSIGN'),
        ('[/=]',              'ASSIGN'),
        ('[%=]',              'ASSIGN'),
        ('[//=]',             'ASSIGN'),
        ('[**=]',             'ASSIGN'),
        # COMPARISON
        (r'==',                'COMPARE'),
        ('[!=]',              'COMPARE'),
        ('>',                 'COMPARE'),
        ('<',                 'COMPARE'),
        ('[>=]',              'COMPARE'),
        ('[<=]',              'COMPARE'),
                # ETCS
        (':',                 'COLON'),
        ('.',                 'DOT'),
        ('\n',                'NEWLINE'),
        # ARITHMETIC
        ('\+',              'ARITHMETIC'),
        ('\-',              'ARITHMETIC'),
        ('\*',              'ARITHMETIC'),
        ('\/',              'ARITHMETIC'),
        ('%',               'ARITHMETIC'),
        ('//]',            'ARITHMETIC'),
        ('[**]',            'ARITHMETIC'),
        # PARENTHESIS
        ('\(',              'LP'),
        ('\)',              'RP'),
        ('\[',              'LSB'),
        ('\]',              'RSB'),
        # ASSIGNMENT
        # ('=',                 'ASSIGN'),
    ]

    lx = Lexer(rules, skip_whitespace=True)
    lx.input('''
    def get_rule_category:
    rule_product = rule[PRODUCT_KEY]
    if len(rule_product) == 0:
        return EPSILON_RULE_KEY
    elif len(rule_product) == 1:
        if rule_product[0].islower:
            return TERMINAL_RULE_KEY
        else:
            return UNARY_RULE_KEY
    elif len(rule_product) == 2:
        return BINARY_RULE_KEY
    else:
        return N_ARIES_RULE_KEY
    ''')

    output = ''
    try:
        for tok in lx.tokens():
            if tok == '':
                output = output
            else:
                output += str(tok) + ' '
            print(tok)
    except LexerError as err:
        print('LexerError at position %s' % err.pos)

    print(output)