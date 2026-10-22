"""Structural fixtures only: no test hosts, revisions or hashes assert real executions."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import jsonschema
import pytest
import yaml

from agent_harness.scripts.validate_round import LAB, check, discover

EXAMPLES = sorted((LAB / 'agent_harness/examples').glob('*/round-*/round.yaml'))


def write(path, data):
    path.write_text(yaml.safe_dump(data))
    return path


@pytest.fixture
def planned(tmp_path):
    source = EXAMPLES[0]
    shutil.copytree(source.parent / 'assignments', tmp_path / 'assignments')
    return tmp_path / 'round.yaml', yaml.safe_load(source.read_text())


@pytest.fixture
def completed(planned):
    path, data = planned
    data['status'] = 'active'
    # Deliberately synthetic commit-shaped strings, never stored as a real round.
    data['repos'] = {'forest_cover_lab': 'a' * 40, 'sentinel_monthly_forest_cover': 'b' * 40, 'lab_graph_revision': 'c' * 64}
    instance = data['instances'][0]
    instance['selection_status'] = 'completed'
    loaded = []
    for source, name in [('forest-cover-lab', 'AGENTS.md'), ('forest-cover-lab', 'docs/agents.md'), ('forest-cover-lab', instance['role']), ('round', instance['assignment'])]:
        content = (path.parent if source == 'round' else LAB) / name
        loaded.append({'source': source, 'path_or_identifier': name, 'revision': data['repos']['forest_cover_lab'] if source == 'forest-cover-lab' else None, 'sha256': hashlib.sha256(content.read_bytes()).hexdigest(), 'capture_status': 'captured'})
    instance['actual_executions'] = [{
        'attempt_id': 'synthetic-test-only', 'host': 'codex',
        'started_utc': '2026-10-21T10:00:00Z', 'ended_utc': '2026-10-21T10:01:00Z',
        'status': 'completed', 'model_if_known': None, 'loaded_harness': loaded,
        'prompt_ref': 'synthetic fixture', 'tool_access': [], 'source_refs': [],
        'output_refs': ['synthetic.txt'], 'output_hashes': {'synthetic.txt': hashlib.sha256(b'test-only').hexdigest()},
        'checks': ['fixture structure only; no scientific execution'],
        'limitations': ['Synthetic test record; not an observed host execution'],
    }]
    return path, data


def findings(record):
    path, data = record
    return check(write(path, data))


def test_roles_have_contracts():
    roles = list((LAB / 'agent_harness/roles').glob('*.md'))
    assert roles
    for role in roles:
        for marker in ('**Mandate:**', '**Required inputs:**', '**Outputs:**', '**Stop/escalate:**'):
            assert marker in role.read_text()


def test_schema_and_local_rounds():
    schema = json.loads((LAB / 'agent_harness/schemas/round.schema.json').read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    assert EXAMPLES
    for path in discover(LAB):
        assert not check(path), check(path)
    for path in EXAMPLES:
        data = yaml.safe_load(path.read_text())
        assert data['status'] == 'planned'
        assert all(i['selection_status'] == 'planned' and not i['actual_executions'] for i in data['instances'])


def test_completed_record(completed):
    assert not findings(completed)


@pytest.mark.parametrize('field', ['forest_cover_lab', 'sentinel_monthly_forest_cover', 'lab_graph_revision'])
@pytest.mark.parametrize('value', [None, '', 'main', 'abc123'])
def test_missing_pins(completed, field, value):
    completed[1]['repos'][field] = value
    assert findings(completed)


@pytest.mark.parametrize('target', ['sha256', 'revision', 'loaded_harness', 'output_hashes', 'checks', 'output_refs', 'ended_utc'])
def test_missing_completion_provenance(completed, target):
    attempt = completed[1]['instances'][0]['actual_executions'][0]
    if target in {'sha256', 'revision'}:
        attempt['loaded_harness'][0][target] = None
    else:
        attempt.pop(target)
    assert findings(completed)


def test_all_captured_and_repository_loads_need_hashes(completed):
    attempt = completed[1]['instances'][0]['actual_executions'][0]
    for index in range(len(attempt['loaded_harness'])):
        data = copy.deepcopy(completed[1])
        data['instances'][0]['actual_executions'][0]['loaded_harness'][index]['sha256'] = None
        assert findings((completed[0], data))


@pytest.mark.parametrize('change', ['planned_round', 'no_attempt', 'not_used', 'missing_rules', 'selected_load', 'wrong_revision', 'duplicate_attempt', 'duplicate_instance', 'backward_time', 'output_hash', 'missing_check'])
def test_contradictions(completed, change):
    data = completed[1]
    instance = data['instances'][0]
    attempt = instance['actual_executions'][0]
    if change == 'planned_round': data['status'] = 'planned'
    elif change == 'no_attempt': instance['actual_executions'] = []
    elif change == 'not_used': instance['selection_status'] = 'not_used'
    elif change == 'missing_rules': attempt['loaded_harness'].pop(0)
    elif change == 'selected_load': attempt['loaded_harness'][0]['capture_status'] = 'selected'
    elif change == 'wrong_revision': attempt['loaded_harness'][0]['revision'] = 'd' * 40
    elif change == 'duplicate_attempt': instance['actual_executions'].append(copy.deepcopy(attempt))
    elif change == 'duplicate_instance': data['instances'].append(copy.deepcopy(instance))
    elif change == 'backward_time': attempt['ended_utc'] = '2026-10-20T10:00:00Z'
    elif change == 'output_hash': attempt['output_hashes']['synthetic.txt'] = 'bad'
    elif change == 'missing_check': attempt['checks'] = []
    assert findings(completed)


def test_private_instructions_are_explicit_limits(completed):
    attempt = completed[1]['instances'][0]['actual_executions'][0]
    attempt['loaded_harness'].append({'source': 'private-project', 'path_or_identifier': 'private-project-policy', 'revision': None, 'sha256': None, 'capture_status': 'not_captured'})
    assert not findings(completed)
    attempt['limitations'] = []
    assert findings(completed)


def test_review_requires_human_basis_and_decision(completed):
    data = completed[1]
    data['status'] = 'reviewed'
    assert findings(completed)
    data['human_review'] = {'status': 'needs_more_evidence', 'reviewer': 'synthetic test reviewer (not real approval)', 'decision': 'test only', 'basis': 'fixture assertions only'}
    assert not findings(completed)
    data['human_review']['basis'] = None
    assert findings(completed)


def test_local_role_requires_explicit_scope(planned):
    path, data = planned
    instance = data['instances'][0]
    instance['role'] = instance['assignment']
    assert findings(planned)
    instance['role_scope'] = 'round_only'
    assert not findings(planned)


@pytest.mark.parametrize('name', ['../outside.md', '/tmp/outside.md'])
def test_paths_cannot_escape_roots(planned, name):
    planned[1]['instances'][0]['assignment'] = name
    assert findings(planned)


def test_symlink_cannot_escape_round(planned, tmp_path):
    path, data = planned
    outside = tmp_path.parent / f'{tmp_path.name}-external.md'
    outside.write_text('fixture only')
    link = path.parent / 'linked.md'
    try:
        link.symlink_to(outside)
        data['instances'][0]['assignment'] = 'linked.md'
        assert findings(planned)
    finally:
        outside.unlink()


def test_research_and_downstream_paths_and_cli(planned, tmp_path):
    path, data = planned
    root = tmp_path / 'isolated-checkout'
    for relative in ('research/inquiries/q/rounds/r', 'reviews/investigation/rounds/r'):
        folder = root / relative
        folder.mkdir(parents=True)
        shutil.copytree(path.parent / 'assignments', folder / 'assignments')
        write(folder / 'round.yaml', data)
    assert len(list(discover(root))) == 2
    result = subprocess.run([sys.executable, str(LAB / 'agent_harness/scripts/validate_round.py'), '--root', str(root)], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    (root / 'reviews/investigation/rounds/r/round.yaml').write_text('not: valid')
    result = subprocess.run([sys.executable, str(LAB / 'agent_harness/scripts/validate_round.py'), '--root', str(root)], capture_output=True, text=True)
    assert result.returncode == 1


def test_downstream_completed_requires_downstream_rules(completed, tmp_path):
    path, data = completed
    folder = tmp_path / 'reviews/i/rounds/r'
    folder.mkdir(parents=True)
    shutil.copytree(path.parent / 'assignments', folder / 'assignments')
    record = (folder / 'round.yaml', data)
    assert any('sentinel-monthly-forest-cover:AGENTS.md' in e for e in findings(record))
    data['instances'][0]['actual_executions'][0]['loaded_harness'].append({'source': 'sentinel-monthly-forest-cover', 'path_or_identifier': 'AGENTS.md', 'revision': 'b' * 40, 'sha256': 'd' * 64, 'capture_status': 'captured'})
    assert not findings(record)


def test_invalid_yaml_and_missing_manifest_return_findings(tmp_path):
    path = tmp_path / 'round.yaml'
    assert check(path)
    path.write_text('schema_version: "1.0"\nschema_version: "1.0"\n')
    assert any('duplicate YAML key' in e for e in check(path))
    path.write_text('[')
    assert check(path)


@pytest.fixture
def version_11(completed):
    path, data = completed
    data['schema_version'] = '1.1'
    for instance in data['instances']:
        instance['delegation'] = {
            'mode': 'sequential_role', 'parent_instance_id': None,
            'question': 'Synthetic bounded question; not an execution',
            'output_contract': 'Synthetic artifact and documented checks',
            'permitted_writes': [],
            'budget': {'tool_call_limit': None, 'elapsed_seconds_limit': None, 'cost_usd_limit': None},
        }
        for attempt in instance['actual_executions']:
            attempt.update(
                runtime={'client_version': None, 'model_configuration': {}, 'context_mode': 'unknown', 'workspace_mode': 'unknown', 'permission_summary': None},
                handoffs=[], coordination_events=[],
                independence={'source_lineage_groups': [], 'conclusion_exposure': 'unknown', 'evidence_inspected': [], 'limitations': ['Synthetic unknown lineage; no independence claim']},
            )
    return path, data


def test_version_11_and_legacy_10(completed, version_11):
    assert not findings(version_11)
    old = yaml.safe_load(EXAMPLES[0].read_text())
    assert old['schema_version'] == '1.0'
    assert not check(EXAMPLES[0])


@pytest.mark.parametrize('field', ['runtime', 'handoffs', 'independence', 'coordination_events'])
def test_version_11_requires_capture_fields(version_11, field):
    version_11[1]['instances'][0]['actual_executions'][0].pop(field)
    assert findings(version_11)


def test_version_11_requires_delegation_contract(version_11):
    version_11[1]['instances'][0].pop('delegation')
    assert findings(version_11)


@pytest.mark.parametrize('parent', ['absent-instance', 'pub-01'])
def test_parent_reference_must_resolve_to_another_instance(version_11, parent):
    first = version_11[1]['instances'][0]
    first['delegation']['parent_instance_id'] = first['id'] if parent == 'pub-01' else parent
    assert findings(version_11)


def test_parent_cycles_rejected(version_11):
    first, second = version_11[1]['instances'][:2]
    first['delegation']['parent_instance_id'] = second['id']
    second['delegation']['parent_instance_id'] = first['id']
    assert any('cyclic delegation' in e for e in findings(version_11))


def test_native_subagent_requires_parent(version_11):
    first, second = version_11[1]['instances'][:2]
    first['actual_executions'] = []
    first['selection_status'] = 'planned'
    first['delegation']['mode'] = 'native_subagent'
    assert findings(version_11)
    first['delegation']['parent_instance_id'] = second['id']
    assert not findings(version_11)


def test_actual_native_subagent_requires_observed_parent(version_11):
    first, second = version_11[1]['instances'][:2]
    first['delegation'].update(mode='native_subagent', parent_instance_id=second['id'])
    assert any('observed parent attempt' in e for e in findings(version_11))


def test_version_11_preserves_optional_round_graph(version_11, tmp_path):
    source = LAB / 'agent_harness/examples/road-widening/round-0001/round.yaml'
    data = yaml.safe_load(source.read_text())
    shutil.copytree(source.parent / 'assignments', tmp_path / 'graph-assignments')
    data['schema_version'] = '1.1'
    for instance in data['instances']:
        instance['assignment'] = instance['assignment'].replace('assignments/', 'graph-assignments/')
        instance['delegation'] = copy.deepcopy(version_11[1]['instances'][0]['delegation'])
    assert not check(write(tmp_path / 'round.yaml', data))


def test_runtime_unknowns_need_limits(version_11):
    attempt = version_11[1]['instances'][0]['actual_executions'][0]
    attempt['limitations'] = []
    assert any('unknown runtime' in e for e in findings(version_11))


def test_unknown_independence_and_inspected_references(version_11):
    attempt = version_11[1]['instances'][0]['actual_executions'][0]
    disclosure = attempt['independence']
    disclosure['limitations'] = []
    assert findings(version_11)
    disclosure.update(source_lineage_groups=['synthetic-source-group'], conclusion_exposure='received', evidence_inspected=['synthetic-primary'])
    assert findings(version_11)
    attempt['source_refs'] = ['synthetic-primary']
    assert not findings(version_11)


@pytest.mark.parametrize('capture', ['selected', 'not_captured', 'missing_digest'])
def test_handoff_requires_capture_and_digest(version_11, capture):
    attempt = version_11[1]['instances'][0]['actual_executions'][0]
    artifact = {'source': 'round', 'path_or_identifier': 'synthetic-handoff', 'revision': None, 'sha256': 'd' * 64, 'capture_status': 'captured'}
    attempt['handoffs'] = [artifact]
    assert not findings(version_11)
    if capture == 'missing_digest':
        artifact['sha256'] = None
    else:
        artifact['capture_status'] = capture
    assert findings(version_11)


def test_coordination_artifact_requires_digest(version_11):
    attempt = version_11[1]['instances'][0]['actual_executions'][0]
    event = {'kind': 'reconciliation', 'detail': 'Synthetic disagreement retained', 'artifact': None}
    attempt['coordination_events'] = [event]
    assert not findings(version_11)
    event['artifact'] = {'source': 'round', 'path_or_identifier': 'synthetic-event', 'revision': None, 'sha256': None, 'capture_status': 'captured'}
    assert findings(version_11)
