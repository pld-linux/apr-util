# TODO
# - play with DSO dbd's
# - licensing issues with mysql. can we (PLD Linux) package it inside
#   apr-util? see INSTALL.MySQL for more details
#
# Conditional build:
%bcond_without	ldap	# without LDAP support
%bcond_with	mysql	# with MySQL support
%bcond_without	pgsql	# without PostgreSQL support
%bcond_with	sqlite	# with SQLite 2.x support
%bcond_without	sqlite3	# without SQLite3 support
%bcond_with	dso	# experimental dso linking
#
Summary:	A companion library to Apache Portable Runtime
Summary(pl):	Biblioteka towarzysz±ca Apache Portable Runtime
Name:		apr-util
Version:	1.2.2
Release:	1.18
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	694228b227e30cb9da3823514516e91c
# http://apache.webthing.com/database/apr_dbd_mysql.c, our is modified
Source1:	apr_dbd_mysql.c
Patch0:		%{name}-link.patch
Patch1:		%{name}-mysql.patch
Patch2:		%{name}-db4.4.patch
Patch3:		%{name}-dso.patch
URL:		http://apr.apache.org/
BuildRequires:	apr-devel >= 1:1.1.0
%{?with_mysql:BuildRequires:	apr-devel >= 1:1.2.2-2.6}
BuildRequires:	autoconf
BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	sed >= 4.0
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
%patch1 -p1
%patch2 -p1
%if %{with mysql}
cp %{SOURCE1} dbd/apr_dbd_mysql.c
%else
# not needed, gen-build.py is not packaged in apr-util
# (and it shouldn't: apr-devel should have it -glen)
%{__sed} -i -e 's/^\(.*gen-build\.py\)/#\1/' buildconf
%endif
%{?with_dso:%patch3 -p1}

rm -rf xml/expat

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
	%{?with_mysql:--with-mysql=%{_prefix}} \
	%{!?with_pgsql:--without-pgsql} \
	%{!?with_sqlite:--without-sqlite2} \
	%{!?with_sqlite3:--without-sqlite3}

%{__make} \
	CC="%{__cc}"

%if %{with dso}
%{__sed} -i -e 's,-l\(pq\|mysqlclient_r\|sqlite\|sqlite3\) ,,g' Makefile
%{__sed} -i -e '/OBJECTS_all/s, dbd/apr_dbd_.*\.lo,,g' build-outputs.mk
rm -f libaprutil-1.la
%{__make} libaprutil-1.la

%if %{with mysql}
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version dbd/apr_dbd_mysql.lo -lmysqlclient_r -o dbd/libapr_dbd_mysql.la
%endif
%if %{with pgsql}
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version dbd/apr_dbd_pgsql.lo -lpq  -o dbd/libapr_dbd_pgsql.la
%endif
%if %{with sqlite3}
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version dbd/apr_dbd_sqlite3.lo -lsqlite3 -o dbd/libapr_dbd_sqlite3.la
%endif
%if %{with sqlite}
libtool --mode=link --tag=CC %{__cc} -rpath %{_libdir} -avoid-version dbd/apr_dbd_sqlite2.lo -o dbd/libapr_dbd_sqlite2.la
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
 
%if %{with dso}
%if %{with mysql}
libtool --mode=install /usr/bin/install -c -m 755 dbd/libapr_dbd_mysql.la $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/{lib,}apr_dbd_mysql.so
%endif
%if %{with pgsql}
libtool --mode=install /usr/bin/install -c -m 755 dbd/libapr_dbd_pgsql.la $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/{lib,}apr_dbd_pgsql.so
%endif
%if %{with sqlite3}
libtool --mode=install /usr/bin/install -c -m 755 dbd/libapr_dbd_sqlite3.la $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/{lib,}apr_dbd_sqlite3.so
%endif
%if %{with sqlite}
libtool --mode=install /usr/bin/install -c -m 755 dbd/libapr_dbd_sqlite2.la $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/{lib,}apr_dbd_sqlite2.so
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES
%{?with_mysql:%doc INSTALL.MySQL}
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%{?with_dso:%attr(755,root,root) %{_libdir}/apr_dbd_*.so}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libaprutil*.so
%{_libdir}/lib*.la
%{_libdir}/aprutil.exp
%{_includedir}
%{_pkgconfigdir}/apr-util-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
