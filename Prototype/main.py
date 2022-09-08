from website import create_web

web = create_web()

if __name__ == '__main__':
    web.run(port=9999, debug = True)
