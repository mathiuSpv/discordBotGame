from commands import client

def main():
    with open('key.txt', mode= 'r') as file:
        code= file.readline()
        file.close()
    client.run(code)

if __name__ == "__main__":
    main()