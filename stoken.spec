#
# Conditional build:
%bcond_without	gtk	# GTK+ 3 based GUI
%bcond_without	java	# JNI bindings
#
Summary:	Software Token for Linux/UNIX
Summary(pl.UTF-8):	Token programowy dla systemów Linux/UNIX
Name:		stoken
Version:	0.91
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/stoken/%{name}-%{version}.tar.gz
# Source0-md5:	584432f22032f0a8a719272fa2329bcd
Patch0:		%{name}-sh.patch
URL:		http://stoken.sourceforge.net/
%{?with_java:BuildRequires:	ant}
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.11
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.0}
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libtomcrypt-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 2
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

%package -n java-stoken
Summary:	JNI interface for stoken library
Summary(pl.UTF-8):	Interfejs JNI do biblioteki stoken
License:	BSD
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description -n java-stoken
JNI interface for stoken library.

%description -n java-stoken -l pl.UTF-8
Interfejs JNI do biblioteki stoken.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_gtk:--without-gtk} \
	%{?with_java:--with-java}

%{__make}

%if %{with java}
cd java
install -d dist
%ant
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstoken.la

%if %{with java}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstoken-wrapper.{la,a}
install -D java/dist/stoken-wrapper.jar $RPM_BUILD_ROOT%{_javadir}/stoken-wrapper.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-stoken -p /sbin/ldconfig
%postun	-n java-stoken -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README.md TODO
%attr(755,root,root) %{_bindir}/stoken
%attr(755,root,root) %{_libdir}/libstoken.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstoken.so.1
%{_mandir}/man1/stoken.1*

%if %{with gtk}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/stoken-gui
%{_datadir}/stoken
%{_desktopdir}/stoken-gui.desktop
%{_desktopdir}/stoken-gui-small.desktop
%{_pixmapsdir}/stoken-gui.png
%{_mandir}/man1/stoken-gui.1*
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstoken.so
%{_includedir}/stoken.h
%{_pkgconfigdir}/stoken.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libstoken.a

%if %{with java}
%files -n java-stoken
%defattr(644,root,root,755)
%doc java/src/com/example/LibTest.java
%attr(755,root,root) %{_libdir}/libstoken-wrapper.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstoken-wrapper.so.0
%attr(755,root,root) %{_libdir}/libstoken-wrapper.so
%{_javadir}/stoken-wrapper.jar
%endif
