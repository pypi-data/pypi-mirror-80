"""parse yarn ressource manager log4j aggregated logs"""
from dataclasses import dataclass, field
from typing import List, Pattern, Iterable, Pattern
import re
import logging
import arrow
from itertools import groupby

FILEPATTERN = 'yarn-yarn-resourcemanager*.log*'


@dataclass
class Parser():
    pattern_line: Pattern = field(init=False)

    def __post_init__(self):
        self.pattern_line = re.compile(
            r'(?P<ts>(\d+-?){3}\s(\d+[:,]?){4})\s(?P<level>[A-Z]+)\s{2}(?P<javaclass>\w+\.\w+)\s\(.*\((?P<java_id>\d+)\)\)\s-\s(?P<payload>.*)')

    def parse(self, data: Iterable[str]) -> List[dict]:
        return [self.parse_line(line) for line in data]

    def parse_line(self, logline: str) -> dict:
        """try to parse line, fail silently by returning an empty dict"""
        try:
            return self.pattern_line.match(logline).groupdict()
        except Exception as e:
            logging.debug(e)
            return {}


@dataclass
class StateProcessor:
    pattern_state: Pattern = field(init=False)

    def __post_init__(self):
        self.pattern_state = re.compile(
            r'(?P<id_application>application_\d+_\d+)(.*)from\s(?P<from_state>[A-Z_]+)\sto\s(?P<to_state>[A-Z_]+)'
        )

    def parse(self, data: List[dict]) -> List[dict]:
        "parse 'state' line(transition) and discard other"
        def merge(line):
            return {**{'ts': line['ts']},
                    **(self.parse_payload(line['payload']))}
        valid = [line for line in data if self.is_state(line)]
        return [merge(elt) for elt in valid]

    def parse_payload(self, payload: str) -> dict:
        """try to parse, fail silently by returning an empty dict"""
        try:
            return self.pattern_state.match(payload).groupdict()
        except Exception as e:
            logging.debug(e)
            return {}

    @staticmethod
    def is_state(parsed: dict) -> bool:
        # code 779
        try:
            return parsed['java_id'] == '779'
        except KeyError:
            return False

    @staticmethod
    def make_name(from_state: str, to_state: str) -> str:
        return f'{from_state.lower()}_to_{to_state.lower()}'

    @staticmethod
    def delta(states: List[dict], from_state: str, to_state: str) -> dict:
        """reduce as diff of time"""
        def diff(first, last) -> int:
            if (not first) or (not last):
                return None
            else:
                return abs((arrow.get(last)-arrow.get(first)).seconds)

        def get_state(state):
            try:
                return list(filter(lambda x: x['to_state'] == state, states))[0]
            except IndexError:
                return ''
        # 'to_state' is the last state known.
        # It is the current state of the app at time T
        t1 = get_state(from_state)
        t2 = get_state(to_state)
        try:
            return {'id_application': states[0]['id_application'],
                    'accept_to_running_ts': t2['ts'],
                    StateProcessor.make_name(from_state, to_state): diff(t1['ts'], t2['ts'])}
        except (IndexError, TypeError):
            return {}

    @staticmethod
    def process_diff(parsed: List[dict],
                     from_state: str,
                     to_state: str) -> List[dict]:
        result = []
        def keyfunc(x): return x['id_application']
        sort_data = sorted(parsed, key=keyfunc)
        for key, group in groupby(sort_data, keyfunc):
            result.append(StateProcessor.delta(
                list(group), from_state, to_state))
        return result


@dataclass
class QueueProcessor:
    pattern: Pattern = field(init=False)

    def __post_init__(self):
        self.pattern = re.compile(
            r'(.*)(appId:\s)(?P<id_application>application[0-9_]+)\s(user:\s(?P<user>[a-zA-Z0-9]+)).*(leaf-queue:\s(?P<queue>[a-zA-Z0-9_]+))([^#])(\#user-pending-applications+:\s?(?P<nb_user_pending>\d+))([^#])(#user-active-applications:\s?(?P<nb_user_active>\d+))([^#])(#queue-pending-applications:\s?(?P<nb_queue_pending>\d+))([^#])(#queue-active-applications:\s?(?P<nb_queue_active>\d+))')

    def parse_payload(self, payload: str) -> dict:
        try:
            found = self.pattern.match(payload).groupdict()
        except (AttributeError, TypeError):
            return {}
        for k in found.keys():
            if 'nb_' in k:
                found[k] = int(found[k])
        return found

    def parse_line(self, logline: dict) -> dict:
        return {**{'queue_state_ts': logline['ts']},
                **(self.parse_payload(logline['payload']))}

    @staticmethod
    def is_queue(parsed: dict) -> bool:
        try:
            return (parsed['java_id'] == '744') and (parsed['javaclass'] == 'capacity.LeafQueue')
        except KeyError:
            return False


def kpi_accept_to_run_parsed(parsed: List[dict]) -> List[dict]:
    processor = StateProcessor()
    return processor.process_diff(processor.parse(parsed),
                                  from_state='ACCEPTED',
                                  to_state='RUNNING'
                                  )


def kpi_accept_to_run(lines: List[str]) -> List[dict]:
    return kpi_accept_to_run_parsed(Parser().parse(lines))


def kpi_nb_queue_parsed(parsed: List[dict]) -> List[dict]:
    return [QueueProcessor().parse_line(line) for line in parsed if QueueProcessor.is_queue(line)]


def kpi_nb_queue(lines: List[str]):
    return kpi_nb_queue_parsed(Parser().parse(lines))

# FIXME: see  test & README
# also branch filter queue for poc on notebook


def is_equal(a: dict, b: dict)->bool:
    """compare record parsed on 'id_application' key"""
    try:
        return a['id_application'] == b['id_application']
    except (KeyError,TypeError):
        return False


def process(lines: Iterable[str]) -> List[dict]:
    parsed = Parser().parse(lines)
    nb_queue = kpi_nb_queue_parsed(parsed)
    accept_to_run = kpi_accept_to_run_parsed(parsed)
    merged = []
    for queue in nb_queue:
        for to_run in accept_to_run:
            try:
                if is_equal(queue, to_run):
                    merged.append({**queue, **to_run})
            except KeyError:
                pass
    return merged

    # add state
    # add payload
    # be sure to have dt for both
    # dataframe join ?
    # return nb_queue
