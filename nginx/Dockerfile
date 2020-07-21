FROM nginx:stable

#RUN rm /etc/nginx/sites-enabled/default

COPY sites-enabled/ /etc/nginx/sites-enabled
RUN ls -la /etc/nginx/sites-enabled
COPY sites-enabled/pubtrack /etc/nginx/conf.d/default.conf