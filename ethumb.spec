#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Ethumb - thumbnail generation library
Summary(pl.UTF-8):	Ethumb - biblioteka generująca miniaturki
Name:		ethumb
Version:	1.0.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	ffb8fa09c553b8a95efee5cc8e3050f2
Patch0:		%{name}-plugins.patch
URL:		http://trac.enlightenment.org/e/wiki/Ethumb
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	e_dbus-devel >= 1.0.0
BuildRequires:	ecore-devel >= 1.0.0
BuildRequires:	ecore-evas-devel >= 1.0.0
BuildRequires:	ecore-file-devel >= 1.0.0
BuildRequires:	eina-devel >= 1.0.0
BuildRequires:	emotion-devel
#BuildRequires:	epdf-devel
BuildRequires:	evas-devel >= 1.0.0
BuildRequires:	evas-loader-jpeg >= 1.0.0
BuildRequires:	edje >= 1.0.0
BuildRequires:	edje-devel >= 1.0.0
BuildRequires:	libexif-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ethumb is a thumbnail generation library. Features:
- create thumbnails with a predefined frame (possibly an edje frame);
- have an option to create fdo-like thumbnails;
- have a client/server utility.

%description -l pl.UTF-8
Ethumb to biblioteka do generowania miniaturek. Możliwości:
- tworzenie miniaturek z predefiniowaną ramką (w tym ramką edje);
- opcja tworzenia miniaturek w stylu fdo;
- narzędzia klient-serwer.

%package libs
Summary:	Ethumb shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Ethumb
Group:		Libraries
Requires:	e_dbus >= 1.0.0
Requires:	ecore >= 1.0.0
Requires:	ecore-evas >= 1.0.0
Requires:	ecore-file >= 1.0.0
Requires:	edje-libs >= 1.0.0
Requires:	eina >= 1.0.0
Requires:	evas >= 1.0.0

%description libs
Ethumb shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Ethumb.

%package plugin-emotion
Summary:	Emotion plugin for Ethumb library
Summary(pl.UTF-8):	Wtyczka Emotion dla biblioteki Ethumb
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description plugin-emotion
Emotion plugin for Ethumb library. It creates thumbnails from movies
using Emotion library.

%description plugin-emotion -l pl.UTF-8
Wtyczka Emotion dla biblioteki Ethumb. Potrafi tworzyć miniaturki z
filmów przy użyciu biblioteki Emotion.

%package devel
Summary:	Header files for Ethumb libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Ethumb
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	e_dbus-devel >= 1.0.0
Requires:	ecore-devel >= 1.0.0
Requires:	ecore-evas-devel >= 1.0.0
Requires:	ecore-file-devel >= 1.0.0
Requires:	edje-devel >= 1.0.0
Requires:	eina-devel >= 1.0.0
Requires:	emotion-devel
Requires:	evas-devel >= 1.0.0
Requires:	libexif-devel

%description devel
Header files for Ethumb libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Ethumb.

%package static
Summary:	Static Ethumb libraries
Summary(pl.UTF-8):	Statyczne biblioteki Ethumb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Ethumb libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Ethumb.

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
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ethumb/plugins/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_bindir}/ethumb
%attr(755,root,root) %{_bindir}/ethumbd
%attr(755,root,root) %{_bindir}/ethumbd_client
%attr(755,root,root) %{_libdir}/ethumbd_slave
%{_datadir}/ethumb
%{_datadir}/dbus-1/services/org.enlightenment.Ethumb.service

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libethumb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libethumb.so.1
%attr(755,root,root) %{_libdir}/libethumb_client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libethumb_client.so.1
%dir %{_libdir}/ethumb
%dir %{_libdir}/ethumb/plugins

%files plugin-emotion
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ethumb/plugins/emotion.so
%{_libdir}/ethumb/plugins/data

#%files plugin-epdf
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/ethumb/plugins/epdf.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libethumb.so
%attr(755,root,root) %{_libdir}/libethumb_client.so
%{_libdir}/libethumb.la
%{_libdir}/libethumb_client.la
%{_includedir}/ethumb-1
%{_pkgconfigdir}/ethumb.pc
%{_pkgconfigdir}/ethumb_client.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libethumb.a
%{_libdir}/libethumb_client.a
%endif
