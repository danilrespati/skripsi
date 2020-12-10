import os
import time


def sendAngle(stat, target, pos, angle):
    path = "/var/www/html/skripsi"
    os.chdir(path)
    message = """
        <?php
        $stat = {a};
        $target = '{b}';
        $x = {c};
        $y = {d};
        $pan = {e};
        $tlt = {f};""".format(a=stat, b=str(target), c=pos["x"], d=pos["y"], e=angle["pan"], f=angle["tlt"]) + """
        ?>
        """
    f = open('var.php', 'w')
    f.write(message)
    f.close()


pos = {"x": 0, "y": 0}
angle = {"pan": 0, "tlt": 0}
sendAngle(1, "Speedtest", pos, angle)
print(time.time())
sendAngle(0, "None", pos, angle)
print("\n[INFO] Exiting Program and cleanup stuff")
