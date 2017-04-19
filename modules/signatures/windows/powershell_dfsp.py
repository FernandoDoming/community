# Copyright (C) 2010-2015 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import shlex
import yara
import logging
import traceback

from lib.cuckoo.common.abstracts import Signature

log = logging.getLogger()

class PowershellDFSP(Signature):
    name = "powershell_dfsp"
    description = "Powershell Downloader DFSP detected"
    severity = 5
    categories = ["script", "dropper", "downloader", "malware"]
    authors = ["FDD", "Cuckoo Technologies"]
    minimum = "2.0"

    def on_complete(self):
        psempire_rule = """
        rule PowershellDFSP {
          meta:
            author = "FDD"
            description = "Rule for Powershell DFSP detection"

          strings:
            $Net = "new-object system.net.webclient" nocase
            $Download = "downloadfile(" nocase
            $Start = "Start-Process" nocase
            $Payload = /(https?|ftp):\/\/[^\s\/$.?#].[^\s"']*/

          condition:
            all of them
        }
        """
        for cmdline in self.get_command_lines():
            lower = cmdline.lower()

            if "powershell" not in lower:
                continue

            if "-enc" in lower or "-encodedcommand" in lower:
                script, args = None, shlex.split(cmdline)
                for idx, arg in enumerate(args):
                    if "-enc" not in arg.lower() and "-encodedcommand" not in arg.lower():
                        continue

                    try:
                        script = args[idx+1].decode("base64").decode("utf16")
                        rule = yara.compile(source=psempire_rule)
                        matches = rule.match(data=script)

                        if matches:
                            self.mark_ioc("Malware family", "Powershell Downloader DFSP")
                            for m in matches:
                                for string in m.strings:
                                    if string[1] == "$Payload":
                                        self.mark_ioc("Payload", string[2])
                            break
                    except Exception as e:
                        traceback.print_exc(e)
                        pass

        return self.has_marks()