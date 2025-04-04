import subprocess
import re

# Input: The list of libraries
libraries = """
	        linux-vdso.so.1 (0x00007ffff7fc3000)
        liblagom-imagedecoderclient.so.0 => /cfop/Build/lagom/lib/liblagom-imagedecoderclient.so.0 (0x00007ffff7df5000)
        liblagom-websocket.so.0 => /cfop/Build/lagom/lib/liblagom-websocket.so.0 (0x00007ffff7dce000)
        liblagom-webview.so.0 => /cfop/Build/lagom/lib/liblagom-webview.so.0 (0x00007ffff7c12000)
        libQt6Multimedia.so.6 => /lib/x86_64-linux-gnu/libQt6Multimedia.so.6 (0x00007ffff7b33000)
        libQt6Network.so.6 => /lib/x86_64-linux-gnu/libQt6Network.so.6 (0x00007ffff799c000)
        libQt6Core.so.6 => /lib/x86_64-linux-gnu/libQt6Core.so.6 (0x00007ffff748e000)
        liblagom-sql.so.0 => /cfop/Build/lagom/lib/liblagom-sql.so.0 (0x00007ffff7405000)
        liblagom-web.so.0 => /cfop/Build/lagom/lib/liblagom-web.so.0 (0x00007ffff5c00000)
        liblagom-accelgfx.so.0 => /cfop/Build/lagom/lib/liblagom-accelgfx.so.0 (0x00007ffff73ef000)
        liblagom-gfx.so.0 => /cfop/Build/lagom/lib/liblagom-gfx.so.0 (0x00007ffff5800000)
        liblagom-js.so.0 => /cfop/Build/lagom/lib/liblagom-js.so.0 (0x00007ffff5000000)
        liblagom-filesystem.so.0 => /cfop/Build/lagom/lib/liblagom-filesystem.so.0 (0x00007ffff73e0000)
        liblagom-protocol.so.0 => /cfop/Build/lagom/lib/liblagom-protocol.so.0 (0x00007ffff5b85000)
        liblagom-ipc.so.0 => /cfop/Build/lagom/lib/liblagom-ipc.so.0 (0x00007ffff73c6000)
        liblagom-core.so.0 => /cfop/Build/lagom/lib/liblagom-core.so.0 (0x00007ffff5761000)
        liblagom-corebasic.so.0 => /cfop/Build/lagom/lib/liblagom-corebasic.so.0 (0x00007ffff5b12000)
        liblagom-coreminimal.so.0 => /cfop/Build/lagom/lib/liblagom-coreminimal.so.0 (0x00007ffff5729000)
        liblagom-url.so.0 => /cfop/Build/lagom/lib/liblagom-url.so.0 (0x00007ffff73ac000)
        liblagom-ak.so.0 => /cfop/Build/lagom/lib/liblagom-ak.so.0 (0x00007ffff56b4000)
        libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007ffff4d82000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ffff4b70000)
        /lib64/ld-linux-x86-64.so.2 (0x00007ffff7fc5000)
        liblagom-tls.so.0 => /cfop/Build/lagom/lib/liblagom-tls.so.0 (0x00007ffff4af4000)
        liblagom-crypto.so.0 => /cfop/Build/lagom/lib/liblagom-crypto.so.0 (0x00007ffff5661000)
        liblagom-syntax.so.0 => /cfop/Build/lagom/lib/liblagom-syntax.so.0 (0x00007ffff739b000)
        liblagom-unicode.so.0 => /cfop/Build/lagom/lib/liblagom-unicode.so.0 (0x00007ffff4600000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007ffff4a0b000)
        libQt6Gui.so.6 => /lib/x86_64-linux-gnu/libQt6Gui.so.6 (0x00007ffff3ecf000)
        libpulse.so.0 => /lib/x86_64-linux-gnu/libpulse.so.0 (0x00007ffff49ba000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007ffff498c000)
        libgssapi_krb5.so.2 => /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 (0x00007ffff3e7b000)
        libbrotlidec.so.1 => /lib/x86_64-linux-gnu/libbrotlidec.so.1 (0x00007ffff5b04000)
        libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007ffff3dc1000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007ffff3da5000)
        libproxy.so.1 => /lib/x86_64-linux-gnu/libproxy.so.1 (0x00007ffff565c000)
        libicui18n.so.74 => /lib/x86_64-linux-gnu/libicui18n.so.74 (0x00007ffff3a57000)
        libicuuc.so.74 => /lib/x86_64-linux-gnu/libicuuc.so.74 (0x00007ffff384a000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007ffff3701000)
        libdouble-conversion.so.3 => /lib/x86_64-linux-gnu/libdouble-conversion.so.3 (0x00007ffff4977000)
        libb2.so.1 => /lib/x86_64-linux-gnu/libb2.so.1 (0x00007ffff36e3000)
        libpcre2-16.so.0 => /lib/x86_64-linux-gnu/libpcre2-16.so.0 (0x00007ffff3657000)
        liblagom-regex.so.0 => /cfop/Build/lagom/lib/liblagom-regex.so.0 (0x00007ffff35e2000)
        liblagom-markdown.so.0 => /cfop/Build/lagom/lib/liblagom-markdown.so.0 (0x00007ffff35c1000)
        liblagom-http.so.0 => /cfop/Build/lagom/lib/liblagom-http.so.0 (0x00007ffff3595000)
        liblagom-audio.so.0 => /cfop/Build/lagom/lib/liblagom-audio.so.0 (0x00007ffff34f1000)
        liblagom-media.so.0 => /cfop/Build/lagom/lib/liblagom-media.so.0 (0x00007ffff3464000)
        liblagom-wasm.so.0 => /cfop/Build/lagom/lib/liblagom-wasm.so.0 (0x00007ffff3334000)
        liblagom-xml.so.0 => /cfop/Build/lagom/lib/liblagom-xml.so.0 (0x00007ffff3305000)
        liblagom-idl.so.0 => /cfop/Build/lagom/lib/liblagom-idl.so.0 (0x00007ffff32d8000)
        libOpenGL.so.0 => /lib/x86_64-linux-gnu/libOpenGL.so.0 (0x00007ffff32ad000)
        liblagom-textcodec.so.0 => /cfop/Build/lagom/lib/liblagom-textcodec.so.0 (0x00007ffff323b000)
        libEGL.so.1 => /lib/x86_64-linux-gnu/libEGL.so.1 (0x00007ffff3229000)
        liblagom-compress.so.0 => /cfop/Build/lagom/lib/liblagom-compress.so.0 (0x00007ffff31c7000)
        liblagom-riff.so.0 => /cfop/Build/lagom/lib/liblagom-riff.so.0 (0x00007ffff5651000)
        liblagom-locale.so.0 => /cfop/Build/lagom/lib/liblagom-locale.so.0 (0x00007ffff2600000)
        libcrypt.so.1 => /lib/x86_64-linux-gnu/libcrypt.so.1 (0x00007ffff318d000)
        libfontconfig.so.1 => /lib/x86_64-linux-gnu/libfontconfig.so.1 (0x00007ffff313c000)
        libX11.so.6 => /lib/x86_64-linux-gnu/libX11.so.6 (0x00007ffff24c3000)
        libQt6DBus.so.6 => /lib/x86_64-linux-gnu/libQt6DBus.so.6 (0x00007ffff3087000)
        libxkbcommon.so.0 => /lib/x86_64-linux-gnu/libxkbcommon.so.0 (0x00007ffff303e000)
        libGLX.so.0 => /lib/x86_64-linux-gnu/libGLX.so.0 (0x00007ffff2490000)
        libpng16.so.16 => /lib/x86_64-linux-gnu/libpng16.so.16 (0x00007ffff2458000)
        libharfbuzz.so.0 => /lib/x86_64-linux-gnu/libharfbuzz.so.0 (0x00007ffff234b000)
        libmd4c.so.0 => /lib/x86_64-linux-gnu/libmd4c.so.0 (0x00007ffff2339000)
        libfreetype.so.6 => /lib/x86_64-linux-gnu/libfreetype.so.6 (0x00007ffff226d000)
        libpulsecommon-16.1.so => /usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-16.1.so (0x00007ffff21ef000)
        libdbus-1.so.3 => /lib/x86_64-linux-gnu/libdbus-1.so.3 (0x00007ffff21a0000)
        libkrb5.so.3 => /lib/x86_64-linux-gnu/libkrb5.so.3 (0x00007ffff20d7000)
        libk5crypto.so.3 => /lib/x86_64-linux-gnu/libk5crypto.so.3 (0x00007ffff20ab000)
        libcom_err.so.2 => /lib/x86_64-linux-gnu/libcom_err.so.2 (0x00007ffff3038000)
        libkrb5support.so.0 => /lib/x86_64-linux-gnu/libkrb5support.so.0 (0x00007ffff209e000)
        libbrotlicommon.so.1 => /lib/x86_64-linux-gnu/libbrotlicommon.so.1 (0x00007ffff207b000)
        libpxbackend-1.0.so => /usr/lib/x86_64-linux-gnu/libproxy/libpxbackend-1.0.so (0x00007ffff206d000)
        libgobject-2.0.so.0 => /lib/x86_64-linux-gnu/libgobject-2.0.so.0 (0x00007ffff200a000)
        libicudata.so.74 => /lib/x86_64-linux-gnu/libicudata.so.74 (0x00007ffff02aa000)
        libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x00007ffff0210000)
        libgomp.so.1 => /lib/x86_64-linux-gnu/libgomp.so.1 (0x00007ffff01ba000)
        liblagom-threading.so.0 => /cfop/Build/lagom/lib/liblagom-threading.so.0 (0x00007ffff01b0000)
        libGLdispatch.so.0 => /lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x00007ffff00f8000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007ffff00cd000)
        libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007ffff00a4000)
        libgraphite2.so.3 => /lib/x86_64-linux-gnu/libgraphite2.so.3 (0x00007ffff007e000)
        libbz2.so.1.0 => /lib/x86_64-linux-gnu/libbz2.so.1.0 (0x00007ffff006a000)
        libsndfile.so.1 => /lib/x86_64-linux-gnu/libsndfile.so.1 (0x00007fffeffe2000)
        libX11-xcb.so.1 => /lib/x86_64-linux-gnu/libX11-xcb.so.1 (0x00007fffeffdd000)
        libsystemd.so.0 => /lib/x86_64-linux-gnu/libsystemd.so.0 (0x00007fffefefd000)
        libasyncns.so.0 => /lib/x86_64-linux-gnu/libasyncns.so.0 (0x00007fffefef5000)
        libapparmor.so.1 => /lib/x86_64-linux-gnu/libapparmor.so.1 (0x00007fffefee1000)
        libkeyutils.so.1 => /lib/x86_64-linux-gnu/libkeyutils.so.1 (0x00007fffefeda000)
        libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007fffefec7000)
        libcurl-gnutls.so.4 => /lib/x86_64-linux-gnu/libcurl-gnutls.so.4 (0x00007fffefe0c000)
        libgio-2.0.so.0 => /lib/x86_64-linux-gnu/libgio-2.0.so.0 (0x00007fffefc3c000)
        libduktape.so.207 => /lib/x86_64-linux-gnu/libduktape.so.207 (0x00007fffefbf1000)
        libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007fffefbe5000)
        libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007fffefbdf000)
        libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007fffefbd7000)
        libFLAC.so.12 => /lib/x86_64-linux-gnu/libFLAC.so.12 (0x00007fffefb73000)
        libvorbis.so.0 => /lib/x86_64-linux-gnu/libvorbis.so.0 (0x00007fffefb45000)
        libvorbisenc.so.2 => /lib/x86_64-linux-gnu/libvorbisenc.so.2 (0x00007fffefa98000)
        libopus.so.0 => /lib/x86_64-linux-gnu/libopus.so.0 (0x00007fffefa39000)
        libogg.so.0 => /lib/x86_64-linux-gnu/libogg.so.0 (0x00007fffefa2f000)
        libmpg123.so.0 => /lib/x86_64-linux-gnu/libmpg123.so.0 (0x00007fffef9d3000)
        libmp3lame.so.0 => /lib/x86_64-linux-gnu/libmp3lame.so.0 (0x00007fffef95d000)
        libcap.so.2 => /lib/x86_64-linux-gnu/libcap.so.2 (0x00007fffef94e000)
        libgcrypt.so.20 => /lib/x86_64-linux-gnu/libgcrypt.so.20 (0x00007fffef806000)
        liblz4.so.1 => /lib/x86_64-linux-gnu/liblz4.so.1 (0x00007fffef7e4000)
        liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007fffef7b2000)
        libnghttp2.so.14 => /lib/x86_64-linux-gnu/libnghttp2.so.14 (0x00007fffef787000)
        libidn2.so.0 => /lib/x86_64-linux-gnu/libidn2.so.0 (0x00007fffef763000)
        librtmp.so.1 => /lib/x86_64-linux-gnu/librtmp.so.1 (0x00007fffef745000)
        libssh.so.4 => /lib/x86_64-linux-gnu/libssh.so.4 (0x00007fffef6d4000)
        libpsl.so.5 => /lib/x86_64-linux-gnu/libpsl.so.5 (0x00007fffef6c0000)
        libnettle.so.8 => /lib/x86_64-linux-gnu/libnettle.so.8 (0x00007fffef66b000)
        libgnutls.so.30 => /lib/x86_64-linux-gnu/libgnutls.so.30 (0x00007fffef471000)
        libldap.so.2 => /lib/x86_64-linux-gnu/libldap.so.2 (0x00007fffef412000)
        liblber.so.2 => /lib/x86_64-linux-gnu/liblber.so.2 (0x00007fffef402000)
        libgmodule-2.0.so.0 => /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 (0x00007fffef3fb000)
        libmount.so.1 => /lib/x86_64-linux-gnu/libmount.so.1 (0x00007fffef3ae000)
        libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007fffef381000)
        libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007fffef369000)
        libgpg-error.so.0 => /lib/x86_64-linux-gnu/libgpg-error.so.0 (0x00007fffef344000)
        libunistring.so.5 => /lib/x86_64-linux-gnu/libunistring.so.5 (0x00007fffef197000)
        libhogweed.so.6 => /lib/x86_64-linux-gnu/libhogweed.so.6 (0x00007fffef14f000)
        libgmp.so.10 => /lib/x86_64-linux-gnu/libgmp.so.10 (0x00007fffef0cb000)
        libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x00007fffeebb6000)
        libp11-kit.so.0 => /lib/x86_64-linux-gnu/libp11-kit.so.0 (0x00007fffeea12000)
        libtasn1.so.6 => /lib/x86_64-linux-gnu/libtasn1.so.6 (0x00007fffee9fc000)
        libsasl2.so.2 => /lib/x86_64-linux-gnu/libsasl2.so.2 (0x00007fffee9e2000)
        libblkid.so.1 => /lib/x86_64-linux-gnu/libblkid.so.1 (0x00007fffee9a7000)
        libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007fffee996000)
                linux-vdso.so.1 (0x00007ffff7fc3000)
        liblagom-imagedecoderclient.so.0 => /cfop/Build/lagom/lib/liblagom-imagedecoderclient.so.0 (0x00007ffff7df5000)
        liblagom-websocket.so.0 => /cfop/Build/lagom/lib/liblagom-websocket.so.0 (0x00007ffff7dce000)
        liblagom-webview.so.0 => /cfop/Build/lagom/lib/liblagom-webview.so.0 (0x00007ffff7c12000)
        libQt6Multimedia.so.6 (0x00007ffff7b3b000)
        libQt6Network.so.6 (0x00007ffff79a4000)
        libQt6Core.so.6 (0x00007ffff7496000)
        liblagom-sql.so.0 => /cfop/Build/lagom/lib/liblagom-sql.so.0 (0x00007ffff740d000)
        liblagom-web.so.0 => /cfop/Build/lagom/lib/liblagom-web.so.0 (0x00007ffff5c00000)
        liblagom-accelgfx.so.0 => /cfop/Build/lagom/lib/liblagom-accelgfx.so.0 (0x00007ffff73f7000)
        liblagom-gfx.so.0 => /cfop/Build/lagom/lib/liblagom-gfx.so.0 (0x00007ffff5800000)
        liblagom-js.so.0 => /cfop/Build/lagom/lib/liblagom-js.so.0 (0x00007ffff5000000)
        liblagom-filesystem.so.0 => /cfop/Build/lagom/lib/liblagom-filesystem.so.0 (0x00007ffff73e8000)
        liblagom-protocol.so.0 => /cfop/Build/lagom/lib/liblagom-protocol.so.0 (0x00007ffff5b85000)
        liblagom-ipc.so.0 => /cfop/Build/lagom/lib/liblagom-ipc.so.0 (0x00007ffff73ce000)
        liblagom-core.so.0 => /cfop/Build/lagom/lib/liblagom-core.so.0 (0x00007ffff5761000)
        liblagom-corebasic.so.0 => /cfop/Build/lagom/lib/liblagom-corebasic.so.0 (0x00007ffff5b12000)
        liblagom-coreminimal.so.0 => /cfop/Build/lagom/lib/liblagom-coreminimal.so.0 (0x00007ffff7394000)
        liblagom-url.so.0 => /cfop/Build/lagom/lib/liblagom-url.so.0 (0x00007ffff5749000)
        liblagom-ak.so.0 => /cfop/Build/lagom/lib/liblagom-ak.so.0 (0x00007ffff56d4000)
        libstdc++.so.6 (0x00007ffff4d82000)
        libc.so.6 (0x00007ffff4b70000)
        /lib64/ld-linux-x86-64.so.2 (0x00007ffff7fc5000)
        liblagom-tls.so.0 => /cfop/Build/lagom/lib/liblagom-tls.so.0 (0x00007ffff5658000)
        liblagom-crypto.so.0 => /cfop/Build/lagom/lib/liblagom-crypto.so.0 (0x00007ffff4b1d000)
        liblagom-syntax.so.0 => /cfop/Build/lagom/lib/liblagom-syntax.so.0 (0x00007ffff4b0e000)
        liblagom-unicode.so.0 => /cfop/Build/lagom/lib/liblagom-unicode.so.0 (0x00007ffff4600000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007ffff4a25000)
        libQt6Gui.so.6 => /lib/x86_64-linux-gnu/libQt6Gui.so.6 (0x00007ffff3ecf000)
        libpulse.so.0 => /lib/x86_64-linux-gnu/libpulse.so.0 (0x00007ffff49d4000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007ffff49a6000)
        libgssapi_krb5.so.2 => /lib/x86_64-linux-gnu/libgssapi_krb5.so.2 (0x00007ffff3e7b000)
        libbrotlidec.so.1 => /lib/x86_64-linux-gnu/libbrotlidec.so.1 (0x00007ffff4998000)
        libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007ffff3dc1000)
        libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007ffff497c000)
        libproxy.so.1 => /lib/x86_64-linux-gnu/libproxy.so.1 (0x00007ffff5653000)
        libicui18n.so.74 => /lib/x86_64-linux-gnu/libicui18n.so.74 (0x00007ffff3a73000)
        libicuuc.so.74 => /lib/x86_64-linux-gnu/libicuuc.so.74 (0x00007ffff3866000)
        libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007ffff371d000)
        libdouble-conversion.so.3 => /lib/x86_64-linux-gnu/libdouble-conversion.so.3 (0x00007ffff3708000)
        libb2.so.1 => /lib/x86_64-linux-gnu/libb2.so.1 (0x00007ffff36ea000)
        libpcre2-16.so.0 => /lib/x86_64-linux-gnu/libpcre2-16.so.0 (0x00007ffff365e000)
        liblagom-regex.so.0 => /cfop/Build/lagom/lib/liblagom-regex.so.0 (0x00007ffff35e9000)
        liblagom-markdown.so.0 => /cfop/Build/lagom/lib/liblagom-markdown.so.0 (0x00007ffff35c8000)
        liblagom-http.so.0 => /cfop/Build/lagom/lib/liblagom-http.so.0 (0x00007ffff359c000)
        liblagom-audio.so.0 => /cfop/Build/lagom/lib/liblagom-audio.so.0 (0x00007ffff34f8000)
        liblagom-media.so.0 => /cfop/Build/lagom/lib/liblagom-media.so.0 (0x00007ffff346b000)
        liblagom-wasm.so.0 => /cfop/Build/lagom/lib/liblagom-wasm.so.0 (0x00007ffff333b000)
        liblagom-xml.so.0 => /cfop/Build/lagom/lib/liblagom-xml.so.0 (0x00007ffff330c000)
        liblagom-idl.so.0 => /cfop/Build/lagom/lib/liblagom-idl.so.0 (0x00007ffff32df000)
        libOpenGL.so.0 => /lib/x86_64-linux-gnu/libOpenGL.so.0 (0x00007ffff32b4000)
        liblagom-textcodec.so.0 => /cfop/Build/lagom/lib/liblagom-textcodec.so.0 (0x00007ffff3242000)
        libEGL.so.1 => /lib/x86_64-linux-gnu/libEGL.so.1 (0x00007ffff3230000)
        liblagom-compress.so.0 => /cfop/Build/lagom/lib/liblagom-compress.so.0 (0x00007ffff31ce000)
        liblagom-riff.so.0 => /cfop/Build/lagom/lib/liblagom-riff.so.0 (0x00007ffff4973000)
        liblagom-locale.so.0 => /cfop/Build/lagom/lib/liblagom-locale.so.0 (0x00007ffff2600000)
        libcrypt.so.1 => /lib/x86_64-linux-gnu/libcrypt.so.1 (0x00007ffff3192000)
        libfontconfig.so.1 => /lib/x86_64-linux-gnu/libfontconfig.so.1 (0x00007ffff3141000)
        libX11.so.6 => /lib/x86_64-linux-gnu/libX11.so.6 (0x00007ffff24c3000)
        libQt6DBus.so.6 => /lib/x86_64-linux-gnu/libQt6DBus.so.6 (0x00007ffff308a000)
        libxkbcommon.so.0 => /lib/x86_64-linux-gnu/libxkbcommon.so.0 (0x00007ffff3041000)
        libGLX.so.0 => /lib/x86_64-linux-gnu/libGLX.so.0 (0x00007ffff2490000)
        libpng16.so.16 => /lib/x86_64-linux-gnu/libpng16.so.16 (0x00007ffff2458000)
        libharfbuzz.so.0 => /lib/x86_64-linux-gnu/libharfbuzz.so.0 (0x00007ffff234b000)
        libmd4c.so.0 => /lib/x86_64-linux-gnu/libmd4c.so.0 (0x00007ffff302f000)
        libfreetype.so.6 => /lib/x86_64-linux-gnu/libfreetype.so.6 (0x00007ffff227d000)
        libpulsecommon-16.1.so => /usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-16.1.so (0x00007ffff21ff000)
        libdbus-1.so.3 => /lib/x86_64-linux-gnu/libdbus-1.so.3 (0x00007ffff21b0000)
        libkrb5.so.3 => /lib/x86_64-linux-gnu/libkrb5.so.3 (0x00007ffff20e7000)
        libk5crypto.so.3 => /lib/x86_64-linux-gnu/libk5crypto.so.3 (0x00007ffff20bb000)
        libcom_err.so.2 => /lib/x86_64-linux-gnu/libcom_err.so.2 (0x00007ffff20b3000)
        libkrb5support.so.0 => /lib/x86_64-linux-gnu/libkrb5support.so.0 (0x00007ffff20a6000)
        libbrotlicommon.so.1 => /lib/x86_64-linux-gnu/libbrotlicommon.so.1 (0x00007ffff2083000)
        libpxbackend-1.0.so => /usr/lib/x86_64-linux-gnu/libproxy/libpxbackend-1.0.so (0x00007ffff2075000)
        libgobject-2.0.so.0 => /lib/x86_64-linux-gnu/libgobject-2.0.so.0 (0x00007ffff2012000)
        libicudata.so.74 => /lib/x86_64-linux-gnu/libicudata.so.74 (0x00007ffff02b0000)
        libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0 (0x00007ffff0216000)
        libgomp.so.1 => /lib/x86_64-linux-gnu/libgomp.so.1 (0x00007ffff01c0000)
        liblagom-threading.so.0 => /cfop/Build/lagom/lib/liblagom-threading.so.0 (0x00007ffff01b6000)
        libGLdispatch.so.0 => /lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x00007ffff00fc000)
        libexpat.so.1 => /lib/x86_64-linux-gnu/libexpat.so.1 (0x00007ffff00d1000)
        libxcb.so.1 => /lib/x86_64-linux-gnu/libxcb.so.1 (0x00007ffff00a8000)
        libgraphite2.so.3 => /lib/x86_64-linux-gnu/libgraphite2.so.3 (0x00007ffff0082000)
        libbz2.so.1.0 => /lib/x86_64-linux-gnu/libbz2.so.1.0 (0x00007ffff006e000)
        libsndfile.so.1 => /lib/x86_64-linux-gnu/libsndfile.so.1 (0x00007fffeffe4000)
        libX11-xcb.so.1 => /lib/x86_64-linux-gnu/libX11-xcb.so.1 (0x00007fffeffdf000)
        libsystemd.so.0 => /lib/x86_64-linux-gnu/libsystemd.so.0 (0x00007fffefeff000)
        libasyncns.so.0 => /lib/x86_64-linux-gnu/libasyncns.so.0 (0x00007fffefef7000)
        libapparmor.so.1 => /lib/x86_64-linux-gnu/libapparmor.so.1 (0x00007fffefee3000)
        libkeyutils.so.1 => /lib/x86_64-linux-gnu/libkeyutils.so.1 (0x00007fffefeda000)
        libresolv.so.2 => /lib/x86_64-linux-gnu/libresolv.so.2 (0x00007fffefec7000)
        libcurl-gnutls.so.4 => /lib/x86_64-linux-gnu/libcurl-gnutls.so.4 (0x00007fffefe0c000)
        libgio-2.0.so.0 => /lib/x86_64-linux-gnu/libgio-2.0.so.0 (0x00007fffefc3c000)
        libduktape.so.207 => /lib/x86_64-linux-gnu/libduktape.so.207 (0x00007fffefbf1000)
        libffi.so.8 => /lib/x86_64-linux-gnu/libffi.so.8 (0x00007fffefbe3000)
        libXau.so.6 => /lib/x86_64-linux-gnu/libXau.so.6 (0x00007fffefbdd000)
        libXdmcp.so.6 => /lib/x86_64-linux-gnu/libXdmcp.so.6 (0x00007fffefbd5000)
        libFLAC.so.12 => /lib/x86_64-linux-gnu/libFLAC.so.12 (0x00007fffefb71000)
        libvorbis.so.0 => /lib/x86_64-linux-gnu/libvorbis.so.0 (0x00007fffefb43000)
        libvorbisenc.so.2 => /lib/x86_64-linux-gnu/libvorbisenc.so.2 (0x00007fffefa96000)
        libopus.so.0 => /lib/x86_64-linux-gnu/libopus.so.0 (0x00007fffefa37000)
        libogg.so.0 => /lib/x86_64-linux-gnu/libogg.so.0 (0x00007fffefa2d000)
        libmpg123.so.0 => /lib/x86_64-linux-gnu/libmpg123.so.0 (0x00007fffef9d1000)
        libmp3lame.so.0 => /lib/x86_64-linux-gnu/libmp3lame.so.0 (0x00007fffef95b000)
        libcap.so.2 => /lib/x86_64-linux-gnu/libcap.so.2 (0x00007fffef94c000)
        libgcrypt.so.20 => /lib/x86_64-linux-gnu/libgcrypt.so.20 (0x00007fffef804000)
        liblz4.so.1 => /lib/x86_64-linux-gnu/liblz4.so.1 (0x00007fffef7e2000)
        liblzma.so.5 => /lib/x86_64-linux-gnu/liblzma.so.5 (0x00007fffef7b0000)
        libnghttp2.so.14 => /lib/x86_64-linux-gnu/libnghttp2.so.14 (0x00007fffef785000)
        libidn2.so.0 => /lib/x86_64-linux-gnu/libidn2.so.0 (0x00007fffef761000)
        librtmp.so.1 => /lib/x86_64-linux-gnu/librtmp.so.1 (0x00007fffef743000)
        libssh.so.4 => /lib/x86_64-linux-gnu/libssh.so.4 (0x00007fffef6d2000)
        libpsl.so.5 => /lib/x86_64-linux-gnu/libpsl.so.5 (0x00007fffef6be000)
        libnettle.so.8 => /lib/x86_64-linux-gnu/libnettle.so.8 (0x00007fffef669000)
        libgnutls.so.30 => /lib/x86_64-linux-gnu/libgnutls.so.30 (0x00007fffef46f000)
        libldap.so.2 => /lib/x86_64-linux-gnu/libldap.so.2 (0x00007fffef410000)
        liblber.so.2 => /lib/x86_64-linux-gnu/liblber.so.2 (0x00007fffef400000)
        libgmodule-2.0.so.0 => /lib/x86_64-linux-gnu/libgmodule-2.0.so.0 (0x00007fffef3f9000)
        libmount.so.1 => /lib/x86_64-linux-gnu/libmount.so.1 (0x00007fffef3ac000)
        libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1 (0x00007fffef37f000)
        libbsd.so.0 => /lib/x86_64-linux-gnu/libbsd.so.0 (0x00007fffef367000)
        libgpg-error.so.0 => /lib/x86_64-linux-gnu/libgpg-error.so.0 (0x00007fffef342000)
        libunistring.so.5 => /lib/x86_64-linux-gnu/libunistring.so.5 (0x00007fffef195000)
        libhogweed.so.6 => /lib/x86_64-linux-gnu/libhogweed.so.6 (0x00007fffef14d000)
        libgmp.so.10 => /lib/x86_64-linux-gnu/libgmp.so.10 (0x00007fffef0c9000)
        libcrypto.so.3 => /lib/x86_64-linux-gnu/libcrypto.so.3 (0x00007fffeebb4000)
        libp11-kit.so.0 => /lib/x86_64-linux-gnu/libp11-kit.so.0 (0x00007fffeea10000)
        libtasn1.so.6 => /lib/x86_64-linux-gnu/libtasn1.so.6 (0x00007fffee9fa000)
        libsasl2.so.2 => /lib/x86_64-linux-gnu/libsasl2.so.2 (0x00007fffee9e0000)
        libblkid.so.1 => /lib/x86_64-linux-gnu/libblkid.so.1 (0x00007fffee9a5000)
        libmd.so.0 => /lib/x86_64-linux-gnu/libmd.so.0 (0x00007fffee994000)
"""

# Extract library paths using regex
library_paths = re.findall(r'=>\s*(\S+)', libraries)

# Run readelf -n for each library path
for path in library_paths:
    try:
        print(f"Running readelf -n on: {path}\n")
        result = subprocess.run(["readelf", "-n", path], capture_output=True, text=True, check=True)
        if "SHSTK" not in result.stdout:
                print("**************************************SHSTK ABSENT!!******************************************************")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running readelf on {path}: {e.stderr}\n")
    except FileNotFoundError:
        print("readelf command not found. Please ensure it is installed and available in PATH.")
        break
