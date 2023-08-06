### 安装依赖
    pi twine
    pi wheel
    pi --upgrade setuptools

### 打包发布
    python setup.py check
    python setup.py sdist
    python setup.py sdist bdist_wheel
    twine upload dist/*
