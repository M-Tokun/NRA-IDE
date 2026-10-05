"""Cline 4.1.22 nested hook payload adapter; no host auto-approval."""
import copy
import json
import os
import sys

READ_TOOLS = frozenset({'readFile', 'read_files', 'read_file', 'list_files',
    'list_directory', 'list_code_definition_names', 'search_files', 'search_codebase', 'search'})
FILE_READ_TOOLS = frozenset({'readFile', 'read_files', 'read_file'})
RANGE_FIELDS = frozenset({'offset', 'limit', 'start_line', 'end_line', 'startLine',
    'endLine', 'line_range', 'lineRange', 'ranges'})
# Installed VS Code hook runner caps contextModification at 50,000 JS UTF-16 units.
CONTEXT_LIMIT = 50000


def normalize_payload(payload):
    events = [name for name in ('preToolUse', 'postToolUse') if name in payload]
    if not events:
        return payload  # Existing flat adapter fixtures remain supported.
    if len(events) != 1 or any(k in payload for k in ('tool_name', 'parameters', 'tool_input', 'tool_response')):
        raise ValueError('Conflicting Cline payload')
    event = events[0]
    nested = payload[event]
    if not isinstance(nested, dict) or not isinstance(nested.get('toolName'), str):
        raise ValueError('Invalid Cline tool')
    # Cline's protobuf toJSON omits an empty parameters map. Explicit null is invalid.
    args = nested.get('parameters', {})
    if not isinstance(args, dict):
        raise ValueError('Invalid Cline arguments')
    result = copy.deepcopy(payload)
    # Unknown Cline names must not inherit another host's built-in read exemption.
    result['tool_name'] = 'Read' if nested['toolName'] in FILE_READ_TOOLS else 'cline_tool:' + nested['toolName']
    result['parameters'] = copy.deepcopy(args)
    if event == 'postToolUse':
        success = nested.get('success')
        if type(success) is not bool or not isinstance(nested.get('result'), str):
            raise ValueError('Invalid Cline read result')
        result['tool_response'] = {'content': nested['result'],
            'is_error': not success or nested['toolName'] not in FILE_READ_TOOLS}
        if RANGE_FIELDS.intersection(args):
            result['parameters']['limit'] = 0  # Preserve any partial-read indicator.
        if len(set(args).intersection({'path', 'file_path', 'absolute_path', 'paths'})) != 1:
            result['tool_response']['is_error'] = True
    if nested['toolName'] in FILE_READ_TOOLS:
        paths = args.get('paths')
        if paths is not None:
            if set(args).intersection({'path', 'file_path', 'absolute_path', 'paths'}) != {'paths'}:
                raise ValueError('Ambiguous Cline read paths')
            if isinstance(paths, str):
                paths = json.loads(paths)
            if not isinstance(paths, list) or len(paths) != 1 or not isinstance(paths[0], str):
                if event == 'postToolUse':
                    result['tool_response']['is_error'] = True
            else:
                del result['parameters']['paths']
                result['parameters']['path'] = paths[0]
        # Resolve relative read paths against this contract, never the hook cwd.
        import _common
        for key in ('path', 'file_path', 'absolute_path'):
            path = result['parameters'].get(key)
            if isinstance(path, str) and not os.path.isabs(path):
                result['parameters'][key] = os.path.join(os.path.dirname(_common.AGENTS_MD_PATH), path)
    return result


def run_task_start():
    import _common
    emitted = False
    try:
        payload = _common.load_payload(sys.stdin, 'cline')
        task_id = payload['taskId']
        _common.invalidate_marker('cline', task_id)
        if payload.get('hookName') not in (None, 'TaskStart', 'TaskResume', 'agent_start', 'agent_resume'):
            raise ValueError('Invalid startup event')
        content = _common.read_agents_md()
        context = 'AGENTS.md loaded\n\n' + content
        if len(context.encode('utf-16-le')) // 2 > CONTEXT_LIMIT:
            raise ValueError('Contract exceeds Cline context limit')
        print(json.dumps({'cancel': False, 'contextModification': context,
                          'errorMessage': ''}, ensure_ascii=True), flush=True)
        emitted = True
        _common.write_marker('cline', task_id, content)
        return 0
    except Exception:
        if emitted:
            # Windows helper discards captured success output on nonzero exit.
            return 2
        try:
            _common.emit_guard_result('cline', _common.INVALID_PAYLOAD_MESSAGE)
            return 0
        except Exception:
            return 2
