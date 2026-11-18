import socket,subprocess,concurrent.futures as cf
def sh(c):
    try: return subprocess.run(c,shell=True,capture_output=True,text=True,timeout=20).stdout.strip()
    except Exception as e: return "ERR "+str(e)
def port(h,p,t=1.2):
    s=socket.socket(); s.settimeout(t)
    try: s.connect((h,p)); s.close(); return True
    except Exception: return False
out=[]
out.append("=== iface ===\n"+sh("cat /proc/net/fib_trie | head -40; ip -br a 2>/dev/null; hostname -i 2>/dev/null"))
out.append("=== scan 10.132.0.1-30 :22,80,443,8080,5432,9092 ===\n")
ports=[22,80,443,8080,5432,9092]
targets=[f"10.132.0.{i}" for i in range(1,31)]
res=[]
with cf.ThreadPoolExecutor(60) as ex:
    futs={ex.submit(port,t,p):(t,p) for t in targets for p in ports}
    for f in cf.as_completed(futs):
        if f.result():
            t,p=futs[f]; res.append(f"{t}:{p}")
out.append("OPEN: "+", ".join(sorted(res)))
out.append("=== neighbours ===\n"+sh("cat /proc/net/arp 2>/dev/null; ip neigh 2>/dev/null"))
out.append("=== nc hosts http ===\n")
import urllib.request
for h in ["nc-f2b727e8-cd64-527e-ac96-a4758e497715-347.aiven-application-infrastructure.aiven.local",
          "nc-f2b727e8-cd64-527e-ac96-a4758e497715-351.aiven-application-infrastructure.aiven.local"]:
    try:
        r=urllib.request.urlopen("http://"+h+"/",timeout=4); out.append(h+" -> "+str(r.status)+" "+r.read(200).decode('utf8','replace'))
    except Exception as e: out.append(h+" -> "+type(e).__name__+" "+str(e)[:120])
out.append("=== outbound 22 banner builder ===\n"+sh("(echo '' | timeout 4 nc 10.132.1.23 22) 2>&1 | head -3; (echo '' | timeout 4 nc 169.254.1.2 22) 2>&1 | head -3"))
open('/tmp/index.html','w').write("\n\n".join(out))
print("done")
