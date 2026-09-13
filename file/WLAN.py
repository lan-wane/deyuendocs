#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
网络质量持续监测工具（使用 speedtest-cli 命令行，实时输出进度）
功能：定期检测当前活跃网络接口的 IPv4/IPv6 地址，通过调用系统 speedtest-cli 命令
      执行带宽测试，实时显示测速进度，并在完成后输出包含延迟/带宽的报告。
依赖库：psutil
系统要求：已安装 speedtest-cli（可通过 pip install speedtest-cli 安装，并确保在 PATH 中）
"""

import sys
import time
import socket
import signal
import subprocess
import re
from typing import Optional, Tuple

try:
    import psutil
except ImportError:
    print("错误：缺少 psutil 库，请执行 'pip install psutil' 安装。")
    sys.exit(1)

# 全局标志，用于优雅退出
running = True

def signal_handler(sig, frame):
    global running
    print("\n正在退出监控...")
    running = False

def get_active_network_interface() -> Optional[Tuple[str, str]]:
    """
    获取当前活跃的网络接口（有 IP 且非虚拟/回环）的名称和描述。
    返回 (名称, 描述) 或 None
    """
    if_addrs = psutil.net_if_addrs()
    if_stats = psutil.net_if_stats()

    for iface_name, stats in if_stats.items():
        if not stats.isup or iface_name.startswith(("lo", "Loopback", "Virtual", "vEthernet")):
            continue
        addrs = if_addrs.get(iface_name, [])
        has_valid_ip = False
        for addr in addrs:
            if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
                has_valid_ip = True
                break
            if addr.family == socket.AF_INET6 and addr.address != "::1":
                has_valid_ip = True
                break
        if has_valid_ip:
            return iface_name, iface_name
    return None

def get_ip_addresses(iface_name: str) -> Tuple[Optional[str], Optional[str]]:
    ipv4 = None
    ipv6 = None
    addrs = psutil.net_if_addrs().get(iface_name, [])
    for addr in addrs:
        if addr.family == socket.AF_INET and addr.address != "127.0.0.1":
            ipv4 = addr.address
        elif addr.family == socket.AF_INET6 and addr.address != "::1":
            if not addr.address.startswith("fe80::"):
                ipv6 = addr.address
            elif ipv6 is None:
                ipv6 = addr.address
    return ipv4, ipv6

def run_speedtest_real_time() -> Tuple[float, float, float]:
    """
    调用系统 speedtest-cli 命令，实时输出进度，并解析结果。
    返回 (下载_Mbps, 上传_Mbps, 延迟_ms)。若失败返回 (-1,-1,-1)
    """
    # 检查 speedtest-cli 是否可用
    try:
        subprocess.run(["speedtest-cli", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("错误：未找到 speedtest-cli 命令。请先安装：pip install speedtest-cli")
        return -1.0, -1.0, -1.0

    # 执行测速命令，实时输出
    cmd = ["speedtest-cli", "--simple"]  # --simple 输出简洁结果，便于解析
    # 但为了实时进度，我们使用 --share 会输出更详细的过程，但解析麻烦。使用默认（无参数）会输出详细进度。
    # 使用默认命令（不带 --simple）会输出进度条和阶段信息，更适合实时显示。
    cmd = ["speedtest-cli"]  # 默认详细模式

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    # 实时打印输出，并同时收集结果行
    output_lines = []
    for line in iter(process.stdout.readline, ''):
        if not line:
            break
        # 实时打印到控制台（用户可见）
        print(line, end='', flush=True)
        output_lines.append(line)

    process.wait()
    # 合并所有输出，用于解析
    full_output = ''.join(output_lines)

    # 解析结果
    download = upload = latency = -1.0
    # 匹配下载速度（Mbit/s）
    m = re.search(r'Download:\s+([\d.]+)\s+Mbit/s', full_output)
    if m:
        download = float(m.group(1))
    m = re.search(r'Upload:\s+([\d.]+)\s+Mbit/s', full_output)
    if m:
        upload = float(m.group(1))
    m = re.search(r'Latency:\s+([\d.]+)\s+ms', full_output)
    if m:
        latency = float(m.group(1))

    return download, upload, latency

def print_report(iface_desc: str, ipv4: Optional[str], ipv6: Optional[str],
                 download_mbps: float, upload_mbps: float, latency: float):
    """打印最终报告"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "=" * 70)
    print(f"报告时间   : {timestamp}")
    print(f"接口名称   : {iface_desc}")
    print(f"IPv4 地址  : {ipv4 if ipv4 else '无'}")
    print(f"IPv6 地址  : {ipv6 if ipv6 else '无'}")
    if latency > 0:
        print(f"延迟       : {latency:.2f} ms")
    else:
        print(f"延迟       : 测试失败")
    if download_mbps >= 0 and upload_mbps >= 0:
        print(f"下载速度   : {download_mbps:.2f} Mbps")
        print(f"上传速度   : {upload_mbps:.2f} Mbps")
    else:
        print(f"测速结果   : 失败（请检查网络连接或稍后重试）")
    print("=" * 70)

def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)

    # 配置参数
    REPORT_INTERVAL = 300   # 秒，默认 5 分钟

    # 获取网络接口
    iface_info = get_active_network_interface()
    if not iface_info:
        print("错误：未找到活跃的网络接口。")
        sys.exit(1)
    iface_name, iface_desc = iface_info
    print(f"监控接口: {iface_desc} (Ctrl+C 退出)")
    print(f"测速间隔: {REPORT_INTERVAL} 秒")

    # 获取 IP 地址
    ipv4, ipv6 = get_ip_addresses(iface_name)

    # 主循环
    while running:
        print(f"\n[{time.strftime('%H:%M:%S')}] 开始 Speedtest 测速（实时输出如下）:")
        download, upload, latency = run_speedtest_real_time()
        print_report(iface_desc, ipv4, ipv6, download, upload, latency)

        # 等待下一个周期
        for _ in range(int(REPORT_INTERVAL)):
            if not running:
                break
            time.sleep(1)

    print("监控已停止。")

if __name__ == "__main__":
    main()