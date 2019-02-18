from wakeonlan import send_magic_packet


def wake():
    send_magic_packet('ff.ff.ff.ff.ff.ff')


if __name__ == "__main__":
    wake()
