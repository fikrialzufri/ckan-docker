FROM ckan/ckan-base:ckan-2.10.0
#FROM ckan/ckan-base:dev-v2.10

# Set up environment variables
ENV APP_DIR=/srv/app
ENV TZ=UTC
RUN echo ${TZ} > /etc/timezone

# Make sure both files are not exactly the same
RUN if ! [ /usr/share/zoneinfo/${TZ} -ef /etc/localtime ]; then \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime ;\
    fi ;

# Install ckanext-mahulu extension
COPY src/ckanext-mahulu ${APP_DIR}/src/ckanext-mahulu
RUN if [ -d "${APP_DIR}/src/ckanext-mahulu" ]; then \
    pip3 install -e ${APP_DIR}/src/ckanext-mahulu; \
    fi

# Install ckanext-blog extension
COPY src/ckanext-blog ${APP_DIR}/src/ckanext-blog
RUN if [ -d "${APP_DIR}/src/ckanext-blog" ]; then \
    pip3 install -e ${APP_DIR}/src/ckanext-blog; \
    fi