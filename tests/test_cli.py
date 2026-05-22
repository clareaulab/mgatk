import pytest
from click.testing import CliRunner
from mgatk import cli
from mgatk import __version__
from mgatk.deletioncalling import clidel, clifind
from hashlib import md5


def file_checksums_equal(file1, file2):
    with open(file1) as f:
        checksum1 = md5(f.read()).hexdigest()
    with open(file2) as f:
        checksum2 = md5(f.read()).hexdigest()
    return checksum1==checksum2 


def test_check():
	runner = CliRunner()
	result = runner.invoke(cli.main, ['check', '-i', 'intput', '-o', 'output', '-n', 'name'])
	print(result.output)
	#assert file_checksums_equal('p.s3_1.trim.fastq', 'correct_output/p.s3_1.trim.fastq')


@pytest.mark.parametrize(
	('command', 'prog_name'),
	[
		(cli.main, 'mgatk'),
		(clidel.main, 'mgatk-del'),
		(clifind.main, 'mgatk-del-find'),
	],
)
def test_version_options(command, prog_name):
	runner = CliRunner()
	result = runner.invoke(command, ['--version'])

	assert result.exit_code == 0
	assert prog_name in result.output
	assert __version__ in result.output
