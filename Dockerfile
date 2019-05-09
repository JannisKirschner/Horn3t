FROM debian:latest

MAINTAINER xorkiwi

RUN apt update -y
RUN apt install chromium python3 python3-pip apache2 supervisor -y
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY src/ /var/www/html/
RUN pip3 install -r /var/www/html/requirements.txt
RUN pip3 install -r /var/www/html/libs/sublist3r/requirements.txt

RUN chmod -R 777 /var/www/html/
RUN ln -s /usr/lib/chromium/chromium /usr/bin/google-chrome
RUN chmod 700 /usr/bin/google-chrome

EXPOSE 80
EXPOSE 8080

CMD ["/usr/bin/supervisord"]
