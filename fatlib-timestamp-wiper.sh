#!/bin/sh

if !( [ -f "${1}" ] ); then
    echo "Usage: fatlib-timestamp-wiper.sh <STATIC_LIB_PATH>"
    exit 1;
fi

SCRIPT_DIR="$(cd $(dirname ${0}); pwd)"
DIR="$(cd $(dirname ${1}); pwd)"
NAME=$(basename -s .a ${1})
FAT_LIB="${DIR}/${NAME}.old.a" 
mv -f "${1}" "${FAT_LIB}"

wipe_thin_lib() {
    ARCH="${1}";
    THIN_LIB="${DIR}/${NAME}-${ARCH}.a";

    lipo "${FAT_LIB}" -thin ${ARCH} -output "${THIN_LIB}"
    "${SCRIPT_DIR}/ar-timestamp-wiper.py" "${THIN_LIB}"
}

wipe_thin_lib i386
wipe_thin_lib armv7
wipe_thin_lib x86_64
wipe_thin_lib arm64

# link thin libs
lipo -create "${DIR}/${NAME}-i386.a" "${DIR}/${NAME}-armv7.a" "${DIR}/${NAME}-x86_64.a" "${DIR}/${NAME}-arm64.a" -output ${1}
rm "${DIR}/${NAME}-i386.a" "${DIR}/${NAME}-armv7.a" "${DIR}/${NAME}-x86_64.a" "${DIR}/${NAME}-arm64.a"

if [ -f "${1}" ]; then
    rm ${FAT_LIB}
    echo "wiping done."
else
    mv -f "${FAT_LIB}" "${1}"
    echo "wiping failed - library ${NAME}.a was recoverd"
fi
