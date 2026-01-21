import uvicorn

# "app.app:app", in order: app folder, app file, app object/variable
# 0.0.0.0 host means running the app on any available domain
# which ends up being localhost most likely, also private IP address
# as mentioned by Tim

# any time a change is made to project files, server automatically restarts

# /docs always works for fastapi projects. can test endpoints in swagger easily



if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)

