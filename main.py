# main.py -- put your code here!

from pyb import UART, Pin

# 串口通信
uart2 = UART(2, 9600)

# 定义百位数码管:
A3 = Pin('B1', Pin.IN, Pin.PULL_DOWN)
B3 = Pin('C5', Pin.IN, Pin.PULL_DOWN)
C3 = Pin('A7', Pin.IN, Pin.PULL_DOWN)
D3 = Pin('A5', Pin.IN, Pin.PULL_DOWN)
E3 = Pin('A1', Pin.IN, Pin.PULL_DOWN)
F3 = Pin('C3', Pin.IN, Pin.PULL_DOWN)
G3 = Pin('C1', Pin.IN, Pin.PULL_DOWN)

# 定义十位数码管
A2 = Pin('B8', Pin.IN, Pin.PULL_DOWN)
B2 = Pin('C0', Pin.IN, Pin.PULL_DOWN)
C2 = Pin('C2', Pin.IN, Pin.PULL_DOWN)
D2 = Pin('A4', Pin.IN, Pin.PULL_DOWN)
E2 = Pin('A6', Pin.IN, Pin.PULL_DOWN)
F2 = Pin('C4', Pin.IN, Pin.PULL_DOWN)
G2 = Pin('B0', Pin.IN, Pin.PULL_DOWN)

# 定义个位数码管
A1 = Pin('B14', Pin.IN, Pin.PULL_DOWN)
B1 = Pin('C6', Pin.IN, Pin.PULL_DOWN)
C1 = Pin('B12', Pin.IN, Pin.PULL_DOWN)
D1 = Pin('B13', Pin.IN, Pin.PULL_DOWN)
E1 = Pin('B9', Pin.IN, Pin.PULL_DOWN)
F1 = Pin('C7', Pin.IN, Pin.PULL_DOWN)
G1 = Pin('B15', Pin.IN, Pin.PULL_DOWN)

# 重定义数码管位段列表
out1 = [G1, F1, E1, D1, C1, B1, A1]
out2 = [G2, F2, E2, D2, C2, B2, A2]
out3 = [G3, F3, E3, D3, C3, B3, A3]

# 数码管转换为16进制数据
tube = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]  # 0~9

AT_SCORE_Read = b'\x41\x54\x2b\x53\x43\x4f\x52\x45\x3d\x3f\x0d\x0a'  # AT+SCORE=?\r\n
AT = b'\x41\x54\x0d\x0a'  # AT 进行测试，返回值为OK
AT_OK = b'\x4f\x4b\x0d\x0a'

ERR = 0xFFFF

def get_value():

    out1_value, out2_value, out3_value = 0, 0, 0
    value = ERR
    try:
        for i in range(7):
            if out1[i].value() == 0:  # 检测电平为高时，说明数码管是熄灭的状态,因此只需检测是否为0即可
                out1_value |= 1
            out1_value << 1
        if out1_value in tube:
            out1_value = tube.index(out1_value)
        else:
            return ERR

        for i in range(7):
            if out2[i].value() == 0:
                out2_value |= 1
            out2_value << 1
        if out2_value in tube:
            out2_value = tube.index(out2_value)
        else:
            return ERR

        for i in range(7):
            if out3[i].value() == 0:
                out3_value |= 1
            out3_value << 1
        if out3_value in tube:
            out3_value = tube.index(out3_value)
        else:
            return ERR

        value = out3_value *100 + out2_value * 10 + out1_value
    except Exception as e:
        print("get_value is error", str(e))
    finally:
        return value


def main():
    while True:
        try:
            readData = uart2.readline()
            if readData == AT_SCORE_Read:
                value = get_value()
                AD_wirte = AT_SCORE_Read[2:9] + str(value) + AT_SCORE_Read[10:12]
                uart2.write(AD_wirte)
            elif readData == AT:
                uart2.write(AT_OK)
            elif readData is not None:
                print(readData)
        except Exception as e:
            print("get_value is error", str(e))


if __name__ == "__main__":
    main()