# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  tests/test_srt_converter.py
#

from app.services.srt_converter import convert_srt

TEST_SRT = """1
00:00:01,000 --> 00:00:03,023
Eerste subtitle test

2
00:00:03,676 --> 00:00:05,930
<i>Italic werkt ook</i>

3
00:00:06,972 --> 00:50:16,350
Gewone tekst hier 50 minuten lang!


"""

TEST_VTT_OUTPUT = """WEBVTT

00:00:01.000 --> 00:00:03.023
Eerste subtitle test

00:00:03.676 --> 00:00:05.930
<i>Italic werkt ook</i>

00:00:06.972 --> 00:50:16.350
Gewone tekst hier 50 minuten lang!"""


def test_srt_string_conversion():
    assert convert_srt(TEST_SRT) == TEST_VTT_OUTPUT
