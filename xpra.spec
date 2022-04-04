# TODO
# - test and finish systemd integration
# - subpackages for client/server, see http://xpra.org/dev.html
# - nvenc>=7 for cuda support (on bcond)
# - nvfbc (on bcond)
#
# Conditional build:
%bcond_without	client		# client part
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
Version:	2.5.3
Release:	5
License:	GPL v2+
Group:		X11/Applications/Networking
Source0:	http://xpra.org/src/%{name}-%{version}.tar.xz
# Source0-md5:	2fac9c558c099a6ea13d0202732bd684
Patch0:		setup-cc-ccache.patch
Patch1:		%{name}-libexecdir.patch
Patch2:		python3-version.patch
URL:		http://xpra.org/
BuildRequires:	OpenGL-devel
# libavcodec >= 57 for dec_avcodec, libavcodec >= 58.18 for enc_ffmpeg, libswscale
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 3.4}
BuildRequires:	gtk+3-devel >= 3.0
BuildRequires:	libjpeg-turbo-devel >= 1.4
BuildRequires:	libvpx-devel >= 1.4
BuildRequires:	libwebp-devel >= 0.5
%{?with_x264:BuildRequires:	libx264-devel}
%{?with_x265:BuildRequires:	libx265-devel}
BuildRequires:	libyuv-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-Cython >= 0.20
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-pycairo-devel
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	python3-setuptools
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
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libxkbfile-devel
BuildRequires:	xz
Requires:	gdk-pixbuf2 >= 2.0
Requires:	glib2 >= 2.0
Requires:	gobject-introspection >= 1
Requires:	gtk+3 >= 3.0
Requires:	libjpeg-turbo >= 1.4
Requires:	libvpx >= 1.4
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
%patch1 -p1
%patch2 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' cups/xpraforwarder $(grep -l '/usr/bin/env python' -r xpra scripts)
%{__sed} -i -e 's,"/bin/xpra_udev_product_version","%{_bindir}/xpra_udev_product_version",' udev/rules.d/71-xpra-virtual-pointer.rules
%{__sed} -i -e 's,@libexec@,%{_libexecdir},' setup.py

%define setup_opts \\\
	--with-PIC \\\
	--with-Xdummy \\\
	--with-Xdummy_wrapper \\\
	%{__with_without client} \\\
	%{__with_without clipboard} \\\
	%{__with_without swscale csc_swscale} \\\
	--with%{!?debug:out}-debug \\\
	%{__with_without ffmpeg dec_avcodec2} \\\
	%{__with_without ffmpeg enc_ffmpeg} \\\
	%{__with_without x264 enc_x264} \\\
	%{__with_without x265 enc_x265} \\\
	--without-gtk2 \\\
	--with-gtk3 \\\
	--without-nvenc \\\
	--without-nvfbc \\\
	%{__with_without opengl} \\\
	%{__with_without server} \\\
	%{__with_without server shadow} \\\
	%{__with_without sound} \\\
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
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/README

install -d $RPM_BUILD_ROOT/lib/udev/rules.d
%{__mv} $RPM_BUILD_ROOT{%{_prefix},}/lib/udev/rules.d/71-xpra-virtual-pointer.rules

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
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
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/20_sound.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/30_picture.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/35_webcam.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/40_client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/42_client_keyboard.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/50_server_network.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/55_server_x11.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/60_server.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/conf.d/65_proxy.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/xpra
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/X11/xorg.conf.d/90-xpra-virtual.conf
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/xpra
/etc/dbus-1/system.d/xpra.conf
%{systemdunitdir}/xpra.service
%{systemdunitdir}/xpra.socket
/usr/lib/sysusers.d/xpra.conf
/lib/udev/rules.d/71-xpra-virtual-pointer.rules
%attr(755,root,root) %{_bindir}/xpra
%attr(755,root,root) %{_bindir}/xpra_Xdummy
%attr(755,root,root) %{_bindir}/xpra_launcher
%attr(755,root,root) %{_bindir}/xpra_signal_listener
%attr(755,root,root) %{_bindir}/xpra_udev_product_version
%dir %{_libexecdir}/xpra
%attr(755,root,root) %{_libexecdir}/xpra/auth_dialog
%attr(755,root,root) %{_libexecdir}/xpra/gnome-open
%attr(755,root,root) %{_libexecdir}/xpra/gvfs-open
%attr(755,root,root) %{_libexecdir}/xpra/xdg-open
%{_datadir}/appdata/xpra.appdata.xml
%{_datadir}/mime/packages/application-x-xpraconfig.xml
%{_datadir}/xpra
%{_desktopdir}/xpra.desktop
%{_desktopdir}/xpra-gui.desktop
%{_desktopdir}/xpra-launcher.desktop
%{_desktopdir}/xpra-shadow.desktop
%{_iconsdir}/xpra.png
%{_iconsdir}/xpra-mdns.png
%{_iconsdir}/xpra-shadow.png
%{systemdtmpfilesdir}/xpra.conf
# specified in the above (xpra group seems to be optional though)
#%attr(770,root,xpra) %dir /run/xpra
%{_mandir}/man1/xpra.1*
%{_mandir}/man1/xpra_launcher.1*

%dir %{py3_sitedir}/xpra
%dir %{py3_sitedir}/xpra/buffers
%{py3_sitedir}/xpra/buffers/*.py
%{py3_sitedir}/xpra/buffers/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/buffers/membuf.cpython-*.so
%dir %{py3_sitedir}/xpra/client
%{py3_sitedir}/xpra/client/gl
%dir %{py3_sitedir}/xpra/client/gtk3
%attr(755,root,root) %{py3_sitedir}/xpra/client/gtk3/cairo_workaround.cpython-*.so
%{py3_sitedir}/xpra/client/gtk3/*.py
%{py3_sitedir}/xpra/client/gtk3/__pycache__
%{py3_sitedir}/xpra/client/gtk_base
%{py3_sitedir}/xpra/client/mixins
%{py3_sitedir}/xpra/client/*.py
%{py3_sitedir}/xpra/client/__pycache__
%{py3_sitedir}/xpra/clipboard
%dir %{py3_sitedir}/xpra/codecs
%dir %{py3_sitedir}/xpra/codecs/argb
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/argb/argb.cpython-*.so
%{py3_sitedir}/xpra/codecs/argb/*.py
%{py3_sitedir}/xpra/codecs/argb/__pycache__
%dir %{py3_sitedir}/xpra/codecs/csc_libyuv
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/csc_libyuv/colorspace_converter.cpython-*.so
%{py3_sitedir}/xpra/codecs/csc_libyuv/*.py
%{py3_sitedir}/xpra/codecs/csc_libyuv/__pycache__
%if %{with swscale}
%dir %{py3_sitedir}/xpra/codecs/csc_swscale
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/csc_swscale/colorspace_converter.cpython-*.so
%{py3_sitedir}/xpra/codecs/csc_swscale/*.py
%{py3_sitedir}/xpra/codecs/csc_swscale/__pycache__
%endif
%if %{with ffmpeg}
%dir %{py3_sitedir}/xpra/codecs/dec_avcodec2
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/dec_avcodec2/decoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/dec_avcodec2/*.py
%{py3_sitedir}/xpra/codecs/dec_avcodec2/__pycache__
%endif
%if %{with ffmpeg}
%dir %{py3_sitedir}/xpra/codecs/enc_ffmpeg
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/enc_ffmpeg/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/enc_ffmpeg/*.py
%{py3_sitedir}/xpra/codecs/enc_ffmpeg/__pycache__
%endif
%{py3_sitedir}/xpra/codecs/enc_proxy
%if %{with x264}
%dir %{py3_sitedir}/xpra/codecs/enc_x264
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/enc_x264/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/enc_x264/*.py
%{py3_sitedir}/xpra/codecs/enc_x264/__pycache__
%endif
%if %{with x265}
%dir %{py3_sitedir}/xpra/codecs/enc_x265
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/enc_x265/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/enc_x265/*.py
%{py3_sitedir}/xpra/codecs/enc_x265/__pycache__
%endif
%dir %{py3_sitedir}/xpra/codecs/jpeg
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/jpeg/decoder.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/jpeg/encoder.cpython-*.so
%{py3_sitedir}/xpra/codecs/jpeg/*.py
%{py3_sitedir}/xpra/codecs/jpeg/__pycache__
%dir %{py3_sitedir}/xpra/codecs/libav_common
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/libav_common/av_log.cpython-*.so
%{py3_sitedir}/xpra/codecs/libav_common/*.py
%{py3_sitedir}/xpra/codecs/libav_common/__pycache__
%{py3_sitedir}/xpra/codecs/pillow
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
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/webp/decode.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/webp/encode.cpython-*.so
%{py3_sitedir}/xpra/codecs/webp/*.py
%{py3_sitedir}/xpra/codecs/webp/__pycache__
%dir %{py3_sitedir}/xpra/codecs/xor
%attr(755,root,root) %{py3_sitedir}/xpra/codecs/xor/cyxor.cpython-*.so
%{py3_sitedir}/xpra/codecs/xor/*.py
%{py3_sitedir}/xpra/codecs/xor/__pycache__
%{py3_sitedir}/xpra/codecs/*.py
%{py3_sitedir}/xpra/codecs/__pycache__
%{py3_sitedir}/xpra/dbus
%dir %{py3_sitedir}/xpra/gtk_common
%dir %{py3_sitedir}/xpra/gtk_common/gtk3
%attr(755,root,root) %{py3_sitedir}/xpra/gtk_common/gtk3/gdk_atoms.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/gtk_common/gtk3/gdk_bindings.cpython-*.so
%{py3_sitedir}/xpra/gtk_common/*.py
%{py3_sitedir}/xpra/gtk_common/__pycache__
%{py3_sitedir}/xpra/keyboard
%dir %{py3_sitedir}/xpra/net
%dir %{py3_sitedir}/xpra/net/bencode
%attr(755,root,root) %{py3_sitedir}/xpra/net/bencode/cython_bencode.cpython-*.so
%{py3_sitedir}/xpra/net/bencode/*.py
%{py3_sitedir}/xpra/net/bencode/__pycache__
%{py3_sitedir}/xpra/net/mdns
%{py3_sitedir}/xpra/net/websockets
%attr(755,root,root) %{py3_sitedir}/xpra/net/vsock.cpython-*.so
%{py3_sitedir}/xpra/net/*.py
%{py3_sitedir}/xpra/net/__pycache__
%{py3_sitedir}/xpra/notifications
%dir %{py3_sitedir}/xpra/platform
%dir %{py3_sitedir}/xpra/platform/xposix
%attr(755,root,root) %{py3_sitedir}/xpra/platform/xposix/netdev_query.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/platform/xposix/sd_listen.cpython-*.so
%{py3_sitedir}/xpra/platform/xposix/*.py
%{py3_sitedir}/xpra/platform/xposix/__pycache__
%{py3_sitedir}/xpra/platform/*.py
%{py3_sitedir}/xpra/platform/__pycache__
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
%{py3_sitedir}/xpra/sound
%dir %{py3_sitedir}/xpra/x11
%dir %{py3_sitedir}/xpra/x11/bindings
%attr(755,root,root) %{py3_sitedir}/xpra/x11/bindings/*.so
%{py3_sitedir}/xpra/x11/bindings/*.py
%{py3_sitedir}/xpra/x11/bindings/__pycache__
%{py3_sitedir}/xpra/x11/dbus
%dir %{py3_sitedir}/xpra/x11/gtk3
%attr(755,root,root) %{py3_sitedir}/xpra/x11/gtk3/gdk_bindings.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/x11/gtk3/gdk_display_source.cpython-*.so
%{py3_sitedir}/xpra/x11/gtk3/*.py
%{py3_sitedir}/xpra/x11/gtk3/__pycache__
%{py3_sitedir}/xpra/x11/gtk_x11
%{py3_sitedir}/xpra/x11/models
%{py3_sitedir}/xpra/x11/*.py
%{py3_sitedir}/xpra/x11/__pycache__
%attr(755,root,root) %{py3_sitedir}/xpra/monotonic_time.cpython-*.so
%attr(755,root,root) %{py3_sitedir}/xpra/rectangle.cpython-*.so
%{py3_sitedir}/xpra/*.py
%{py3_sitedir}/xpra/__pycache__
%{py3_sitedir}/xpra-%{version}-py*.egg-info

%files -n cups-backend-xpra
%defattr(644,root,root,755)
%attr(756,root,root) %{cupsdir}/xpraforwarder
