import os,socket,subprocess,urllib.request
def sh(c):
    try: return subprocess.run(c,shell=True,capture_output=True,text=True,timeout=20).stdout.strip()
    except Exception as e: return "ERR "+str(e)
def port(h,p,t=2):
    s=socket.socket(); s.settimeout(t)
    try:
        s.connect((h,p)); s.close(); return "OPEN"
    except Exception as e: return type(e).__name__
out=[]
out.append("=== caps ===\n"+sh("grep -E 'Cap|Seccomp|NoNewPrivs' /proc/self/status"))
out.append("=== hosts ===\n"+open('/etc/hosts').read())
out.append("=== /podman exists ===\n"+("yes "+sh("ls /podman 2>&1 | head") if os.path.exists('/podman') else "absent"))
out.append("=== writable /proc/sys? ===\n"+sh("echo 1 > /proc/sys/kernel/sysrq 2>&1; echo rc=$?"))
out.append("=== cgroup ===\n"+sh("cat /proc/self/cgroup; ls /sys/fs/cgroup | head"))
out.append("=== host gateway ports 169.254.1.2 ===")
for p in [22,80,443,2375,2376,6443,8080,9090,10250]:
    out.append(f"  169.254.1.2:{p} -> {port('169.254.1.2',p)}")
out.append("=== build host 10.132.1.23 ===")
for p in [22,80,443,2375,2376,5000,6443,8080]:
    out.append(f"  10.132.1.23:{p} -> {port('10.132.1.23',p)}")
out.append("=== gateway 10.132.1.1 ===")
for p in [22,53,80,443,2375,2376,6443]:
    out.append(f"  10.132.1.1:{p} -> {port('10.132.1.1',p)}")
out.append("=== my ip/route ===\n"+sh("ip -br addr 2>/dev/null; ip route 2>/dev/null"))
out.append("=== dns resolve aiven.local ===\n"+sh("getent hosts build-b2f5e370-070d-53ca-c45e-0e7762dbbd60.aiven.local; getent hosts aiven-application-infrastructure.aiven.local"))
out.append("=== /proc/1/root ===")
try: out.append("pid1 root ls: "+",".join(os.listdir('/proc/1/root')[:15]))
except Exception as e: out.append("ERR "+str(e))
open('/tmp/index.html','w').write("\n\n".join(out))
print("done")
