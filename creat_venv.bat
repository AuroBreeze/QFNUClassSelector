echo "创建 Python 虚拟环境"
python -m venv .venv
echo "激活 Python 虚拟环境"
call .venv\Scripts\activate
echo "安装依赖"
pip install -r requirements.txt
pip install -e .
echo "完成"
pause
