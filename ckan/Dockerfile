FROM ckan/ckan-base:2.11

# Install any extensions needed by your CKAN instance
# See Dockerfile.dev for more details and examples

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

# Copy custom initialization scripts
COPY --chown=ckan-sys:ckan-sys docker-entrypoint.d/* /docker-entrypoint.d/

# Apply any patches needed to CKAN core or any of the built extensions (not the
# runtime mounted ones)
COPY --chown=ckan-sys:ckan-sys patches ${APP_DIR}/patches

USER ckan

RUN for d in $APP_DIR/patches/*; do \
    if [ -d $d ]; then \
    for f in `ls $d/*.patch | sort -g`; do \
    cd $SRC_DIR/`basename "$d"` && echo "$0: Applying patch $f to $SRC_DIR/`basename $d`"; patch -p1 < "$f" ; \
    done ; \
    fi ; \
    done
