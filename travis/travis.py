# Copyright (c) 2012-2017 DreamWorks Animation LLC
#
# All rights reserved. This software is distributed under the
# Mozilla Public License 2.0 ( http://www.mozilla.org/MPL/2.0/ )
#
# Redistributions of source code must retain the above copyright
# and license notice and the following restrictions and disclaimer.
#
# *     Neither the name of DreamWorks Animation nor the names of
# its contributors may be used to endorse or promote products derived
# from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# IN NO EVENT SHALL THE COPYRIGHT HOLDERS' AND CONTRIBUTORS' AGGREGATE
# LIABILITY FOR ALL CLAIMS REGARDLESS OF THEIR BASIS EXCEED US$250.00.
#
# Python script to download the latest Houdini production builds
#
# Author: Dan Bailey

import requests
import sys
import re
import shutil
from sidefx_api import service


# this argument is for the major.minor version of Houdini to download (such as 15.0, 15.5, 16.0)
version = sys.argv[1]

if not re.match('[0-9][0-9]\.[0-9]$', version):
    raise IOError('Invalid Houdini Version "%s", expecting in the form "major.minor" such as "16.0"' % version)

sidefx_client_id = sys.argv[2]
sidefx_secret_key = sys.argv[3]

sidefx_service = service(
    access_token_url='https://www.sidefx.com/oauth2/application_token',
    client_id=sidefx_client_id,
    client_secret_key=sidefx_secret_key,
    endpoint_url='https://www.sidefx.com/api/',
)


release_list = service.download.get_daily_builds_list(
    product='houdini', version=version, platform='linux')
latest_release = service.download.get_daily_builds_download(
    product='houdini', version=version, build=release_list[0]['build'], platform='linux')

# Download the file
local_filename = latest_release['filename']
r = requests.get(latest_release['download_url'], stream=True)
if r.status_code == 200:
    with open(local_filename, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
else:
    raise Exception('Error downloading file!')
