import subprocess
import re

# Input: The list of libraries
libraries = """
0x00007ffff7fc6000  0x00007ffff7ff0195  Yes         /lib64/ld-linux-x86-64.so.2
0x00007ffff7faad40  0x00007ffff7fb47f6  Yes         /cfop/Build/lagom/lib/liblagom-imagedecoderclient.so.0
0x00007ffff7e6b640  0x00007ffff7f04906  Yes         /cfop/Build/lagom/lib/liblagom-webview.so.0
0x00007ffff7d7a180  0x00007ffff7d9573f  Yes         /cfop/Build/lagom/lib/liblagom-protocol.so.0
0x00007ffff7c1a660  0x00007ffff7d0d861  Yes (*)     /lib/x86_64-linux-gnu/libQt6Network.so.6
0x00007ffff760d6e0  0x00007ffff7a54567  Yes (*)     /lib/x86_64-linux-gnu/libQt6Widgets.so.6
0x00007ffff6e7bf00  0x00007ffff7344fab  Yes (*)     /lib/x86_64-linux-gnu/libQt6Gui.so.6
0x00007ffff6902cc0  0x00007ffff6be7dcb  Yes (*)     /lib/x86_64-linux-gnu/libQt6Core.so.6
0x00007ffff67ec820  0x00007ffff6839fe6  Yes         /cfop/Build/lagom/lib/liblagom-sql.so.0
0x00007ffff55e1ce0  0x00007ffff6280257  Yes         /cfop/Build/lagom/lib/liblagom-web.so.0
0x00007ffff4c4a400  0x00007ffff4e0651c  Yes         /cfop/Build/lagom/lib/liblagom-gfx.so.0
0x00007ffff67c7960  0x00007ffff67ccac2  Yes         /cfop/Build/lagom/lib/liblagom-filesystem.so.0
0x00007ffff67aed00  0x00007ffff67b9803  Yes         /cfop/Build/lagom/lib/liblagom-ipc.so.0
0x00007ffff4f7b500  0x00007ffff4faab97  Yes         /cfop/Build/lagom/lib/liblagom-core.so.0
0x00007ffff4b9f040  0x00007ffff4bb342f  Yes         /cfop/Build/lagom/lib/liblagom-corebasic.so.0
0x00007ffff4f38200  0x00007ffff4f52daa  Yes         /cfop/Build/lagom/lib/liblagom-coreminimal.so.0
0x00007ffff4f15ae0  0x00007ffff4f22d61  Yes         /cfop/Build/lagom/lib/liblagom-url.so.0
0x00007ffff4b2bb40  0x00007ffff4b6cbc6  Yes         /cfop/Build/lagom/lib/liblagom-ak.so.0
0x00007ffff493f5c0  0x00007ffff4a7ece2  Yes (*)     /lib/x86_64-linux-gnu/libstdc++.so.6
0x00007ffff46b0800  0x00007ffff4837c8d  Yes         /lib/x86_64-linux-gnu/libc.so.6
0x00007ffff4136e50  0x00007ffff44d4ea7  Yes         /cfop/Build/lagom/lib/liblagom-js.so.0
0x00007ffff6799260  0x00007ffff67a04b8  Yes         /cfop/Build/lagom/lib/liblagom-syntax.so.0
0x00007ffff3c04a40  0x00007ffff3c13cdb  Yes         /cfop/Build/lagom/lib/liblagom-unicode.so.0
0x00007ffff3b27420  0x00007ffff3ba5418  Yes         /lib/x86_64-linux-gnu/libm.so.6
0x00007ffff3fba470  0x00007ffff3ff1b78  Yes (*)     /lib/x86_64-linux-gnu/libgssapi_krb5.so.2
0x00007ffff467b1a0  0x00007ffff4682b6a  Yes (*)     /lib/x86_64-linux-gnu/libbrotlidec.so.1
0x00007ffff3a61400  0x00007ffff3b077b2  Yes (*)     /lib/x86_64-linux-gnu/libzstd.so.1
0x00007ffff4660260  0x00007ffff4671c40  Yes (*)     /lib/x86_64-linux-gnu/libz.so.1
0x00007ffff4f0d1c0  0x00007ffff4f0d3e1  Yes (*)     /lib/x86_64-linux-gnu/libproxy.so.1
0x00007ffff3f82780  0x00007ffff3fa5745  Yes (*)     /lib/x86_64-linux-gnu/libgcc_s.so.1
0x00007ffff464f7c0  0x00007ffff46586fc  Yes (*)     /lib/x86_64-linux-gnu/libEGL.so.1
0x00007ffff3a14f90  0x00007ffff3a422ee  Yes (*)     /lib/x86_64-linux-gnu/libfontconfig.so.1
0x00007ffff38e9100  0x00007ffff3977fde  Yes (*)     /lib/x86_64-linux-gnu/libX11.so.6
0x00007ffff37a5e90  0x00007ffff3843362  Yes (*)     /lib/x86_64-linux-gnu/libglib-2.0.so.0
0x00007ffff36f3740  0x00007ffff37667b2  Yes (*)     /lib/x86_64-linux-gnu/libQt6DBus.so.6
0x00007ffff368d5a0  0x00007ffff36ac672  Yes (*)     /lib/x86_64-linux-gnu/libxkbcommon.so.0
0x00007ffff3658700  0x00007ffff3672371  Yes (*)     /lib/x86_64-linux-gnu/libGLX.so.0
0x00007ffff363f1c0  0x00007ffff363f638  Yes (*)     /lib/x86_64-linux-gnu/libOpenGL.so.0
0x00007ffff35f7510  0x00007ffff361e488  Yes (*)     /lib/x86_64-linux-gnu/libpng16.so.16
0x00007ffff34f0e90  0x00007ffff35bd1e2  Yes (*)     /lib/x86_64-linux-gnu/libharfbuzz.so.0
0x00007ffff34d51a0  0x00007ffff34dff9a  Yes (*)     /lib/x86_64-linux-gnu/libmd4c.so.0
0x00007ffff34147f0  0x00007ffff34a462a  Yes (*)     /lib/x86_64-linux-gnu/libfreetype.so.6
0x00007ffff31abf70  0x00007ffff3369dd9  Yes (*)     /lib/x86_64-linux-gnu/libicui18n.so.74
0x00007ffff2f14940  0x00007ffff3018bea  Yes (*)     /lib/x86_64-linux-gnu/libicuuc.so.74
0x00007ffff2e99200  0x00007ffff2ea492c  Yes (*)     /lib/x86_64-linux-gnu/libdouble-conversion.so.3
0x00007ffff2e7c120  0x00007ffff2e9224d  Yes (*)     /lib/x86_64-linux-gnu/libb2.so.1
0x00007ffff2def2a0  0x00007ffff2e4f645  Yes (*)     /lib/x86_64-linux-gnu/libpcre2-16.so.0
0x00007ffff2d894a0  0x00007ffff2dd456f  Yes         /cfop/Build/lagom/lib/liblagom-regex.so.0
0x00007ffff2d5fbc0  0x00007ffff2d6f1af  Yes         /cfop/Build/lagom/lib/liblagom-markdown.so.0
0x00007ffff2d34dc0  0x00007ffff2d4968f  Yes         /cfop/Build/lagom/lib/liblagom-http.so.0
0x00007ffff2c92f40  0x00007ffff2cc7eca  Yes         /cfop/Build/lagom/lib/liblagom-audio.so.0
0x00007ffff2c0b4e0  0x00007ffff2c626ec  Yes         /cfop/Build/lagom/lib/liblagom-media.so.0
0x00007ffff2b16d80  0x00007ffff2bbb30d  Yes         /cfop/Build/lagom/lib/liblagom-wasm.so.0
0x00007ffff2a9f700  0x00007ffff2abeaea  Yes         /cfop/Build/lagom/lib/liblagom-xml.so.0
0x00007ffff2a748c0  0x00007ffff2a8e9de  Yes         /cfop/Build/lagom/lib/liblagom-idl.so.0
0x00007ffff2a01860  0x00007ffff2a4fbd6  Yes         /cfop/Build/lagom/lib/liblagom-tls.so.0
0x00007ffff29e1ee0  0x00007ffff29eadc0  Yes         /cfop/Build/lagom/lib/liblagom-accelgfx.so.0
0x00007ffff2997560  0x00007ffff29c7105  Yes         /cfop/Build/lagom/lib/liblagom-crypto.so.0
0x00007ffff291d440  0x00007ffff2930533  Yes         /cfop/Build/lagom/lib/liblagom-textcodec.so.0
0x00007ffff28c18c0  0x00007ffff28e5fb0  Yes         /cfop/Build/lagom/lib/liblagom-compress.so.0
0x00007ffff28ae320  0x00007ffff28b0b95  Yes         /cfop/Build/lagom/lib/liblagom-riff.so.0
0x00007ffff2874040  0x00007ffff288810e  Yes (*)     /lib/x86_64-linux-gnu/libcrypt.so.1
0x00007ffff1e5dc60  0x00007ffff1e7a6df  Yes         /cfop/Build/lagom/lib/liblagom-locale.so.0
0x00007ffff1d58f30  0x00007ffff1db714e  Yes (*)     /lib/x86_64-linux-gnu/libkrb5.so.3
0x00007ffff284a3c0  0x00007ffff2864611  Yes (*)     /lib/x86_64-linux-gnu/libk5crypto.so.3
0x00007ffff28423c0  0x00007ffff2842fc1  Yes (*)     /lib/x86_64-linux-gnu/libcom_err.so.2
0x00007ffff2836630  0x00007ffff283b934  Yes (*)     /lib/x86_64-linux-gnu/libkrb5support.so.0
0x00007ffff1d150a0  0x00007ffff1d157be  Yes (*)     /lib/x86_64-linux-gnu/libbrotlicommon.so.1
0x00007ffff1d09f40  0x00007ffff1d0e1f5  Yes (*)     /usr/lib/x86_64-linux-gnu/libproxy/libpxbackend-1.0.so
0x00007ffff1cb3110  0x00007ffff1ce83d0  Yes (*)     /lib/x86_64-linux-gnu/libgobject-2.0.so.0
0x00007ffff1c2c2c0  0x00007ffff1c2e42f  Yes (*)     /lib/x86_64-linux-gnu/libGLdispatch.so.0
0x00007ffff1bc4210  0x00007ffff1bdfcf3  Yes (*)     /lib/x86_64-linux-gnu/libexpat.so.1
0x00007ffff1ba2660  0x00007ffff1bb4ebe  Yes (*)     /lib/x86_64-linux-gnu/libxcb.so.1
0x00007ffff1aff300  0x00007ffff1b6c210  Yes (*)     /lib/x86_64-linux-gnu/libpcre2-8.so.0
0x00007ffff1abaf10  0x00007ffff1ae97bb  Yes (*)     /lib/x86_64-linux-gnu/libdbus-1.so.3
0x00007ffff1a8b240  0x00007ffff1aa7d4d  Yes (*)     /lib/x86_64-linux-gnu/libgraphite2.so.3
0x00007ffff1a76280  0x00007ffff1a82ff3  Yes (*)     /lib/x86_64-linux-gnu/libbz2.so.1.0
0x00007fffefd15040  0x00007fffefd150f9  Yes (*)     /lib/x86_64-linux-gnu/libicudata.so.74
0x00007fffefcc9f00  0x00007fffefd04ce2  Yes (*)     /lib/x86_64-linux-gnu/libgomp.so.1
0x00007fffefcb7440  0x00007fffefcb9e28  Yes         /cfop/Build/lagom/lib/liblagom-threading.so.0
0x00007fffefcaf260  0x00007fffefcb04c8  Yes (*)     /lib/x86_64-linux-gnu/libkeyutils.so.1
0x00007fffefc9d6e0  0x00007fffefca6379  Yes         /lib/x86_64-linux-gnu/libresolv.so.2
0x00007fffefbf1d90  0x00007fffefc76203  Yes (*)     /lib/x86_64-linux-gnu/libcurl-gnutls.so.4
0x00007fffefa4f7e0  0x00007fffefb5e756  Yes (*)     /lib/x86_64-linux-gnu/libgio-2.0.so.0
0x00007fffef9cca60  0x00007fffef9fc8d6  Yes (*)     /lib/x86_64-linux-gnu/libduktape.so.207
0x00007fffef9ba460  0x00007fffef9c007a  Yes (*)     /lib/x86_64-linux-gnu/libffi.so.8
0x00007fffef9b3360  0x00007fffef9b4042  Yes (*)     /lib/x86_64-linux-gnu/libXau.so.6
0x00007fffef9ac1a0  0x00007fffef9ada89  Yes (*)     /lib/x86_64-linux-gnu/libXdmcp.so.6
0x00007fffef8dfe20  0x00007fffef96c6c0  Yes (*)     /lib/x86_64-linux-gnu/libsystemd.so.0
0x00007fffef8a2200  0x00007fffef8b755b  Yes (*)     /lib/x86_64-linux-gnu/libnghttp2.so.14
0x00007fffef87d3e0  0x00007fffef8809b9  Yes (*)     /lib/x86_64-linux-gnu/libidn2.so.0
0x00007fffef862da0  0x00007fffef8725a1  Yes (*)     /lib/x86_64-linux-gnu/librtmp.so.1
0x00007fffef7fc600  0x00007fffef840c41  Yes (*)     /lib/x86_64-linux-gnu/libssh.so.4
0x00007fffef7d83e0  0x00007fffef7d9fa0  Yes (*)     /lib/x86_64-linux-gnu/libpsl.so.5
0x00007fffef78d280  0x00007fffef7bb285  Yes (*)     /lib/x86_64-linux-gnu/libnettle.so.8
0x00007fffef5bcd00  0x00007fffef6f20fd  Yes (*)     /lib/x86_64-linux-gnu/libgnutls.so.30
0x00007fffef539fe0  0x00007fffef572f12  Yes (*)     /lib/x86_64-linux-gnu/libldap.so.2
0x00007fffef51d360  0x00007fffef524741  Yes (*)     /lib/x86_64-linux-gnu/liblber.so.2
0x00007fffef513500  0x00007fffef5145d2  Yes (*)     /lib/x86_64-linux-gnu/libgmodule-2.0.so.0
0x00007fffef4ce380  0x00007fffef5000ec  Yes (*)     /lib/x86_64-linux-gnu/libmount.so.1
0x00007fffef49e040  0x00007fffef4b95bc  Yes (*)     /lib/x86_64-linux-gnu/libselinux.so.1
0x00007fffef485de0  0x00007fffef4904f6  Yes (*)     /lib/x86_64-linux-gnu/libbsd.so.0
0x00007fffef477980  0x00007fffef47c517  Yes (*)     /lib/x86_64-linux-gnu/libcap.so.2
0x00007fffef339ac0  0x00007fffef42c0de  Yes (*)     /lib/x86_64-linux-gnu/libgcrypt.so.20
0x00007fffef30b180  0x00007fffef325e8c  Yes (*)     /lib/x86_64-linux-gnu/liblz4.so.1
0x00007fffef2d9400  0x00007fffef2fa5ef  Yes (*)     /lib/x86_64-linux-gnu/liblzma.so.5
0x00007fffef13a7a0  0x00007fffef170b85  Yes (*)     /lib/x86_64-linux-gnu/libunistring.so.5
0x00007fffef0e9ca0  0x00007fffef0fc9bd  Yes (*)     /lib/x86_64-linux-gnu/libhogweed.so.6
0x00007fffef065240  0x00007fffef0c7192  Yes (*)     /lib/x86_64-linux-gnu/libgmp.so.10
0x00007fffeebfd000  0x00007fffeef2df72  Yes (*)     /lib/x86_64-linux-gnu/libcrypto.so.3
0x00007fffee9dcc80  0x00007fffeeaad9f0  Yes (*)     /lib/x86_64-linux-gnu/libp11-kit.so.0
0x00007fffee9914a0  0x00007fffee99ed05  Yes (*)     /lib/x86_64-linux-gnu/libtasn1.so.6
0x00007fffee977950  0x00007fffee986aea  Yes (*)     /lib/x86_64-linux-gnu/libsasl2.so.2
0x00007fffee93ed40  0x00007fffee961657  Yes (*)     /lib/x86_64-linux-gnu/libblkid.so.1
0x00007fffee92a160  0x00007fffee932a7a  Yes (*)     /lib/x86_64-linux-gnu/libmd.so.0
0x00007fffee907a20  0x00007fffee91cd72  Yes (*)     /lib/x86_64-linux-gnu/libgpg-error.so.0
0x00007fffee888240  0x00007fffee888629  Yes (*)     /usr/lib/x86_64-linux-gnu/qt6/plugins/platforms/libqxcb.so
0x00007fffee808700  0x00007fffee86568b  Yes (*)     /lib/x86_64-linux-gnu/libQt6XcbQpa.so.6
0x00007fffee7d7160  0x00007fffee7d819d  Yes (*)     /lib/x86_64-linux-gnu/libxcb-icccm.so.4
0x00007fffee7d0300  0x00007fffee7d19b5  Yes (*)     /lib/x86_64-linux-gnu/libxcb-image.so.0
0x00007fffee7cb140  0x00007fffee7cb9b6  Yes (*)     /lib/x86_64-linux-gnu/libxcb-keysyms.so.1
0x00007fffee7c00c0  0x00007fffee7c4c57  Yes (*)     /lib/x86_64-linux-gnu/libxcb-randr.so.0
0x00007fffee7af120  0x00007fffee7b3ccb  Yes (*)     /lib/x86_64-linux-gnu/libxcb-render.so.0
0x00007fffee7a5400  0x00007fffee7a6326  Yes (*)     /lib/x86_64-linux-gnu/libxcb-render-util.so.0
0x00007fffee79f0a0  0x00007fffee79fc19  Yes (*)     /lib/x86_64-linux-gnu/libxcb-shape.so.0
0x00007fffee79a0e0  0x00007fffee79ab07  Yes (*)     /lib/x86_64-linux-gnu/libxcb-shm.so.0
0x00007fffee793100  0x00007fffee7952c6  Yes (*)     /lib/x86_64-linux-gnu/libxcb-sync.so.1
0x00007fffee7890a0  0x00007fffee78b789  Yes (*)     /lib/x86_64-linux-gnu/libxcb-xfixes.so.0
0x00007fffee772120  0x00007fffee77ea09  Yes (*)     /lib/x86_64-linux-gnu/libxcb-xkb.so.1
0x00007fffee764040  0x00007fffee76411f  Yes (*)     /lib/x86_64-linux-gnu/libX11-xcb.so.1
0x00007fffee75b4c0  0x00007fffee75f809  Yes (*)     /lib/x86_64-linux-gnu/libSM.so.6
0x00007fffee741ac0  0x00007fffee74f9d8  Yes (*)     /lib/x86_64-linux-gnu/libICE.so.6
0x00007fffee736b60  0x00007fffee7398d6  Yes (*)     /lib/x86_64-linux-gnu/libxkbcommon-x11.so.0
0x00007fffee72e380  0x00007fffee72f181  Yes (*)     /lib/x86_64-linux-gnu/libxcb-util.so.1
0x00007fffee723500  0x00007fffee7272fb  Yes (*)     /lib/x86_64-linux-gnu/libuuid.so.1
0x00007fffee717660  0x00007fffee71c5ec  Yes (*)     /lib/x86_64-linux-gnu/libXcursor.so.1
0x00007fffee70b440  0x00007fffee711787  Yes (*)     /lib/x86_64-linux-gnu/libXrender.so.1
0x00007fffee703300  0x00007fffee705a4a  Yes (*)     /lib/x86_64-linux-gnu/libXfixes.so.3
0x00007fffee881680  0x00007fffee8824d9  Yes (*)     /usr/lib/x86_64-linux-gnu/qt6/plugins/platforminputcontexts/libcomposeplatforminputcontextplugin.so
0x00007fffee6fa700  0x00007fffee6fdac7  Yes (*)     /usr/lib/x86_64-linux-gnu/qt6/plugins/imageformats/libqgif.so
0x00007fffee6eefe0  0x00007fffee6f3729  Yes (*)     /usr/lib/x86_64-linux-gnu/qt6/plugins/imageformats/libqjpeg.so
0x00007fffee663580  0x00007fffee6af720  Yes (*)     /lib/x86_64-linux-gnu/libjpeg.so.8
0x00007fffee6588e0  0x00007fffee65b32b  Yes (*)     /usr/lib/x86_64-linux-gnu/qt6/plugins/imageformats/libqico.so
"""

# Extract library paths using regex
library_paths = re.findall(r'\/[^\s]+', libraries)

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
