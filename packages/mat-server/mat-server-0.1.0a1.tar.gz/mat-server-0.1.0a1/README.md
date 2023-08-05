# mat 代理伺服器

後端開發用代理伺服器，能攔截設定的 API，直接回傳指定的結果，其餘則直接轉發實際伺服器的回傳值。

   客戶端 -> mat server -> 實際的伺服器

在開發新功能的時候，時常後端功能尚未開發完成，前端必須等待後端功能完成後才能開發的情況，透過 mat 代理伺服器可以直接設定好預計的回傳內容，讓前端不需要通靈開發。

適合小專案快速開發，可以直接架在後端的電腦上，讓前端連進來，隨時可以修改 API 格式。

特色：

* 隨時可以修改設定，自動更新回傳值內容
* 支援 query string

## 安裝

### 透過 pip 安裝

```bash
pip install mat-server
```

## 使用方法

### 操作

```shell

# 初始化 mat (產生 mat-data 設定資料夾)
mat init

# 啟動伺服器 (http://0.0.0.0:3000)
mat -p 3000
```

### mat-data 資料夾

    mat-data/
        config.yml               # 設定要代理的伺服器等設定
        data/
            hello.json

### config.yml

```yaml
server:
  proxy_url: http://target_server  # 要代理的伺服器
routes:
  - listen_path: hello   # 要攔截的路由  (http://target_server/hello)
    method: GET          # HTTP Method  (預設為 GET)
    status_code: 200     # 回傳的 status code (預設為 200 OK)
    response:            # 回傳值設定 
      data:
        msg: hello world # 回傳 {"msg": "hello world"}
  - listen_path: hello
    query:               # 設定 query string (http://target_server/hello?name=marco
      name: marco
    response:
      file_path: data/hello.json # 回傳 hello.json 的檔案內容
```

### 範例

直接透過 config.yml 設定路由和回傳值

```yaml
server:
  proxy_url: https://marco79423.net
routes:
  - listen_path: backend/api/articles/
    response:
      data:
        - title: Hello mat-server
          content: 歡迎使用 mat-server
```

### 特殊路由

#### /_mat

回傳設定檔的內容

```json
{
  "server": {
    "proxy_url": "https://marco79423.net"
  },
  "routes": [
    {
      "listen_path": "backend/api/articles/",
      "response": {
        "data": [
          {
            "title": "Hello mat-server",
            "content": "歡迎使用 mat-server"
          } 
        ]
      }
    }
  ]
}
```

## 專案架構

    setup.py
    requirements.txt
    mat_server/
        app/                                    # 應用層
            command/
                __init__.py
                container.py
                main.py
            server/
              __init__.py
              container.py
              extensions/
                flask_routes/
                    proxy.py
                    info.py
        domain/                                 # 領域層
            use_cases/                          # 用例
                create_mat_data_use_case.py
                parse_mat_data_use_case.py
                proxy_target_route_use_case.py
                return_mat_data_use_case.py
                ...
            entities/
                config.py
                route.py
            helpers/
                yaml_helper.py
                
        infrastrcture/                          # 實作層
            helpers/
                yaml_helper.py
