
# local log (globalスコープを汚さないログツール) [llog]
# 【動作確認 / 使用例】

import sys
from sout import sout
from relpath import add_import_path
add_import_path("../")
from llog import llog

# 出力確認
sout(llog())
