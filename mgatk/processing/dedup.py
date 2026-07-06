import os
import subprocess

import pysam


def dedup_with_picard(script_dir, temp_bam, output_bam, rmlog, max_javamem, remove_duplicates, umi_tag=""):
    """
    Either run Picard MarkDuplicates (temp_bam -> output_bam, assumed already
    sorted+indexed) or just promote temp_bam to output_bam unchanged, then
    index output_bam. umi_tag, if non-empty, is passed as Picard's BARCODE_TAG
    so duplicates are only merged within the same UMI/cell barcode.
    """
    if remove_duplicates == "True":
        picard_jar = os.path.join(script_dir, "bin", "picard.jar")
        cmd = [
            "java", "-Xmx" + max_javamem, "-jar", picard_jar, "MarkDuplicates",
            "I=" + temp_bam, "O=" + output_bam, "M=" + rmlog,
            "REMOVE_DUPLICATES=true", "ASSUME_SORTED=true",
            "VALIDATION_STRINGENCY=SILENT", "QUIET=true", "VERBOSITY=ERROR",
            "USE_JDK_DEFLATER=true", "USE_JDK_INFLATER=true",
        ]
        if umi_tag:
            cmd.append("BARCODE_TAG=" + umi_tag)
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        os.replace(temp_bam, output_bam)
        os.remove(temp_bam + ".bai")
    pysam.index(output_bam)
