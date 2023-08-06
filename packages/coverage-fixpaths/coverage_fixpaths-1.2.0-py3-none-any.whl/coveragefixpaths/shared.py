import logging
import os
import xml.etree.ElementTree as ElementTree
from typing import Optional


class CoverageFixPathsError(Exception):
    pass


def fix_filenames(filename_finder, updaters):

    def _fix_filenames(coverage_report: str, source_dir: str, out_file=None, logger=None):
        if logger is None:
            logger = logging

        # Get data from the coverage report.
        tree = parse_report(coverage_report)
        xml_filenames = filename_finder(tree)
        l = len(xml_filenames)
        if l > 1:
            xml_prefix = os.path.commonpath(xml_filenames)
        elif l == 1:
            xml_prefix = os.path.dirname(next(iter(xml_filenames)))
        else:
            raise CoverageFixPathsError('No files in report')
        logger.debug(f"Found {len(xml_filenames)} filenames in report.")
        logger.debug(f"Common prefix for filenames in report is '{xml_prefix}'.")

        # Find the shallowest location of the files in the coverage report on the actual file system.
        new_prefix = find_first_matching_prefix(xml_filenames, xml_prefix, source_dir, logger)
        if new_prefix is None:
            raise CoverageFixPathsError(f'Cannot find all coverage report files in the directory {source_dir}')
        logger.info(f"Replacing prefix '{xml_prefix}' with '{new_prefix}'.")

        # Update the XML tree.
        for updater in updaters:
            updater(tree, source_dir, new_prefix, xml_prefix, logger)

        # Write out the updated coverage file.
        if out_file:
            target = out_file
        else:
            target = coverage_report
        tree.write(target)
        logger.debug(f"Done writing out new coverage report to {target}.")

    return _fix_filenames


def parse_report(coverage_report_path: str) -> ElementTree.ElementTree:
    try:
        tree = ElementTree.parse(coverage_report_path)
    except FileNotFoundError:
        raise CoverageFixPathsError(f"Cannot find coverage report {coverage_report_path}.")
    except IsADirectoryError:
        raise CoverageFixPathsError(f"Given coverage report {coverage_report_path} is a directory.")
    except ElementTree.ParseError as e:
        raise CoverageFixPathsError(f"Error parsing coverage report (error code {e.code}).")
    return tree


def find_first_matching_prefix(xml_filenames, xml_prefix, source_dir, logger) -> Optional[str]:
    # Distill a bit of information from the XML filenames.
    xml_basenames = {os.path.basename(f) for f in xml_filenames}
    xml_root_files = set()
    xml_root_folders = set()
    xml_rel_filenames = set()
    for filename in xml_filenames:
        relative_filename = os.path.relpath(filename, start=xml_prefix)
        xml_rel_filenames.add(relative_filename)
        *folders, file = relative_filename.split(os.sep)
        if not folders:
            xml_root_files.add(file)
        else:
            xml_root_folders.add(folders[0])

    # Parse data from the file system.
    source_filenames = set()
    source_paths = []
    for path, subdirs, files in os.walk(source_dir):
        rel_path = os.path.relpath(path, start=source_dir)
        if xml_root_files.issubset(set(files)) and xml_root_folders.issubset(set(subdirs)):
            source_paths.append(rel_path)
        for file in files:
            if file in xml_basenames:
                filename = normjoin(rel_path, file)
                source_filenames.add(filename)
    logger.debug(f"Found {len(source_paths)} possible matching source directories.")
    logger.debug(f"Found {len(source_filenames)} file base names in source dir that match those in report.")

    # Attempt to find the first / shallowest matching prefix (breadth-first).
    first_prefix = None
    source_paths = sorted(source_paths, key=lambda path: (path.count(os.sep), path.startswith('.'), path.lower()))
    for source_path in source_paths:
        is_match = True
        for xml_rel_filename in xml_rel_filenames:
            if normjoin(source_path, xml_rel_filename) not in source_filenames:
                is_match = False
                break
        if is_match:
            first_prefix = source_path
            break

    return first_prefix


def normjoin(*args):
    return os.path.normpath(os.path.join(*args))
