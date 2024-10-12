import uvicorn

def main() -> None:
    uvicorn.run(
        "provisionr.wsgi:create_app",
        host="127.0.0.1",
        port=8080,
        factory=True,
        reload=True,
    )


if __name__ == "__main__":
    main()
