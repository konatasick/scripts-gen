#!/usr/bin/python
#coding=utf8


from __future__ import with_statement
from itertools import izip
__author__ = u'Ziyuan'


import re
import os
import shutil
import sys
import logging
import itertools
from string import Template
import argparse
from io import open


_logger = logging.getLogger(u'ScriptsGen')
_logger.setLevel(logging.INFO)
_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_logger.addHandler(_console)


class ScriptsGen(object):

    def __init__(self, template_file_name, script_file_name_format,
                 open_token=u'<%', close_token=u'%>',
                 comment_token=u'###', **kwargs):
        self.__file_format = script_file_name_format
        try:
            with open(template_file_name, u'r') as template_file:
                content = template_file.read()
                content = re.sub(ur'(?:\r?\n)?%s.*' % comment_token, u'', content)
                content = re.sub(ur'\$', u'$$', content)
                self.__template = Template(re.sub(u'{open_token}(.+?){close_token}'.format(open_token=open_token,
                                                                                          close_token=close_token),
                                                  ur'${\1}', content))
        except FileNotFoundError:
            _logger.error(u'Cannot find template file \'%s\'.' % template_file_name)
            sys.exit(1)

        self.__param_dict = kwargs
        for (key, value) in self.__param_dict.items():
            if isinstance(value, str):
                try:
                    with open(value, u'r') as param_file:
                        self.__param_dict[key] = param_file.read().splitlines()
                except FileNotFoundError:
                    _logger.error(u'Cannot find parameter file \'%s\' for parameter \'%s\'.' % (value, key))
                    sys.exit(1)

    def run(self, save_to_folder, delete_first=False):
        if not os.path.exists(save_to_folder):
            os.mkdir(save_to_folder)
        else:
            if delete_first is True:
                _logger.warning(u'Deleting contents in \'%s\'...' % save_to_folder)
                for file in os.listdir(save_to_folder):
                    file_full_path = os.path.join(save_to_folder, file)
                    if os.path.isfile(file_full_path):
                        os.remove(file_full_path)
                    elif os.path.isdir(file_full_path):
                        shutil.rmtree(file_full_path)
                _logger.warning(u'Done.')

        param_keys = self.__param_dict.keys()
        param_values = self.__param_dict.values()
        combinations = itertools.product(*param_values)

        _logger.info(u'Creating scripts in \'%s\'...' % save_to_folder)
        for params in combinations:
            local_param_dict = dict(izip(param_keys, params))
            try:
                script_file_name = self.__file_format.format(**local_param_dict)
                if script_file_name == u"":
                    _logger.error(u'Cannot create script file with an empty name.')
                try:
                    script_full_path = os.path.join(save_to_folder, script_file_name)
                    with open(script_full_path, u'w') as script_file:
                        local_param_dict[u'__FULL_PATH__'] = script_full_path
                        local_param_dict[u'__DST_FOLDER__'] = save_to_folder[:-1] if save_to_folder.endswith(u'/') or save_to_folder.endswith(u'\\') else save_to_folder
                        local_param_dict[u'__FILE__'] = script_file_name
                        (file_no_ext, ext) = os.path.splitext(script_file_name)
                        local_param_dict[u'__FILE_NO_EXT__'] = file_no_ext
                        local_param_dict[u'__EXT__'] = ext
                        script = self.__template.substitute(local_param_dict)
                        script_file.write(script)
                    if os.name == u'posix':
                        os.system(u'chmod +x ' + script_full_path)
                except OSError, e:
                    _logger.error(u'Cannot create script %s.' % script_file_name)
            except ValueError, e:
                _logger.error(u'Cannot parse format string: %s .' % unicode(e))
                sys.exit(1)
            except KeyError, e:
                _logger.error(u'Format string needs the value of parameter %s.' % unicode(e))
                sys.exit(1)
            except AttributeError:
                _logger.error(u'Cannot parse format string %s.' % self.__file_format)
                sys.exit(1)

        _logger.info(u'Done.')


def main():
    parser = argparse.ArgumentParser(description=u'Generate scripts from a template, by enumerating combinations of parameters.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser._optionals.title = u'arguments'
    parser.add_argument(u'--template', metavar=u'FILE', help=u'The location of the template file.', required=True, default=argparse.SUPPRESS)
    parser.add_argument(u'--save-to', metavar=u'FOLDER', help=u'The destination folder for the scripts.', required=True, default=argparse.SUPPRESS)
    parser.add_argument(u'--param', metavar=u'DICT', help=u"""
    All the parameters with their values as a dictionary,
    where a value can be a list, or a file name that refers to a file containing one parameter value per line.
    See Python\'s dictionary literals (http://docs.python.org/3/reference/expressions.html#dictionary-displays).
    """, required=True, default=argparse.SUPPRESS)
    parser.add_argument(u'--format', metavar=u'STRING', help=u"""
    The format string for the file names of the scripts.
    See Python\'s format string syntax (http://docs.python.org/3/library/string.html#format-string-syntax).
    """,required=True, default=argparse.SUPPRESS)
    parser.add_argument(u'--open', metavar=u'TOKEN', help=u'The token that indicates the start of a template identifier.', default=u'<%')
    parser.add_argument(u'--close', metavar=u'TOKEN', help=u'The token that indicates the end of a template identifier.', default=u'%>')
    parser.add_argument(u'--comment', metavar=u'TOKEN', help=u"""
    The token placed in the template file that treats the rest of the line,
    which will be removed in the scripts, as a comment.
    """, default=u'###')
    parser.add_argument(u'--delete', action=u'store_true', help=u'Delete the contents in the destination folder before creation.', default=False)
    args = parser.parse_args()

    try:
        param_dict = eval(args.param)
    except SyntaxError:
        _logger.error(u'Cannot parse the parameter dictionary %s.' % args.param)
        sys.exit(2)
    scripts_gen = ScriptsGen(template_file_name=args.template,
                             script_file_name_format=args.format,
                             open_token=args.open,
                             close_token=args.close,
                             comment_token=args.comment,
                             **param_dict)

    scripts_gen.run(save_to_folder=args.save_to, delete_first=args.delete)

if __name__ == u"__main__":
    main()

