:: 创建 Python 虚拟环境（假设虚拟环境目录为 .venv）
echo "创建 Python 虚拟环境"
python -m venv .venv
echo "激活 Python 虚拟环境"
call .venv\Scripts\activate
echo "安装依赖"
pip install -r requirements.txt