import gzip
from pathlib import Path

from mgatk.mgatkHelp import file_len, split_barcodes_file


def test_file_len_reads_gzipped_barcode_files(tmp_path):
    barcodes = tmp_path / "barcodes.tsv.gz"
    with gzip.open(barcodes, "wt") as handle:
        handle.write("AAAC\nGGGT\n")

    assert file_len(str(barcodes)) == 2


def test_split_barcodes_file_decompresses_gzip_without_splitting(tmp_path):
    barcodes = tmp_path / "barcodes.tsv.gz"
    with gzip.open(barcodes, "wt") as handle:
        handle.write("AAAC\nGGGT\n")

    split_files = split_barcodes_file(str(barcodes), 0, str(tmp_path / "out"))

    assert len(split_files) == 1
    assert Path(split_files[0]).read_text() == "AAAC\nGGGT\n"


def test_split_barcodes_file_splits_gzipped_barcodes(tmp_path):
    barcodes = tmp_path / "barcodes.tsv.gz"
    with gzip.open(barcodes, "wt") as handle:
        handle.write("AAAC\nGGGT\nTTTA\n")

    split_files = split_barcodes_file(str(barcodes), 2, str(tmp_path / "out"))

    assert [Path(filename).read_text() for filename in split_files] == [
        "AAAC\nGGGT\n",
        "TTTA\n",
    ]
