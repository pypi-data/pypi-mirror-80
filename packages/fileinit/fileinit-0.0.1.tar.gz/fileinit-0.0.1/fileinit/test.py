
# ファイル初期化 [fileinit]
# 【動作確認 / 使用例】

import sys
from relpath import add_import_path
add_import_path("../")
from fileinit import fileinit

# ファイル初期化 [fileinit]
fileinit(
	"./test.txt",	# ファイル名
	overwrite = True,
	init_str = "Hello, World!!\n",
	encoding = "utf-8"
)
