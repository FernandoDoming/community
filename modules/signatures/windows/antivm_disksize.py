# Copyright (C) 2016 Kevin Ross
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class AntiVMDiskSize(Signature):
    name = "antivm_disk_size"
    description = "Queries the disk size which could be used to detect virtual machine with small fixed size or dynamic allocation"
    severity = 2
    categories = ["anti-vm"]
    authors = ["Kevin Ross"]
    minimum = "2.0"
    evented = True

    filter_apinames = set(["GetDiskFreeSpaceExW","GetDiskFreeSpaceExW"])

    whitelistprocs = [
        "iexplore.exe",
        "firefox.exe",
        "chrome.exe",
        "safari.exe"
    ]

    def on_call(self, call, process):
        if process["process_name"].lower() not in self.whitelistprocs:
            self.mark_call()

    def on_complete(self):
        return self.has_marks()
