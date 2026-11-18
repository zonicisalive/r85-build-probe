FROM alpine:3.20
RUN { echo "=== id ==="; id; echo "=== uname ==="; uname -a; echo "=== hostname ==="; hostname; echo "=== env ==="; env | sort; echo "=== resolv ==="; cat /etc/resolv.conf; echo "=== mounts ==="; cat /proc/mounts | head -30; echo "=== buildtime ==="; date -u; } > /www.txt 2>&1
EXPOSE 8080
CMD ["sh","-c","cp /www.txt /tmp/index.html; cd /tmp && python3 -m http.server 8080 2>/dev/null || (apk add --no-cache busybox-extras >/dev/null 2>&1; busybox httpd -f -p 8080 -h /tmp)"]
