from ib_insync import IB


def check_ib_gateway(host="127.0.0.1", port=7496, client_id=0):
    ib = IB()
    try:
        ib.connect(host, port, clientId=client_id, timeout=10)
        ib.disconnect()
        print("IB Gateway is healthy.")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


if __name__ == "__main__":
    exit(0 if check_ib_gateway() else 1)
