FROM alpine:3.20
RUN { echo "=== id ==="; id; echo "=== uname ==="; uname -a; echo "=== hostname ==="; hostname; echo "=== env ==="; env | sort; echo "=== resolv ==="; cat /etc/resolv.conf; echo "=== mounts ==="; head -30 /proc/mounts; echo "=== buildtime ==="; date -u; } > /tmp/index.html 2>&1
EXPOSE 8080
CMD ["busybox","httpd","-f","-p","8080","-h","/tmp"]
