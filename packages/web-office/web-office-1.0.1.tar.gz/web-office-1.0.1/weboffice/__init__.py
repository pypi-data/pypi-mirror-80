# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import sys
from urllib.parse import quote
import webbrowser
from progresslib import Pulsate

from weboffice.githosting import GitLab


@Pulsate
def main(viewer_url):
    hosting = GitLab()
    file_urls = hosting.push(sys.argv[1:])

    for u in file_urls:
        u = viewer_url % quote(u)
        print(u)
        webbrowser.open(u)


def msoo():
    main(viewer_url="http://view.officeapps.live.com/op/view.aspx?src=%s")


def gdocs():
    main(viewer_url="http://docs.google.com/viewer?url=%s")


if __name__ == "__main__":
    sys.argv.append("/home/pacholik/scores/Cry me a river.doc")
    msoo()
