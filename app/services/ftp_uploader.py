#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @Author: Walter Schreppers
#
#  app/ftp_uploader.py
#
#   FTP upload subtitle file and sidecar xml files.
#   as temporary workaround to get this working until
#   mh-api v2 solution is available.
#

import os
from ftplib import FTP, error_perm, error_temp
import socket
import logging

logger = logging.getLogger(__name__)


class FtpUploader:
    FTP_SERVER = os.environ.get(
        'FTP_SERVER',
        'ftp.localhost'
    )
    FTP_USER = os.environ.get('FTP_USER', 'anonymous')
    FTP_PASS = os.environ.get('FTP_PASS', '')
    FTP_DIR = os.environ.get('FTP_DIR', '/FTP_DIR/')

    def ftp_client(self, server):
        return FTP(server)

    def upload_subtitles(self, upload_folder, metadata, tp):
        try:
            # sends srt_file and xml_file to mediahaven
            srt_path = os.path.join(upload_folder, tp['srt_file'])
            xml_path = os.path.join(upload_folder, tp['xml_file'])

            logger.info(
                f"Uploading to {self.FTP_SERVER} in folder #{self.FTP_DIR}")

            ftp = self.ftp_client(self.FTP_SERVER)
            ftp.login(self.FTP_USER, self.FTP_PASS)

            # change to correct ftp dir
            ftp.cwd(self.FTP_DIR)

            # upload srt file
            srt_result = ftp.storbinary(
                f"STOR {tp['srt_file']}",
                fp=open(srt_path, 'rb')
            )

            # upload xml sidecar file
            xml_result = ftp.storbinary(
                f"STOR {tp['xml_file']}",
                fp=open(xml_path, 'rb')
            )

            return {
                'srt_ftp_response': srt_result,
                'xml_ftp_response': xml_result
            }

        except error_temp as msg:
            print(f"FTP error: {msg}", flush=True)
            return {'ftp_error': str(msg)}

        except error_perm as msg:
            print(f"FTP error: {msg}", flush=True)
            return {'ftp_error': str(msg)}

        except (socket.error, socket.gaierror):
            print('FTP host error "{}"'.format(self.FTP_SERVER), flush=True)
            return {
                'ftp_error': f"FTP connect error, could not connect to {self.FTP_SERVER}"
            }
