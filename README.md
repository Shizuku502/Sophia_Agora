# Sophia_Agora

Sophia_Agora 是一個基於 Flask 架構的論壇系統，提供以下功能：

- 使用者登入 / 登出
- 帳號管理（學生、老師、管理員）
- 發文 / 留言 / 回覆
- 按讚 / 倒讚 系統
- 髒話過濾
- 管理者後台：帳號、貼文、留言管理

## 技術棧

- Python 3.x
- Flask
- Jinja2 (template engine)
- SQLAlchemy
- MySQL
- Bootstrap (前端樣式)
- Git & GitHub

## 專案架構

Sophia_Agora/          
│
├── run.py 
├── config.py         
├── requirements.txt 
│
├── app/   
│   ├── models/
│   ├── auth/
│   │   └── templates/
│   │       └── auth/
│   ├── admin/ 
│   │   └── templates/
│   │       └── admin/
│   ├── forum/             
│   │   └── templates/
│   │       └── forum/
│   ├── templates/       
│   ├── static/           
│   │   ├── css/
│   │   └── js/
│   ├── utils/             
└── README.md         

## 執行方式

```bash
python run.py
