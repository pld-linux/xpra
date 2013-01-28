# TODO
# - package just xpra, get rid of the wm stuff
# - subpackages for client/server, see http://xpra.org/dev.html
Summary:	Xpra gives you "persistent remote applications" for X
Name:		xpra
Version:	0.7.8
Release:	0.2
License:	GPL v2+
Source0:	http://xpra.org/src/%{name}-%{version}.tar.xz
# Source0-md5:	940d20f26c1cfaa16bd0aee69bfb2233
Group:		Networking
URL:		http://xpra.org/
BuildRequires:	ffmpeg-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libx264-devel
BuildRequires:	pkgconfig
BuildRequires:	python-Cython
BuildRequires:	python-distribute
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xz
#Requires:	PyOpenGL
#Requires:	libvpx
#Requires:	libwebp
#Requires:	libx264
#Requires:	pygtkglext
#Requires:	python-PIL
#Requires:	python-ctypes
#Requires:	python-dbus
#Requires:	python-numeric
#Requires:	python-pygtk-gtk
#Requires:	python-uuid
#Requires:	x264-libs
#Requires:	xorg-x11-drv-dummy
#Requires:	xorg-x11-drv-void
#Requires:	xorg-x11-server-Xvfb
#Requires:	xorg-x11-server-utils
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

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/parti/test_*.py*

%{__rm} $RPM_BUILD_ROOT%{_datadir}/parti/README
%{__rm} $RPM_BUILD_ROOT%{_datadir}/parti/parti.README
%{__rm} $RPM_BUILD_ROOT%{_datadir}/wimpiggy/wimpiggy.README
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/COPYING
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/webm/LICENSE
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/xpra.README
%{__rm} $RPM_BUILD_ROOT%{_datadir}/xpra/icons/xpra.ico

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS xpra.README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xorg.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/xpra.conf
%attr(755,root,root) %{_bindir}/parti
%attr(755,root,root) %{_bindir}/parti-repl
%attr(755,root,root) %{_bindir}/xpra
%attr(755,root,root) %{_bindir}/xpra_Xdummy
%attr(755,root,root) %{_bindir}/xpra_launcher
%dir %{_datadir}/xpra
%dir %{_datadir}/xpra/icons
%{_datadir}/xpra/icons/*.png
%{_desktopdir}/xpra_launcher.desktop
%{_iconsdir}/xpra.png
%{_mandir}/man1/parti.1*
%{_mandir}/man1/xpra.1*
%{_mandir}/man1/xpra_launcher.1*

%dir %{py_sitedir}/parti
%{py_sitedir}/parti/*.py[co]
%{py_sitedir}/parti/addons
%{py_sitedir}/parti/scripts
%{py_sitedir}/parti/trays
%{py_sitedir}/parti_all-%{version}-py*.egg-info

%dir %{py_sitedir}/wimpiggy
%dir %{py_sitedir}/wimpiggy/gdk
%dir %{py_sitedir}/wimpiggy/gdk/*.py[co]
%dir %{py_sitedir}/wimpiggy/lowlevel
%{py_sitedir}/wimpiggy/*.py[co]
%{py_sitedir}/wimpiggy/lowlevel/*.py[co]
%attr(755,root,root) %{py_sitedir}/wimpiggy/gdk/gdk_atoms.so
%attr(755,root,root) %{py_sitedir}/wimpiggy/lowlevel/bindings.so

%dir %{py_sitedir}/xpra
%dir %{py_sitedir}/xpra/platform
%dir %{py_sitedir}/xpra/rencode
%dir %{py_sitedir}/xpra/scripts
%dir %{py_sitedir}/xpra/vpx
%dir %{py_sitedir}/xpra/webm
%dir %{py_sitedir}/xpra/x264
%dir %{py_sitedir}/xpra/xposix
%{py_sitedir}/xpra/*.py[co]
%{py_sitedir}/xpra/platform/*.py[co]
%{py_sitedir}/xpra/rencode/*.py[co]
%{py_sitedir}/xpra/scripts/*.py[co]
%{py_sitedir}/xpra/vpx/*.py[co]
%{py_sitedir}/xpra/webm/*.py[co]
%{py_sitedir}/xpra/x264/*.py[co]
%{py_sitedir}/xpra/xposix/*.py[co]
%attr(755,root,root) %{py_sitedir}/xpra/rencode/_rencode.so
%attr(755,root,root) %{py_sitedir}/xpra/vpx/codec.so
%attr(755,root,root) %{py_sitedir}/xpra/wait_for_x_server.so
%attr(755,root,root) %{py_sitedir}/xpra/x264/codec.so
