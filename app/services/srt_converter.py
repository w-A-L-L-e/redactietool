# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/srt_converter.py
#
#   Uses webvtt wrappers to do string with
#   subtitles in srt format into webvtt format
#

from webvtt.parsers import SRTParser
from webvtt.writers import WebVTTWriter
from webvtt.errors import MalformedFileError


class SRTStringParser(SRTParser):
    """
    SRT parser that works on strings
    """

    def readstr(self, srt_string):
        """Reads the captions as string."""
        lines = srt_string.splitlines()
        self._validate(lines)
        self._parse(lines)

        return self


def convert_srt(srt_content):
    try:
        parser = SRTStringParser().readstr(srt_content)
        captions = parser.captions
        webvtt_str = WebVTTWriter().webvtt_content(captions)

        return webvtt_str
    except MalformedFileError as e:
        print("convert_srt: error", e)
        return ""
