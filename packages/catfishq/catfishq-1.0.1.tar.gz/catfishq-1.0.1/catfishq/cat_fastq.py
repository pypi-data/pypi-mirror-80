from __future__ import print_function

import os
import sys
import glob
import math
import argparse
import pysam
import logging

from pathlib import Path

LOOKUP = []

for q in range(100):
    LOOKUP.append(pow(10, -.1 * q))


def _compute_mean_qscore(scores):
    """ Returns the phred score corresponding to the mean of the probabilities
    associated with the phred scores provided.

    :param scores: Iterable of phred scores.

    :returns: Phred score corresponding to the average error rate, as
        estimated from the input phred scores.
    """
    if not scores:
        return 0.0
    sum_prob = 0.0
    for val in scores:
        sum_prob += LOOKUP[val]
    mean_prob = sum_prob / len(scores)
    return -10.0 * math.log10(mean_prob)


def parse_args(argv):
    """
    Commandline parser

    :param argv: Command line arguments
    :type argv: List
    """
    usage = "Cat long lists of FASTQ files"
    parser = argparse.ArgumentParser(
        description=usage,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-l", "--log",
                        dest="log",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR',
                                 'CRITICAL',
                                 'debug', 'info', 'warning', 'error',
                                 'critical'],
                        default="INFO",
                        help="Print debug information")
    parser.add_argument("-o", "--output",
                        dest="OUT",
                        type=str,
                        default="/dev/stdout",
                        help="Output file. (default: stdout)")
    parser.add_argument("--min-length",
                        dest="MIN_LEN",
                        type=int,
                        default=0,
                        help="Minimum read length")
    parser.add_argument("--min-qscore",
                        dest="MIN_QSCORE",
                        type=int,
                        default=0,
                        help="Minimum q-score")
    parser.add_argument("--max_n",
                        dest="MAX_N",
                        type=int,
                        default=0,
                        help="Only output <int> reads")
    parser.add_argument("-r",
                        "--recursive",
                        dest="RECURSIVE",
                        action='store_true',
                        help="Search folders recursively")

    parser.add_argument("FASTQ",
                        nargs="+",
                        type=str,
                        help="FASTQ files or folders containing FASTQ files")

    args = parser.parse_args(argv)

    return args


def find_file_in_folder(folder, recursive=True, patterns=["*.fastq", "*.fastq.gz", '*.fasta', '*.fasta.gz', '*.fa', '*.fa.gz', '*.fq', '*.fq.gz']):
    if os.path.isfile(folder):
        return folder
    files = []

    glob = Path(folder).glob
    if recursive:
        glob = Path(folder).rglob

    for pattern in patterns:
        for file in glob(pattern):
           files.append(file)

    if len(files) == 0:
        logging.warning("Could not find {} files in {}".format(pattern, folder))
    return files


def parse_fastqs(filename, min_len=0, min_qscore=0):
    with pysam.FastxFile(filename) as fh:
        for entry in fh:
            if min_len and len(entry.sequence) < min_len:
                continue
            if min_qscore and _compute_mean_qscore(entry.get_quality_array()) < min_qscore:
                continue
            if entry.comment:
                entry.comment = "CO:Z:{}".format(entry.comment)

            yield entry


def get_file_names(path, recursive):
    if os.path.exists(path):
        filenames = [path]
        if os.path.isdir(path):
            logging.debug("Searching {} for FASTQ files".format(path))
            filenames = find_file_in_folder(path, recursive=recursive)
    else:
        logging.warning("Could not find {}".format(path))

    return filenames


def format_fq(paths, out_filename, min_len=0, min_qscore=0, max_n=0, recursive=False):
    """
    Concatenate FASTQ files

    :param paths: Input FASTQ files or folders containing FASTQ files
    :param out_filename: Output FASTQ file
    :return: None
    """

    n = 0
    with open(out_filename, mode='w') as fout:
        for path in paths:
            filenames = get_file_names(path, recursive)
            logging.debug("Found {} files".format(len(filenames)))
            for filename in filenames:
                for entry in parse_fastqs(filename, min_len=min_len, min_qscore=min_qscore):
                    fout.write(str(entry) + "\n")
                    n += 1
                    if max_n and n >= max_n:
                        return


def main(argv=sys.argv[1:]):
    """
    Basic command line interface to telemap.

    :param argv: Command line arguments
    :type argv: list
    :return: None
    :rtype: NoneType
    """
    args = parse_args(argv=argv)

    numeric_level = getattr(logging, args.log.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.log.upper())
    logging.basicConfig(level=numeric_level, format='%(message)s')

    format_fq(args.FASTQ, args.OUT, min_len=args.MIN_LEN, min_qscore=args.MIN_QSCORE, max_n=args.MAX_N, recursive=args.RECURSIVE)


if __name__ == '__main__':
    main()
