# njnuko

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.
# 安装必要工具
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository testpypi dist/*

4.python setup.py sdist build
5.twine upload dist/*
ID/PW:njnuko/2018!Daren
pip install njnuko==4.0.0 -i https://pypi.org/project
