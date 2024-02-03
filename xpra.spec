# TODO
# - test and finish systemd integration
# - subpackages for client/server, see http://xpra.org/dev.html
# - nvenc>=7 for cuda support (on bcond)
# - nvfbc (on bcond)
# - nvjpeg (on bcond)
#
# Conditional build:
%bcond_without	client		# client part
%bcond_without	doc		# HTML documentation
%bcond_without	server		# server part
%bcond_without	sound		# (gstreamer) sound support
%bcond_without	clipboard	# clipboard support
%bcond_without	swscale		# swscale colorspace conversion support
%bcond_without	opengl		# OpenGL support
%bcond_without	ffmpeg		# avcodec decoding / FFmpeg encoding support
%bcond_without	vpx		# VPX/WebM support
%bcond_without	webp		# WebP support
%bcond_without	x264		# x264 encoding
%bcond_without	x265		# x265 encoding

%ifarch i386 i486 x32
%undefine	with_x265
%endif

Summary:	Xpra gives you "persistent remote applications" for X
Summary(pl.UTF-8):	Xpra - "stałe zdalne aplikacje" dla X
Name:		xpra
Version:	5.0.4
Release:	1
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://xpra.org/src/%{name}-%{version}.tar.xz
# Source0-md5:	e5cf620739abcc8a089e934f388ecda4
Patch0:		%{name}-evdi.patch
URL:		http://xpra.org/
BuildRequires:	OpenGL-devel
BuildRequires:	cairo-devel
BuildRequires:	evdi-devel >= 1.9
# libavcodec >= 57 for dec_avcodec, libavcodec >= 58.18 for enc_ffmpeg, libswscale
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 3.4}
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	libavif-devel >= 0.9
BuildRequires:	libbrotli-devel
BuildRequires:	libdrm-devel >= 2.4
BuildRequires:	libjpeg-turbo-devel >= 1.4
BuildRequires:	libspng-devel >= 0.7
BuildRequires:	libvpx-devel >= 1.7
BuildRequires:	libwebp-devel >= 0.5
# ABI 155
%{?with_x264:BuildRequires:	libx264-devel}
%{?with_x265:BuildRequires:	libx265-devel}
BuildRequires:	libyuv-devel
BuildRequires:	lz4-devel
BuildRequires:	openh264-devel >= 2.0
BuildRequires:	pam-devel
# with --lua-filter option
%{?with_doc:BuildRequires:	pandoc >= 2.0}
BuildRequires:	pkgconfig
BuildRequires:	procps-devel >= 1:4.0
BuildRequires:	python3-Cython >= 0.20
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-pycairo-devel
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	python3-setuptools
BuildRequires:	qrencode-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXres-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xz
Requires:	evdi >= 1.9
Requires:	gdk-pixbuf2 >= 2.0
Requires:	glib2 >= 2.0
Requires:	gobject-introspection >= 1
Requires:	gtk+3 >= 3.0
Requires:	libjpeg-turbo >= 1.4
Requires:	libspng >= 0.7
Requires:	libvpx >= 1.7
Requires:	libwebp >= 0.5
Requires:	python3-pycairo
Requires:	python3-pygobject3 >= 3.0
Requires:	xorg-app-setxkbmap
Requires:	xorg-app-xauth
Requires:	xorg-app-xmodmap
Requires:	xorg-xserver-Xvfb
Suggests:	python3-PIL
Suggests:	python3-PyOpenGL
Suggests:	python3-numpy
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# currently lib, not %{_lib} (see cups.spec)
%define		cupsdir		/usr/lib/cups/backend
# xpra/x11/bindings/randr_bindings.c:... error: dereferencing type-punned pointer will break strict-aliasing rules [-Werror=strict-aliasing]
%define		specflags	-fno-strict-aliasing

%description
Xpra gives you "persistent remote applications" for X. That is, unlike
normal X applications, applications run with xpra are "persistent" --
you can run them remotely, and they don't die if your connection does.
You can detach them, and reattach them later -- even from another
computer -- with no loss of state. And unlike VNC or RDP, xpra is for
remote applications, not remote desktops -- individual applications
show up as individual windows on your screen, managed by your window
manager. They're not trapped in a box.

So basically it's screen for remote X apps.

%description -l pl.UTF-8
Xpra daje "stałe zdalne aplikacje" dla serwera X, które w
przeciwieństwie do zwykłych X-owych aplikacji, uruchamiane są z xprą
jako niezamykające. Można je uruchomić zdalnie i one nie zostaną
zamknięte, gdy połączenie zostanie przerwane. Można je odłączyć i
podłączyć z powrotem później, również z innego komputera, bez straty
stanu. W odróżnieniu od VNC czy RDP, xpra jest dla zdalnych aplikacji,
a nie zdalnych pulpitów - pojedyncze aplikacje pokazują się jako
samodzielne okno na lokalnym ekranie, zarządzane przez lokalnego
zarządcę okien.

W uproszczeniu xpra to "screen" dla zdalnych aplikacji X-owych.

%package -n cups-backend-xpra
Summary:	Xpra backend for CUPS
Summary(pl.UTF-8):	Backend Xpra dla CUPS-a
Group:		Applications/Printing
Requires:	%{name} = %{version}-%{release}
Requires:	cups

%description -n cups-backend-xpra
Xpra backend for CUPS.

%description -n cups-backend-xpra -l pl.UTF-8
Backend Xpra dla CUPS-a.

%prep
%setup -q
%patch0 -p1

libexecdir="%{_libexecdir}"
%{__sed} -i -e 's,"libexec","'${libexecdir#%{_prefix}/}'",' setup.py

%define setup_opts \\\
	--with-PIC \\\
	--with-Xdummy \\\
	--with-Xdummy_wrapper \\\
	%{__with_without client} \\\
	%{__with_without clipboard} \\\
	%{__with_without swscale csc_swscale} \\\
	--with%{!?debug:out}-debug \\\
	%{!?with_doc:--without-docs} \\\
	%{__with_without ffmpeg} \\\
	%{__with_without ffmpeg dec_avcodec2} \\\
	%{__with_without ffmpeg enc_ffmpeg} \\\
	%{__with_without x264 enc_x264} \\\
	--with-gtk3 \\\
	--without-nvenc \\\
	--without-nvfbc \\\
	%{__with_without opengl} \\\
	%{__with_without server} \\\
	%{__with_without server shadow} \\\
	--without-strict \\\
	%{__with_without vpx} \\\
	--with-warn \\\
	%{__with_without webp} \\\
	--with-x11 \\\
	%{nil}

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python3} setup.py build \
	%{setup_opts}

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} setup.py install \
	%{setup_opts} \
	--skip-build \
	--prefix=%{_prefix} \
	--install-purelib=%{py3_sitescriptdir} \
	--install-platlib=%{py3_sitedir} \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/COPYING
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/README.md

install -d $RPM_BUILD_ROOT/lib/udev/rules.d
%{__mv} $RPM_BUILD_ROOT{%{_prefix},}/lib/udev/rules.d/71-xpra-virtual-pointer.rules

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xorg.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xpra.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xorg-uinput.conf
%dir %{_sysconfdir}/%{name}/conf.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/05_features.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/10_network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/12_ssl.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/15_file_transfers.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/16_printing.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/20_audio.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/30_picture.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/35_webcam.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/40_client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/42_client_keyboard.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/50_server_network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/55_server_x11.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/60_server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/65_proxy.conf
%dir %{_sysconfdir}/%{name}/content-categories
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-categories/10_default.conf
%dir %{_sysconfdir}/%{name}/content-parent
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-parent/10_default.conf
%dir %{_sysconfdir}/%{name}/content-type
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-type/10_role.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-type/30_title.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-type/50_class.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/content-type/70_commands.conf
%dir %{_sysconfdir}/%{name}/http-headers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/http-headers/00_nocache.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/http-headers/10_content_security_policy.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xorg.conf.d/90-xpra-virtual.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/xpra
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xpra
/etc/dbus-1/system.d/xpra.conf
%{systemdunitdir}/xpra.service
%{systemdunitdir}/xpra.socket
/usr/lib/sysusers.d/xpra.conf
/lib/udev/rules.d/71-xpra-virtual-pointer.rules
%attr(755,root,root) %{_bindir}/run_scaled
%attr(755,root,root) %{_bindir}/xpra
%attr(755,root,root) %{_bindir}/xpra_Xdummy
%attr(755,root,root) %{_bindir}/xpra_launcher
%dir %{_libexecdir}/xpra
%attr(755,root,root) %{_libexecdir}/xpra/auth_dialog
%attr(755,root,root) %{_libexecdir}/xpra/gnome-open
%attr(755,root,root) %{_libexecdir}/xpra/gvfs-open
%attr(755,root,root) %{_libexecdir}/xpra/xdg-open
%attr(755,root,root) %{_libexecdir}/xpra/xpra_signal_listener
%attr(755,root,root) %{_libexecdir}/xpra/xpra_udev_product_version
%{_datadir}/mime/packages/application-x-xpraconfig.xml
%{_datadir}/xpra
%{_desktopdir}/xpra.desktop
%{_desktopdir}/xpra-gui.desktop
%{_desktopdir}/xpra-launcher.desktop
%{_desktopdir}/xpra-shadow.desktop
%if %{with doc}
%{_docdir}/xpra
%endif
%{_iconsdir}/xpra.png
%{_iconsdir}/xpra-mdns.png
%{_iconsdir}/xpra-shadow.png
%{_datadir}/metainfo/xpra.appdata.xml
%{systemdtmpfilesdir}/xpra.conf
# specified in the above (xpra group seems to be optional though)
#%attr(770,root,xpra) %dir /run/xpra
%{_mandir}/man1/run_scaled.1*
%{_mandir}/man1/xpra.1*
%{_mandir}/man1/xpra_launcher.1*

%dir %{py3_sitedir}/xpra
%attr(755,root,root) %{py3_sitedir}/xpra/rectangle.cpython-*.so
%{py3_sitedir}/xpra/*.py
%{py3_sitedir}/xpra/__pycache__
%dir %{py3_sitedir}/xpra/audio
%{py3_sitedir}/xpra/audio/*.py
%{py3_sitedir}/xpra/audio/__pycache__
%dir %{py3_sitedir}/xpra/audio/pulseaudio
%{py3_sitedir}/xpra/audio/pulseaudio/*.py
%{py3_sitedir}/xpra/audio/pulseaudio/__pycache__
%dir %{py3_sitedir}/xpra/buffers
%{py3_sitedir}/xpra/buffers/*.py
%{py3_sitedir}/xpra/buffers/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/buffers/cyxor.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/buffers/membuf.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/buffers/xxh.cpython-*.so
%dir %{py3_sitedir}/xpra/client
%dir %{py3_sitedir}/xpra/client/auth
%{py3_sitedir}/xpra/client/auth/*.py
%{py3_sitedir}/xpra/client/auth/__pycache__
%dir %{py3_sitedir}/xpra/client/base
%{py3_sitedir}/xpra/client/base/*.py
%{py3_sitedir}/xpra/client/base/__pycache__
%{py3_sitedir}/xpra/client/gl
%dir %{py3_sitedir}/xpra/client/gtk3
%attr(755,root,root) %{py3_sitedir}/xpra/client/gtk3/cairo_workaround.cpython-*.so
%{py3_sitedir}/xpra/client/gtk3/*.py
%{py3_sitedir}/xpra/client/gtk3/__pycache__
%{py3_sitedir}/xpra/client/gtk3/example
%dir %{py3_sitedir}/xpra/client/gui
%{py3_sitedir}/xpra/client/gui/*.py
%{py3_sitedir}/xpra/client/gui/__pycache__
%{py3_sitedir}/xpra/client/mixins
%{py3_sitedir}/xpra/client/*.py
%{py3_sitedir}/xpra/client/__pycache__
%{py3_sitedir}/xpra/clipboard
%dir %{py3_sitedir}/xpra/codecs
%{py3_sitedir}/xpra/codecs/*.py
%{py3_sitedir}/xpra/codecs/__pycache__
%dir %{py3_sitedir}/xpra/codecs/argb
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/argb/argb.cpython-*.so
%{py3_sitedir}/xpra/codecs/argb/*.py
%{py3_sitedir}/xpra/codecs/argb/__pycache__
%if %{with ffmpeg}
%dir %{py3_sitedir}/xpra/codecs/avif
%{py3_sitedir}/xpra/codecs/avif/*.py
%{py3_sitedir}/xpra/codecs/avif/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/avif/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/avif/encoder.cpython-*.so
%endif
%dir %{py3_sitedir}/xpra/codecs/csc_cython
%{py3_sitedir}/xpra/codecs/csc_cython/*.py
%{py3_sitedir}/xpra/codecs/csc_cython/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/csc_cython/colorspace_converter.cpython-*.so
%dir %{py3_sitedir}/xpra/codecs/drm
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/drm/drm.cpython-*.so
%dir %{py3_sitedir}/xpra/codecs/evdi
%{py3_sitedir}/xpra/codecs/evdi/*.py
%{py3_sitedir}/xpra/codecs/evdi/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/evdi/capture.cpython-*.so
%if %{with ffmpeg}
%dir %{py3_sitedir}/xpra/codecs/ffmpeg
%{py3_sitedir}/xpra/codecs/ffmpeg/*.py
%{py3_sitedir}/xpra/codecs/ffmpeg/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/ffmpeg/av_log.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/ffmpeg/colorspace_converter.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/ffmpeg/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/ffmpeg/encoder.cpython-*.so
%endif
%dir %{py3_sitedir}/xpra/codecs/gstreamer
%{py3_sitedir}/xpra/codecs/gstreamer/*.py
%{py3_sitedir}/xpra/codecs/gstreamer/__pycache__
%dir %{py3_sitedir}/xpra/codecs/jpeg
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/jpeg/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/jpeg/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/jpeg/*.py
%{py3_sitedir}/xpra/codecs/jpeg/__pycache__
%dir %{py3_sitedir}/xpra/codecs/libyuv
%{py3_sitedir}/xpra/codecs/libyuv/*.py
%{py3_sitedir}/xpra/codecs/libyuv/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/libyuv/colorspace_converter.cpython-*.so
%ifarch %{x8664}
%{py3_sitedir}/xpra/codecs/nvidia
%endif
%dir %{py3_sitedir}/xpra/codecs/openh264
%{py3_sitedir}/xpra/codecs/openh264/*.py
%{py3_sitedir}/xpra/codecs/openh264/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/openh264/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/openh264/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/pillow
%{py3_sitedir}/xpra/codecs/proxy
%dir %{py3_sitedir}/xpra/codecs/spng
%{py3_sitedir}/xpra/codecs/spng/*.py
%{py3_sitedir}/xpra/codecs/spng/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/spng/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/spng/encoder.cpython-*.so
%dir %{py3_sitedir}/xpra/codecs/v4l2
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/v4l2/pusher.cpython-*.so
%{py3_sitedir}/xpra/codecs/v4l2/*.py
%{py3_sitedir}/xpra/codecs/v4l2/__pycache__
%dir %{py3_sitedir}/xpra/codecs/vpx
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/vpx/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/vpx/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/vpx/*.py
%{py3_sitedir}/xpra/codecs/vpx/__pycache__
%dir %{py3_sitedir}/xpra/codecs/webp
%{py3_sitedir}/xpra/codecs/webp/*.py
%{py3_sitedir}/xpra/codecs/webp/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/webp/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/webp/encoder.cpython-*.so
%if %{with x264}
%dir %{py3_sitedir}/xpra/codecs/x264
%{py3_sitedir}/xpra/codecs/x264/*.py
%{py3_sitedir}/xpra/codecs/x264/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/x264/encoder.cpython-*.so
%endif
%{py3_sitedir}/xpra/dbus
%dir %{py3_sitedir}/xpra/gtk_common
%{py3_sitedir}/xpra/gtk_common/*.py
%{py3_sitedir}/xpra/gtk_common/__pycache__
%dir %{py3_sitedir}/xpra/gtk_common/gtk3
%{py3_sitedir}/xpra/gtk_common/gtk3/*.py
%{py3_sitedir}/xpra/gtk_common/gtk3/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/gtk_common/gtk3/gdk_atoms.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/gtk_common/gtk3/gdk_bindings.cpython-*.so
%{py3_sitedir}/xpra/keyboard
%dir %{py3_sitedir}/xpra/net
%{py3_sitedir}/xpra/net/*.py
%{py3_sitedir}/xpra/net/__pycache__
%dir %{py3_sitedir}/xpra/net/bencode
%attr(755,root,root) %{py3_sitedir}/xpra/net/bencode/cython_bencode.cpython-*.so
%{py3_sitedir}/xpra/net/bencode/*.py
%{py3_sitedir}/xpra/net/bencode/__pycache__
%dir %{py3_sitedir}/xpra/net/brotli
%{py3_sitedir}/xpra/net/brotli/*.py
%{py3_sitedir}/xpra/net/brotli/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/net/brotli/compressor.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/net/brotli/decompressor.cpython-*.so
%{py3_sitedir}/xpra/net/http
%dir %{py3_sitedir}/xpra/net/lz4
%{py3_sitedir}/xpra/net/lz4/*.py
%{py3_sitedir}/xpra/net/lz4/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/net/lz4/lz4.cpython-*.so
%{py3_sitedir}/xpra/net/mdns
%{py3_sitedir}/xpra/net/protocol
%{py3_sitedir}/xpra/net/qrcode/*.py
%dir %{py3_sitedir}/xpra/net/qrcode
%{py3_sitedir}/xpra/net/qrcode/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/net/qrcode/qrencode.cpython-*.so
%dir %{py3_sitedir}/xpra/net/quic
%{py3_sitedir}/xpra/net/quic/*.py
%{py3_sitedir}/xpra/net/quic/__pycache__
%dir %{py3_sitedir}/xpra/net/rencodeplus
%attr(755,root,root) %{py3_sitedir}/xpra/net/rencodeplus/rencodeplus.cpython-*.so
%{py3_sitedir}/xpra/net/rfb
%{py3_sitedir}/xpra/net/ssh
%dir %{py3_sitedir}/xpra/net/vsock
%{py3_sitedir}/xpra/net/vsock/*.py
%{py3_sitedir}/xpra/net/vsock/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/net/vsock/vsock.cpython-*.so
%{py3_sitedir}/xpra/net/websockets
%{py3_sitedir}/xpra/notifications
%dir %{py3_sitedir}/xpra/platform
%{py3_sitedir}/xpra/platform/*.py
%{py3_sitedir}/xpra/platform/__pycache__
%dir %{py3_sitedir}/xpra/platform/posix
%{py3_sitedir}/xpra/platform/posix/*.py
%{py3_sitedir}/xpra/platform/posix/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/platform/posix/netdev_query.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/platform/posix/proc_libproc.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/platform/posix/sd_listen.cpython-*.so
%{py3_sitedir}/xpra/scripts
%dir %{py3_sitedir}/xpra/server
%{py3_sitedir}/xpra/server/auth
%{py3_sitedir}/xpra/server/dbus
%{py3_sitedir}/xpra/server/mixins
%{py3_sitedir}/xpra/server/proxy
%{py3_sitedir}/xpra/server/rfb
%{py3_sitedir}/xpra/server/shadow
%{py3_sitedir}/xpra/server/source
%dir %{py3_sitedir}/xpra/server/window
%attr(755,root,root) %{py3_sitedir}/xpra/server/window/motion.cpython-*.so
%{py3_sitedir}/xpra/server/window/*.py
%{py3_sitedir}/xpra/server/window/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/server/cystats.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/server/pam.cpython-*.so
%{py3_sitedir}/xpra/server/*.py
%{py3_sitedir}/xpra/server/__pycache__
%dir %{py3_sitedir}/xpra/x11
%{py3_sitedir}/xpra/x11/*.py
%{py3_sitedir}/xpra/x11/__pycache__
%dir %{py3_sitedir}/xpra/x11/bindings
%attr(755,root,root) %{py3_sitedir}/xpra/x11/bindings/*.so
%{py3_sitedir}/xpra/x11/bindings/*.py
%{py3_sitedir}/xpra/x11/bindings/__pycache__
%{py3_sitedir}/xpra/x11/dbus
%{py3_sitedir}/xpra/x11/desktop
%dir %{py3_sitedir}/xpra/x11/gtk3
%attr(755,root,root) %{py3_sitedir}/xpra/x11/gtk3/gdk_bindings.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/x11/gtk3/gdk_display_source.cpython-*.so
%{py3_sitedir}/xpra/x11/gtk3/*.py
%{py3_sitedir}/xpra/x11/gtk3/__pycache__
%{py3_sitedir}/xpra/x11/gtk_x11
%{py3_sitedir}/xpra/x11/models
%{py3_sitedir}/xpra-%{version}-py*.egg-info

%files -n cups-backend-xpra
%defattr(644,root,root,755)
%attr(756,root,root) %{cupsdir}/xpraforwarder
