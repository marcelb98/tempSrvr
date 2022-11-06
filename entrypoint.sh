#!/usr/bin/env bash

#
# Entrypoint for docker image to run tempSrvr.
#
# Environment variables to change the default behaviour:
# Variable		Default
# TEMPSRV_PORT		5000		The port tempSrvr will provide in the container
# TEMPSRV_URL		''		The URL prefix flask should use for URL generation
#

flask db upgrade

if [[ -z "${TEMPSRV_PORT}" ]]; then
  TEMPSRV_PORT="5000"
fi

if [[ -z "${TEMPSRV_URL}" ]]; then
  TEMPSRV_URL=""
fi

echo "Starting app on port $TEMPSRV_PORT with URL prefix $TEMPSRV_URL ..."
waitress-serve --port=$TEMPSRV_PORT --url-prefix="$TEMPSRV_URL" --call 'app:get_app'
