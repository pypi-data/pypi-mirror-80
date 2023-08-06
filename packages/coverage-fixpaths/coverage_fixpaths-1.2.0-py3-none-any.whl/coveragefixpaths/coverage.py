import os
import xml.etree.ElementTree as ElementTree

from .shared import fix_filenames, normjoin


def fix_coverage_filenames(*args, **kwargs):
    fix_filenames(
        filename_finder, [update_report_filenames, update_sources_tags]
    )(*args, **kwargs)

def filename_finder(tree):
    classes = tree.findall('./packages/package/classes/class[@filename]')
    return {c.get('filename') for c in classes}

def update_report_filenames(tree, source_dir, new_prefix, old_prefix, logger):
    classes = tree.findall('./packages/package/classes/class[@filename]')
    for c in classes:
        old_filename = c.get('filename')
        new_filename = normjoin(
            new_prefix,
            os.path.relpath(old_filename, start=old_prefix)
        )
        c.set('filename', new_filename)

def update_sources_tags(tree, source_dir, new_prefix, old_prefix, logger):
    sources = tree.find('./sources')
    for source in list(iter(sources)):
        logger.debug(f"Removing source path {source.text} from report.")
        sources.remove(source)
    abs_source_path = os.path.abspath(source_dir)
    logger.debug(f"Adding source path {abs_source_path} to report.")
    source_element = ElementTree.Element('source')
    source_element.text = abs_source_path
    sources.append(source_element)
