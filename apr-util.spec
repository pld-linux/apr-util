#
# Conditional build:
%bcond_with	freetds	# with FreeTDS (sybdb) DBD module (unfinished)
%bcond_without	mysql	# without MySQL DBD module
%bcond_without	odbc	# without ODBC DBD module
%bcond_with	oracle	# with Oracle DBD module (BR: proprietary libs)
%bcond_without	pgsql	# without PostgreSQL DBD module
%bcond_with	sqlite2	# with SQLite 2.x DBD module
%bcond_without	sqlite3	# without SQLite3 DBD module
%bcond_without	ldap	# without LDAP module
%bcond_without	tests

# define	dbver	db50
%if 0%{!?dbver:1}
	%if "%{pld_release}" == "th"
		%define	dbver	db47
	%endif
	%if "%{pld_release}" == "ti"
		%define	dbver	db45
	%endif
	%if "%{pld_release}" == "ac"
		%define	dbver	db42
	%endif
%endif

# files list broken, feel free to really fix
%ifarch alpha
%undefine	with_mysql
%endif

Summary:	A companion library to Apache Portable Runtime
Summary(pl.UTF-8):	Biblioteka towarzysząca Apache Portable Runtime
Name:		apr-util
Version:	1.3.12
Release:	2
Epoch:		1
License:	Apache v2.0
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
# Source0-md5:	0f671b037ca62751a8a7005578085560
Patch0:		%{name}-link.patch
Patch1:		%{name}-config-noldap.patch
Patch2:		%{name}-libtool.patch
Patch3:		%{name}-flags.patch
URL:		http://apr.apache.org/
BuildRequires:	apr-devel >= 1:1.3.0
BuildRequires:	autoconf >= 2.59
%if "%{pld_release}" == "th"
BuildRequires:	db-devel >= 4.7
%endif
%if "%{pld_release}" == "ti"
BuildRequires:	db-devel >= 4.5
%endif
%if "%{pld_release}" == "ac"
BuildRequires:	db-devel >= 4.2
BuildConflicts:	db4.5-devel
%endif
BuildRequires:	expat-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	libtool
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpm >= 4.4.9-56
%{?with_sqlite2:BuildRequires:	sqlite-devel >= 2}
%{?with_sqlite3:BuildRequires:	sqlite3-devel >= 3}
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	which
Requires:	apr >= 1:1.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr-util

%description
A companion library to Apache Portable Runtime.

%description -l pl.UTF-8
Biblioteka towarzysząca dla biblioteki Apache Portable Runtime
(przenośnej biblioteki uruchomieniowej).

%package dbm-db
Summary:	DBM driver for DB
Summary(pl.UTF-8):	Sterownik DBM dla DB
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbm-db
DBM driver for DB.

%description dbm-db -l pl.UTF-8
Sterownik DBM dla DB.

%package dbd-freetds
Summary:	DBD driver for FreeTDS (Sybase/MS SQL)
Summary(pl.UTF-8):	Sterownik DBD dla FreeTDS (Sybase/MS SQL)
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-freetds
DBD driver for FreeTDS (Sybase/MS SQL).

%description dbd-freetds -l pl.UTF-8
Sterownik DBD dla FreeTDS (Sybase/MS SQL).

%package dbd-mysql
Summary:	DBD driver for MySQL
Summary(pl.UTF-8):	Sterownik DBD dla MySQL-a
License:	GPL
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-mysql
DBD driver for MySQL.

%description dbd-mysql -l pl.UTF-8
Sterownik DBD dla MySQL-a.

%package dbd-odbc
Summary:	DBD driver for ODBC
Summary(pl.UTF-8):	Sterownik DBD dla ODBC
License:	GPL
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-odbc
DBD driver for ODBC.

%description dbd-odbc -l pl.UTF-8
Sterownik DBD dla ODBC.

%package dbd-oracle
Summary:	DBD driver for Oracle
Summary(pl.UTF-8):	Sterownik DBD dla Oracle'a
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-oracle
DBD driver for Oracle.

%description dbd-oracle -l pl.UTF-8
Sterownik DBD dla Oracle'a.

%package dbd-pgsql
Summary:	DBD driver for PostgreSQL
Summary(pl.UTF-8):	Sterownik DBD dla PostgreSQL-a
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-pgsql
DBD driver for PostgreSQL.

%description dbd-pgsql -l pl.UTF-8
Sterownik DBD dla PostgreSQL-a.

%package dbd-sqlite2
Summary:	DBD driver for SQLite 2
Summary(pl.UTF-8):	Sterownik DBD dla SQLite 2
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-sqlite2
DBD driver for SQLite 2.

%description dbd-sqlite2 -l pl.UTF-8
Sterownik DBD dla SQLite 2.

%package dbd-sqlite3
Summary:	DBD driver for SQLite 3
Summary(pl.UTF-8):	Sterownik DBD dla SQLite 3
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description dbd-sqlite3
DBD driver for SQLite 3.

%description dbd-sqlite3 -l pl.UTF-8
Sterownik DBD dla SQLite 3.

%package ldap
Summary:	APR LDAP driver
Summary(pl.UTF-8):	Sterownik APR dla LDAP
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description ldap
APR LDAP driver.

%description ldap -l pl.UTF-8
Sterownik APR dla LDAP.

%package devel
Summary:	Header files and development documentation for apr-util
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja programisty do apr-util
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	apr-devel >= 1:1.3.0
Requires:	expat-devel

%description devel
Header files and development documentation for apr-util.

%description devel -l pl.UTF-8
Pliki nagłówkowe i dokumentacja programisty do apr-util.

%package static
Summary:	Static apr-util library
Summary(pl.UTF-8):	Statyczna biblioteka apr-util
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static apr-util library.

%description static -l pl.UTF-8
Statyczna biblioteka apr-util.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# be sure to link with db version requested
%{__sed} -i -e 's/db4 db\|db5 db//' build/dbm.m4

%{__rm} -r xml/expat

echo '
<Layout PLD>
    prefix:        %{_prefix}
    exec_prefix:   %{_exec_prefix}
    bindir:        %{_bindir}
    sbindir:       %{_sbindir}
    libdir:        %{_libdir}
    libexecdir:    %{_libdir}/apr
    mandir:        %{_mandir}
    sysconfdir:    %{_sysconfdir}
    datadir:       %{_datadir}
    installbuilddir: %{_datadir}/build
    includedir:    %{_includedir}
    localstatedir: %{_localstatedir}
    runtimedir:    %{_localstatedir}/run
    libsuffix:     -${APRUTIL_MAJOR_VERSION}
</Layout>
' > config.layout

%build
./buildconf \
	--with-apr=%{_datadir}/apr

%configure \
	--enable-layout=PLD \
	--with-apr=%{_bindir}/apr-1-config \
	--with-berkeley-db=%{_prefix} \
	--with-dbm=%{dbver} \
	--with-iconv=%{_prefix} \
%if %{with ldap}
	--with-ldap \
	--with-ldap-include=%{_prefix}/include \
	--with-ldap-lib=%{_libdir} \
%endif
	%{!?with_freetds:--without-freetds} \
	%{?with_mysql:--with-mysql=%{_prefix}} \
	%{!?with_odbc:--without-odbc} \
	%{?with_oracle:--with-oracle} \
	%{!?with_pgsql:--without-pgsql} \
	%{!?with_sqlite2:--without-sqlite2} \
	%{!?with_sqlite3:--without-sqlite3}

%{__make} \
	CC="%{__cc}"

%{?with_tests:%{__make} -j1 check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/apr-util-1/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_libdir}/libaprutil-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libaprutil-1.so.0
%dir %{_libdir}/apr-util-1

%files dbm-db
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbm_db-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbm_db.so

%if %{with freetds}
%files dbd-freetds
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_freetds-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_freetds.so
%endif

%if %{with mysql}
%files dbd-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_mysql-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_mysql.so
%endif

%if %{with odbc}
%files dbd-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_odbc-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_odbc.so
%endif

%if %{with oracle}
%files dbd-oracle
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_oracle-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_oracle.so
%endif

%if %{with pgsql}
%files dbd-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_pgsql-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_pgsql.so
%endif

%if %{with sqlite2}
%files dbd-sqlite2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_sqlite2-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_sqlite2.so
%endif

%if %{with sqlite3}
%files dbd-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_sqlite3-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_dbd_sqlite3.so
%endif

%if %{with ldap}
%files ldap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/apr-util-1/apr_ldap-1.so
%attr(755,root,root) %{_libdir}/apr-util-1/apr_ldap.so
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/apu-1-config
%attr(755,root,root) %{_libdir}/libaprutil-1.so
%{_libdir}/libaprutil-1.la
%{_libdir}/aprutil.exp
%{_includedir}
%{_pkgconfigdir}/apr-util-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libaprutil-1.a
