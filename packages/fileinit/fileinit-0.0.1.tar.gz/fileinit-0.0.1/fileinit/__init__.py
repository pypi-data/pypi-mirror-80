
# ファイル初期化 [fileinit]

import os
import sys

# ファイルを作成する必要性の判断
def judge_init(overwrite, exists_flag):
	if overwrite is True:
		return True
	elif overwrite is False:
		return (not exists_flag)
	else:
		raise Exception("invalid value in overwrite (%s)"%str(overwrite))

# ファイル初期化 [fileinit]
def fileinit(
	filename,
	overwrite,
	init_str = "",
	encoding = "utf-8"
):
	# ファイルを作成する必要性の判断
	exists_flag = os.path.exists(filename)
	if judge_init(overwrite, exists_flag) is False: return None
	# ファイル初期化
	dirname = os.path.dirname(filename)
	if os.path.exists(dirname) is False:
		os.makedirs(dirname)
	with open(filename, "w", encoding = encoding) as f:
		f.write(init_str)
