import timeit
import yaml

response_text = "({ 'volume2': '100!50!!5000100!50!!5000', 'volume3': '00000000', 'Outputbuttom': '12345678', 'hdmi_buttom': '0102030405060708' })"

def bench_replace():
    response_text.replace("(", "").replace(")", "")

def bench_strip():
    response_text.strip("()")

print("replace:", timeit.timeit(bench_replace, number=1000000))
print("strip:", timeit.timeit(bench_strip, number=1000000))
