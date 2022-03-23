# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/validation.py
#
#   Some simple input validation and error handling
#   in a later refactor we might use something like Marshmallow
#   but for this simple case, this is good enough
#

import re
from flask import redirect, url_for, flash
from viaa.configuration import ConfigParser
from viaa.observability import logging
from markupsafe import escape

logger = logging.get_logger(__name__, config=ConfigParser())


def pid_error(pid, msg):
    logger.info('search_media', data={'error': msg})
    flash(msg)
    return redirect(
        url_for(
            '.search_media',
            pid=escape(pid),
        )
    )


def upload_error(template_params, error_msg):
    logger.info('upload', data={'error': error_msg})
    flash(error_msg)
    return redirect(
        url_for(
            '.get_upload',
            pid=escape(template_params['pid']),
            department=escape(template_params['department']),
        )
    )


def validate_input(pid, department):
    # we might use Marshmallow in future, for now this
    # is sufficient
    if pid and len(pid) > 120:
        return "Gegeven PID te lang"

    if department and len(department) > 120:
        return "Gegeven department te lang"

    if not re.search('^[A-Za-z0-9_]+$', pid):
        return "PID formaat foutief"

    if not re.search('^[A-Za-z0-9_ ]+$', department):
        return "Department formaat foutief"

    return None


def validate_upload(template_params, request_files):
    if not template_params['pid']:
        return 'Foutieve pid', None

    if 'subtitle_file' not in request_files:
        return 'Geen ondertitels bestand', None

    uploaded_file = request_files['subtitle_file']
    if uploaded_file.filename == '':
        return 'Geen ondertitels bestand geselecteerd', None

    return None, uploaded_file


def validate_conversion(template_params):
    if not template_params.get('subtitle_file'):
        return 'Ondertitels moeten in SRT formaat'

    if not template_params.get('vtt_file'):
        return 'Kon niet converteren naar webvtt formaat'
