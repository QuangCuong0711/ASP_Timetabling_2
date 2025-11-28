#!/bin/bash

# Kiểm tra Python
if command -v python &> /dev/null; then
    PYTHON=python
elif command -v python3 &> /dev/null; then
    PYTHON=python3
else
    echo "Python chưa được cài hoặc chưa thêm vào PATH."
    exit 1
fi

# Cài dependencies nếu cần
pip install -r requirements.txt

# Chạy chương trình chính với tham số
$PYTHON main.py "$@"