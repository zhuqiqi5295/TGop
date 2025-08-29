# -*- coding:utf-8 -*

import subprocess


class cmdrun(object):
    def __init__(self):

        self.tdlpath = ".\\tdl.exe"

    def run_tdl_command(self):
        """
        调用 tdl.exe 执行下载任务
        """
        # 定义命令和参数
        # command = [
        #     self.tdlpath,
        #     "dl",
        #     "-u",
        #     "https://t.me/FanRenXiuXianZhuan_TRJ/239",
        #     "--proxy socks5://192.168.31.125:7890",
        #     "-n zhuqiqi",
        #
        command = [
            self.tdlpath,
            "dl",
            "-u",
            "https://t.me/FanRenXiuXianZhuan_TRJ/6",
            "--proxy",
            "socks5://127.0.0.1:7890",
            "-n",
            "zhuqiqi",
        ]

        try:
            # 使用 subprocess.run 执行命令

            print("执行的命令:", " ".join(command))
            result = subprocess.run(
                command,
                capture_output=True,  # 捕获标准输出和标准错误
                text=True,  # 将输出解码为字符串
            )

            # 输出结果
            print("标准输出:")
            print(result.stdout)
            print("标准错误:")
            print(result.stderr)

        except subprocess.CalledProcessError as e:
            # 捕获命令执行失败的异常
            print(f"命令执行失败，退出码: {e.returncode}")
            print(f"错误信息: {e.stderr}")


if __name__ == "__main__":
    cmdrun().run_tdl_command()
