# (436)
# (190)
# eg : HIVE-494fc462-e060-4617-9baf-3b35793a37f8
"""
Strategie

494fc462-e060-4617-9baf-3b35793a37f8

1. Retrieve callerId form  `submitDAGSession(429)`:

2020-09-15 22:34:41,833 INFO  [HiveServer2-Background-Pool: Thread-199227]: client.TezClient (TezClient.java:submitDAGSession(429)) - Submitting dag to TezSession, sessionName=HIVE-ec1e078a-5e58-47c6-aa33-cdd221b3f5b3, applicationId=application_1598886766592_49581, dagName=SELECT * FROM rep_prd...sc_quote_line_item_c(Stage-1), callerContext={ context=HIVE, callerType=HIVE_QUERY_ID, callerId=hive_20200915175336_89c35e6d-0b15-4f26-bba0-67f0185e3a36 }

2. With callerid you can retrieve `execute(1423)` which contains the query

2020-09-15 14:40:52,517 INFO  [HiveServer2-Background-Pool: Thread-182868]: ql.Driver (Driver.java:execute(1423)) - Starting command(queryId=hive_20200915144052_e80d53b2-832e-42a9-88aa-4fe3e5c07bab): SELECT num_service FROM rep_prd_fbo_project.parametres_cedre_c

eg. grep like:

➜ zgrep -E 'TezClient.java:submitDAGSession|Driver.java:execute' hiveserver2.log > query.log

"""
from typing import List, Pattern, Iterator
from pathlib import Path
from dataclasses import dataclass, field
import gzip
import re
import pandas as pd


def grep_multiline_gz(path: Path, token: str, newline: Pattern) -> List[str]:
    logfile = gzip.open(path, 'rt')
    return grep_multiline(logfile, token, newline)


def grep_multiline(lines: Iterator, token: str, newline: Pattern) -> List[str]:
    """
    NOTE: it will skip a line don't use it as a standard solution
    """
    result = []
    for line in lines:
        chunk = []
        if token in line:
            chunk.append(line)
            for subline in lines:
                if newline.match(subline):
                    result.append(''.join(chunk))
                    break
                else:
                    # we'll skip a line in main for loop
                    # but we don't mind as we expect each relevant line
                    # to have several lines between them
                    chunk.append(subline)
    return result


@dataclass
class HiveServer:
    logs: List[str]
    newline: Pattern = re.compile(r'(\d+-?){3}\s(\d+[:,]?){4}')
    # TezClient.java:submitDAGSession(429)
    submit_dag: Pattern = re.compile(
        r'(?P<ts>(\d+-?){3}\s(\d+[:,]?){4})\s(?P<level>[A-Z]+)\s{2}.*Thread-(?P<thread>[0-9]+)(.*)(?P<id_application>application_[0-9]+_[0-9]+)', re.S)
    # Driver.java.execute
    driver_execute: Pattern = re.compile(
        r'(?P<ts>(\d+-?){3}\s(\d+[:,]?){4})\s(?P<level>[A-Z]+)\s{2}.*Thread-(?P<thread>[0-9]+).*(?P<id_caller>hive[0-9_\-a-z]+)\):\s(?P<query>.*)', flags=re.S)
    mapping: List[dict] = field(default_factory=list)
    queries: List[dict] = field(default_factory=list)
    token_mapping = 'TezClient.java:submitDAGSession(429)'
    token_query = 'Driver.java:execute(1423)'
    dataset: pd.DataFrame = pd.DataFrame()

    def __post_init__(self):
        self.mapping = [self.parse_submit_dag(
            line) for line in self.logs if self._is_mapping(line)]
        self.queries = [self.parse_driver_execute(
            line) for line in self.logs if self._is_query(line)]
        if len(self.mapping) > 0:
            df_mapping = pd.DataFrame(self.mapping).drop(
                columns=['ts', 'level'])
            df_queries = pd.DataFrame(self.queries)
            self.dataset = pd.merge(
                df_mapping, df_queries, on='thread').set_index('id_application')

    @classmethod
    def from_file(cls, log: Path):
        cls.token_mapping
        lines_mapping = grep_multiline(
            log.open('r'), cls.token_mapping, cls.newline)
        lines_query = grep_multiline(
            log.open('r'), cls.token_query, cls.newline)
        return cls(lines_mapping+lines_query)

    @classmethod
    def from_gz_file(cls, log: Path):
        cls.token_mapping
        lines_mapping = grep_multiline(
            gzip.open(log, 'rt'), cls.token_mapping, cls.newline)
        lines_query = grep_multiline(
            gzip.open(log, 'rt'), cls.token_query, cls.newline)
        return cls(lines_mapping+lines_query)

    def _is_mapping(self, line: str) -> bool:
        return self.token_mapping in line

    def _is_query(self, line: str) -> bool:
        return self.token_query in line

    @staticmethod
    def parse_line(line: str, pattern: Pattern) -> dict:
        try:
            return pattern.match(line).groupdict()
        except AttributeError:
            return {}

    def parse_submit_dag(self, line) -> dict:
        return self.parse_line(line, self.submit_dag)

    def parse_driver_execute(self, line) -> dict:
        return self.parse_line(line, self.driver_execute)

    def get_thread(self, app_id: str) -> str:
        try:
            return self.dataset.loc[app_id, 'thread']
        except KeyError:
            return ''

    def get_query(self, app_id: str) -> str:
        try:
            return self.dataset.loc[app_id, 'query']
        except KeyError:
            return ''
