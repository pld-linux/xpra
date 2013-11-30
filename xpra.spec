# TODO
# - subpackages for client/server, see http://xpra.org/dev.html
Summary:	Xpra gives you "persistent remote applications" for X
Summary(pl.UTF-8):	Xpra - "stałe zdalne aplikacje" dla X
Name:		xpra
Version:	0.10.9
Release:	2
License:	GPL v2+
Source0:	http://xpra.org/src/%{name}-%{version}.tar.xz
# Source0-md5:	e53ad427bc0aefc0af1fa3a027b1ca7e
Group:		Networking
URL:		http://xpra.org/
BuildRequires:	OpenGL-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	libvpx-devel
BuildRequires:	libx264-devel
BuildRequires:	pkgconfig
BuildRequires:	python-Cython >= 0.14.0
BuildRequires:	python-distribute
BuildRequires:	python-pygobject-devel >= 2.0
BuildRequires:	python-pygtk-devel >= 2:2.0
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
Requires:	libwebp
Requires:	python-pygtk-gtk >= 2:2.0
Requires:	xorg-xserver-Xvfb
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%prep
%setup -q

%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/COPYING
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/README
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/webm/LICENSE

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xorg.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xpra.conf
%attr(755,root,root) %{_bindir}/xpra
%attr(755,root,root) %{_bindir}/xpra_Xdummy
%attr(755,root,root) %{_bindir}/xpra_launcher
%dir %{_datadir}/xpra
%dir %{_datadir}/xpra/icons
%{_datadir}/xpra/icons/*.png
%{_desktopdir}/xpra.desktop
%{_desktopdir}/xpra_launcher.desktop
%{_iconsdir}/xpra.png
%{_mandir}/man1/xpra.1*
%{_mandir}/man1/xpra_launcher.1*

%dir %{py_sitedir}/xpra
%{py_sitedir}/xpra/client
%{py_sitedir}/xpra/clipboard
%dir %{py_sitedir}/xpra/codecs
%dir %{py_sitedir}/xpra/codecs/argb
%attr(755,root,root) %{py_sitedir}/xpra/codecs/argb/argb.so
%{py_sitedir}/xpra/codecs/argb/__init__.py[co]
%dir %{py_sitedir}/xpra/codecs/csc_swscale
%attr(755,root,root) %{py_sitedir}/xpra/codecs/csc_swscale/colorspace_converter.so
%{py_sitedir}/xpra/codecs/csc_swscale/__init__.py[co]
%dir %{py_sitedir}/xpra/codecs/dec_avcodec
%attr(755,root,root) %{py_sitedir}/xpra/codecs/dec_avcodec/decoder.so
%{py_sitedir}/xpra/codecs/dec_avcodec/__init__.py[co]
%dir %{py_sitedir}/xpra/codecs/enc_x264
%attr(755,root,root) %{py_sitedir}/xpra/codecs/enc_x264/encoder.so
%{py_sitedir}/xpra/codecs/enc_x264/__init__.py[co]
%dir %{py_sitedir}/xpra/codecs/vpx
%attr(755,root,root) %{py_sitedir}/xpra/codecs/vpx/decoder.so
%attr(755,root,root) %{py_sitedir}/xpra/codecs/vpx/encoder.so
%{py_sitedir}/xpra/codecs/vpx/__init__.py[co]
%{py_sitedir}/xpra/codecs/webm
%dir %{py_sitedir}/xpra/codecs/xor
%attr(755,root,root) %{py_sitedir}/xpra/codecs/xor/cyxor.so
%{py_sitedir}/xpra/codecs/xor/*.py[co]
%{py_sitedir}/xpra/codecs/*.py[co]
%dir %{py_sitedir}/xpra/gtk_common
%attr(755,root,root) %{py_sitedir}/xpra/gtk_common/gdk_atoms.so
%{py_sitedir}/xpra/gtk_common/*.py[co]
%{py_sitedir}/xpra/keyboard
%dir %{py_sitedir}/xpra/net
%dir %{py_sitedir}/xpra/net/rencode
%attr(755,root,root) %{py_sitedir}/xpra/net/rencode/_rencode.so
%{py_sitedir}/xpra/net/rencode/*.py[co]
%{py_sitedir}/xpra/net/*.py[co]
%{py_sitedir}/xpra/platform
%{py_sitedir}/xpra/scripts
%dir %{py_sitedir}/xpra/server
%dir %{py_sitedir}/xpra/server/stats
%attr(755,root,root) %{py_sitedir}/xpra/server/stats/cymaths.so
%{py_sitedir}/xpra/server/stats/*.py[co]
%{py_sitedir}/xpra/server/*.py[co]
%{py_sitedir}/xpra/sound
%dir %{py_sitedir}/xpra/x11
%dir %{py_sitedir}/xpra/x11/bindings
%attr(755,root,root) %{py_sitedir}/xpra/x11/bindings/*.so
%{py_sitedir}/xpra/x11/bindings/__init__.py[co]
%dir %{py_sitedir}/xpra/x11/gtk_x11
%attr(755,root,root) %{py_sitedir}/xpra/x11/gtk_x11/gdk_*.so
%{py_sitedir}/xpra/x11/gtk_x11/*.py[co]
%{py_sitedir}/xpra/x11/*.py[co]
%{py_sitedir}/xpra/*.py[co]
%{py_sitedir}/xpra_all-%{version}-py*.egg-info
