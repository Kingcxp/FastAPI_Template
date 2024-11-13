# 项目名
### 作者: 作者名

## 项目简介
简介内容

## 安装项目
(你需要先行安装 `python` 和 `git`)
```sh
# 克隆这个项目
git clone https://github.com/gh_user/project_name.git
cd project_name
# 创建虚拟环境
python3 -m venv serverenv
# 启动虚拟环境
# Bash
source serverenv/bin/activate
# Fish
source serverenv/bin/activate.fish
# Powershell
.\serverenv\Scripts\Activate.ps1
# 安装项目依赖
pip install -r requirements.txt
# 启动项目服务
uvicorn app:app --port 8081 --host 0.0.0.0 --reload
```

## 关于邮件
如果你想发送邮件，你需要创建一个 .env 文件，内容如下：
```txt
EMAIL="user@example.com"
EMAIL_PASSKEY="YOUR_PASSKEY"
EMAIL_HOST="smtp.example.com"
```

## 贡献
如果你有任何改进意见，欢迎提交 issue 或者创建 pull request。
