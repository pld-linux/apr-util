#
# Conditional build:
%bcond_without	ldap	# without LDAP support
%bcond_with	mysql	# with MySQL support
%bcond_without	pgsql	# without PostgreSQL support
%bcond_with	sqlite	# with SQLite 2.x support
%bcond_without	sqlite3	# without SQLite3 support
#
Summary:	A companion library to Apache Portable Runtime
Summary(pl):	Biblioteka towarzysz±ca Apache Portable Runtime
Name:		apr-util
Version:	1.2.2
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	694228b227e30cb9da3823514516e91c
Patch0:		%{name}-link.patch
URL:		http://apr.apache.org/
BuildRequires:	apr-devel >= 1:1.1.0
BuildRequires:	autoconf
BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_sqlite:BuildRequires:	sqlite-devel >= 2}
%{?with_sqlite3:BuildRequires:	sqlite3-devel >= 3}
Requires:	apr >= 1:1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr-util

%description
A companion library to Apache Portable Runtime.

%description -l pl
Biblioteka towarzysz±ca dla biblioteki Apache Portable Runtime
(przeno¶nej biblioteki uruchomieniowej).

%package devel
Summary:	Header files and development documentation for apr-util
Summary(pl):	Pliki nag³ówkowe i dokumentacja programisty do apr-util
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apr-devel >= 1:1.1.0
Requires:	db-devel
Requires:	expat-devel
Requires:	gdbm-devel
%{?with_mysql:Requires:	mysql-devel}
%{?with_ldap:Requires:	openldap-devel}
%{?with_pgsql:Requires:	postgresql-devel}
%{?with_sqlite:Requires:	sqlite-devel >= 2}
%{?with_sqlite3:Requires:	sqlite3-devel >= 3}

%description devel
Header files and development documentation for apr-util.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do apr-util.

%package static
Summary:	Static apr-util library
Summary(pl):	Statyczna biblioteka apr-util
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static apr-util library.

%description static -l pl
Statyczna biblioteka apr-util.

%prep
%setup -q
%patch0 -p1

# not needed, gen-build.py is not packaged in apr
%{__perl} -pi -e 's/^(.*gen-build\.py)/#$1/' buildconf

%build
./buildconf \
	--with-apr=%{_datadir}/apr

%configure \
	--with-apr=%{_bindir}/apr-1-config \
%if %{with ldap}
	--with-ldap \
	--with-ldap-include=%{_prefix}/include \
	--with-ldap-lib=%{_libdir} \
%endif
	--with-iconv=%{_prefix} \
	%{?with_mysql:--with-mysql} \
	%{!?with_pgsql:--without-pgsql} \
	%{!?with_sqlite:--without-sqlite2} \
	%{!?with_sqlite3:--without-sqlite3}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/aprutil.exp
%{_includedir}
%{_pkgconfigdir}/apr-util-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
