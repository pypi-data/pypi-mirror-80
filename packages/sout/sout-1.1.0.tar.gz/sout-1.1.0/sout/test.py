
# 巨大オブジェクトのデバッグ表示 [sout]
# 【動作確認 / 使用例】

import sys
from relpath import add_import_path
add_import_path("../")
# 巨大オブジェクトのデバッグ表示 [sout]
from sout import sout

large_obj = [{j:"foo" for j in range(i+2)}
	for i in range(1000)]
sout(large_obj)
