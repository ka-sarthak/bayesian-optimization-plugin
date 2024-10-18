import os.path

from nomad.client import normalize_all, parse


def test_schema_package():
    test_file = os.path.join('tests', 'data', 'test.archive.yaml')
    entry_archive = parse(test_file)[0]
    normalize_all(entry_archive)
    assert entry_archive.data.analysis_type == 'Bayesian Optimization'


if __name__ == '__main__':
    test_schema_package()
