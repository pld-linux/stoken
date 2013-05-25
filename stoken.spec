Summary:	Software Token for Linux/UNIX
Summary(pl.UTF-8):	Token programowy dla systemów Linux/UNIX
Name:		stoken
Version:	0.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/stoken/%{name}-%{version}.tar.gz
# Source0-md5:	d815783d7198f1181c1a72e3d730d367
URL:		http://stoken.sourceforge.net/
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	libtomcrypt-devel
BuildRequires:	pkgconfig >= 1:0.27
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
stoken is a tokencode generator compatible with RSA SecurID 128-bit
(AES) tokens. It is a hobbyist project, not affiliated with or
endorsed by RSA Security.

%description -l pl.UTF-8
stoken to generator kodów tokenów zgodnych z tokenami 128-bitowymi RSA
SecurID (AES). Jest to projekt hobbistyczny, nie powiązany, ani nie
gwarantowany przez RSA Security.

%package gui
Summary:	Software Token GUI
Summary(pl.UTF-8):	Graficzny interfejs użytkownika do tokenów programowych
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Software Token GUI.

%description gui -l pl.UTF-8
Graficzny interfejs użytkownika do tokenów programowych.

%package devel
Summary:	Header files for stoken library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki stoken
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtomcrypt-devel

%description devel
Header files for stoken library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki stoken.

%package static
Summary:	Static stoken library
Summary(pl.UTF-8):	Statyczna biblioteka stoken
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static stoken library.

%description static -l pl.UTF-8
Statyczna biblioteka stoken.

%prep
%setup -q

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstoken.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README TODO
%attr(755,root,root) %{_bindir}/stoken
%attr(755,root,root) %{_libdir}/libstoken.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstoken.so.1
%{_mandir}/man1/stoken.1*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stoken-gui
%{_desktopdir}/stoken-gui.desktop
%{_pixmapsdir}/stoken-gui.png
%{_mandir}/man1/stoken-gui.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstoken.so
%{_includedir}/stoken.h
%{_pkgconfigdir}/stoken.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libstoken.a
