#!/usr/bin/env python

""" MultiQC config module. Holds a single copy of
config variables to be used across all other modules """

from collections import OrderedDict
from datetime import datetime
import inspect
import os
import pkg_resources
import random
import sys
import yaml

import biobitbot
from biobitbot import logger

# Constants
IBOT_DIR = os.path.dirname(os.path.realpath(inspect.getfile(biobitbot)))

#######################
# Main Config Variables
#######################
title = None
prepend_dirs = False
modules_dir = os.path.join(IBOT_DIR, 'modules')
creation_date = datetime.now().strftime("%Y-%m-%d, %H:%m")
working_dir = os.getcwd()
analysis_dir = [os.getcwd()]
output_dir = os.path.realpath(os.getcwd())
output_fn_name = 'biobitbot_report.html'
data_dir_name = 'biobitbot_data'
make_data_dir = True
force = False
zip_data_dir = False
plots_force_flat = False
plots_force_interactive = False
plots_flat_numseries = 100
genstats_beeswarm_numseries = 50
data_format = 'tsv'
data_format_extensions = {'tsv': 'txt', 'json': 'json', 'yaml': 'yaml'}
fn_clean_exts = [ '.gz', '.fastq', '.fq', '.bam', '.sam', '.sra', '_tophat', '_star_aligned', '_fastqc', '.hicup', '.counts', '_counts', '.txt' ]
fn_ignore_files = ['.DS_Store', '*.bam', '*.sam', '*.fq.gz', '*.fastq.gz', '*.fq', '*.fastq', '*.gtf', '*.bed', '*.vcf', '*.txt.gz']
report_id = 'mqc_report_{}'.format(''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 20)))
no_version_check = False
num_datasets_plot_limit = 50
log_filesize_limit = 1000*1000*1000
report_readerrors = False

#######################
# Module fn search patterns
#######################
# Load here so that they can be overwritten by user configs
searchp_fn = os.path.join( IBOT_DIR, 'utils', 'search_patterns.yaml')
with open(searchp_fn) as f:
    sp = yaml.load(f)

#######################
# Available modules
#######################
# Modules must be listed in setup.py under entry_points['multiqc.modules.v1']
# We load them here so that they can be overwritten by a config file if desired.

# Order that modules should appear in report. Try to list in order of analysis,
# eg. FastQC is usually the first step, so should be last in this list.
# module_order = [
#     # Post-alignment analysis results
#     'csv_table',
#     'snpeff', 'qualimap', 'featureCounts', 'methylQA', 'rseqc',
#     'picard', 'preseq', 'samblaster', 'samtools',
#     # Alignment tool stats
#     'bismark', 'hicup', 'star', 'tophat', 'bowtie2', 'bowtie1',
#     # Pre-alignment QC
#     'cutadapt', 'skewer', 'fastq_screen', 'fastqc',
# ]

# Get all modules, including those from other extension packages
all_avail_analysis_types = {}
for entry_point in pkg_resources.iter_entry_points('biobitbot.analyses.v1'):
    nicename = str(entry_point).split('=')[0].strip()
    all_avail_analysis_types[nicename] = entry_point
    print all_avail_analysis_types



#######################
# Available templates
#######################
# Templates must be listed in setup.py under entry_points['multiqc.templates.v1']

# Get all templates, including those from other extension packages
avail_templates = {}
for entry_point in pkg_resources.iter_entry_points('biobitbot.templates.v1'):
    nicename = str(entry_point).split('=')[0].strip()
    avail_templates[nicename] = entry_point

# Which template to use by default?
template = 'default'

#######################
# Check we have modules & templates
#######################
# Check that we were able to find some modules and templates
# If not, package probably hasn't been installed properly.
# Need to do this before click, else will throw cryptic error
# Note: Can't use logger here, not yet installed.
if len(all_avail_analysis_types) == 0 or len(avail_templates) == 0:
    if len(all_avail_analysis_types) == 0:
        print("Error - No BioBitBot analyses found.")
    if len(avail_templates) == 0:
        print("Error - No MultiQC templates found.")
    print("Could not load BioBitBot - has it been installed?")
    sys.exit(1)


# Load user config in a def. This is called by the main script after initialisation
# This allows the plugin_hooks.mqc_trigger('config_loaded') hook to fire before the
# defaults are overwritten.
# def mqc_load_userconfig():
#     """ Overwrite config defaults with user config files """
#     # Load and parse installation config file if we find it
#     mqc_load_config(os.path.join( os.path.dirname(IBOT_DIR), 'multiqc_config.yaml'))

#     # Load and parse a user config file if we find it
#     mqc_load_config(os.path.expanduser('~/.multiqc_config.yaml'))
    
#     # Load and parse a config file in this working directory if we find it
#     mqc_load_config('.multiqc_config.yaml')

# def mqc_load_config(yaml_config):
#     """ Load and parse a config file if we find it """
#     try:
#         with open(yaml_config) as f:
#             new_config = yaml.load(f)
#             logger.debug("Loading config settings from: {}".format(yaml_config))
#             for c, v in new_config.items():
#                 if c == 'sp':
#                     # Merge filename patterns instead of replacing
#                     sp.extend(v)
#                     logger.debug("Added to filename patterns: {}".format(sp))
#                 if c == 'extra_fn_clean_exts':
#                     # Merge filename cleaning patterns instead of replacing
#                     fn_clean_exts.extend(v)
#                     logger.debug("Added to filename clean extensions. Now looking for: {}".format(fn_clean_exts))
#                 else:
#                     logger.debug("New config '{}': {}".format(c, v))
#                     globals()[c] = v
#     except (IOError, AttributeError) as e:
#         logger.debug("No MultiQC user config found: {}".format(yaml_config))
#         logger.debug("Config error: {}".format(e))

# These config vars are imported by all modules and can be updated by anything.
# The main launcher (scripts/multiqc) overwrites some of these variables
# with what has been given to it on the command line.
