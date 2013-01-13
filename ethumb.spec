#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
%define		ecore_ver	1.7.5
%define		edbus_ver	1.7.5
%define		edje_ver	1.7.5
%define		eet_ver		1.7.5
%define		eina_ver	1.7.5
%define		evas_ver	1.7.5

Summary:	Ethumb - thumbnail generation library
Summary(pl.UTF-8):	Ethumb - biblioteka generująca miniaturki
Name:		ethumb
Version:	1.7.5
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://download.enlightenment.org/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	5d4e0840bea7abb396224062593418ac
Patch0:		%{name}-plugins.patch
URL:		http://trac.enlightenment.org/e/wiki/Ethumb
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1.6
BuildRequires:	e_dbus-devel >= %{edbus_ver}
BuildRequires:	ecore-devel >= %{ecore_ver}
BuildRequires:	ecore-evas-devel >= %{ecore_ver}
BuildRequires:	ecore-file-devel >= %{ecore_ver}
BuildRequires:	eet-devel >= %{eet_ver}
BuildRequires:	eina-devel >= %{eina_ver}
BuildRequires:	emotion-devel
#BuildRequires:	epdf-devel
BuildRequires:	evas-devel >= %{evas_ver}
BuildRequires:	evas-loader-jpeg >= %{evas_ver}
BuildRequires:	edje >= %{edje_ver}
BuildRequires:	edje-devel >= %{edje_ver}
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
Requires:	e_dbus >= %{edbus_ver}
Requires:	ecore >= %{ecore_ver}
Requires:	ecore-evas >= %{ecore_ver}
Requires:	ecore-file >= %{ecore_ver}
Requires:	edje-libs >= %{edje_ver}
Requires:	eina >= %{eina_ver}
Requires:	evas >= %{evas_ver}

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
Requires:	e_dbus-devel >= %{edbus_ver}
Requires:	ecore-devel >= %{ecore_ver}
Requires:	ecore-evas-devel >= %{ecore_ver}
Requires:	ecore-file-devel >= %{ecore_ver}
Requires:	edje-devel >= %{edje_ver}
Requires:	eina-devel >= %{eina_ver}
Requires:	emotion-devel
Requires:	evas-devel >= %{evas_ver}
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
