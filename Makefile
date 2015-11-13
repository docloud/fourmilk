#
# Copyright 2015 FourMilk
#

help:
	@echo "develop  配置环境"
	@echo "test     运行单元测试"
	@echo "coverage 运行测试覆盖率检测"
	@echo "decument 编译文档"

develop:
	pip install -e .

test:
	py.test -s -v

coverage:
	py.test -s -v --cov=${SOURCE} --cov-report=html

document:
	make -C docs html
