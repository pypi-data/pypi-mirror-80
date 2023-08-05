from aim.ql.lexer import lexer
from aim.ql.lexer import grouping
from aim.ql.lexer.splitter import StatementSplitter


class FilterStack(object):
    def __init__(self):
        self.preprocess = []
        self.stmtprocess = []
        self.postprocess = []
        self._grouping = False

    def enable_grouping(self):
        self._grouping = True

    def run(self, ql, encoding=None):
        stream = lexer.tokenize(ql, encoding)
        # Process token stream
        for filter_ in self.preprocess:
            stream = filter_.process(stream)

        stream = StatementSplitter().process(stream)

        # Output: Stream processed Statements
        for stmt in stream:
            if self._grouping:
                stmt = grouping.group(stmt)

            for filter_ in self.stmtprocess:
                filter_.process(stmt)

            for filter_ in self.postprocess:
                stmt = filter_.process(stmt)

            yield stmt