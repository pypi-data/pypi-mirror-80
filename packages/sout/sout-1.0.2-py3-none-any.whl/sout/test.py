
# 巨大オブジェクトのデバッグ表示 [sout]
# 【動作確認 / 使用例】

import sys
from relpath import rel2abs
sys.path.append(rel2abs("../"))
# 巨大オブジェクトのデバッグ表示 [sout]
from sout import sout

large_obj = [{j:"foo" for j in range(i+2)}
	for i in range(1000)]
sout(large_obj)
