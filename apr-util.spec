
%bcond_without	ldap	# without LDAP support

Summary:	A companion library to Apache Portable Runtime
Summary(pl):	Biblioteka towarzysz±ca Apache Portable Runtime
Name:		apr-util
Version:	0.9.5
Release:	2
Epoch:		1
License:	Apache
Group:		Libraries
Source0:	http://www.apache.org/dist/apr/%{name}-0.9.4.tar.gz
# Source0-md5:	909ff60d9efb3f158d33e4569af57874
Patch0:		%{name}-link.patch
Patch1:		%{name}-0.9.4_0.9.5.patch
URL:		http://apr.apache.org/
BuildRequires:	apr-devel >= 1:0.9.4
BuildRequires:	autoconf
BuildRequires:	db-devel
BuildRequires:	expat-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool
%{?with_ldap:BuildRequires:	openldap-devel}
Requires:	apr >= 1:0.9.4
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
Requires:	apr-devel >= 1:0.9.4
Requires:	db-devel
Requires:	expat-devel
Requires:	gdbm-devel
%{?with_ldap:Requires:	openldap-devel}

%description devel
Header files and development documentation for apr-util.

%description devel -l pl
Pliki nag³ówkowe i dokumentacja programisty do apr-util.

%package static
Summary:	Static apr-util library
Summary(pl):	Statyczna biblioteka apr-util
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Conflicts:	apr-static < 1:0.9

%description static
Static apr-util library.

%description static -l pl
Statyczna biblioteka apr-util.

%prep
%setup -q -n %{name}-0.9.4
%patch0 -p1
%patch1 -p1

%build
./buildconf \
	--with-apr=%{_datadir}/apr
%configure \
	--with-apr=%{_bindir}/apr-config \
%{?with_ldap:	--with-ldap} \
%{?with_ldap:	--with-ldap-include=%{_prefix}/include} \
%{?with_ldap:	--with-ldap-lib=%{_libdir}} \
	--with-iconv=%{_prefix}
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
%doc CHANGES STATUS
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/aprutil.exp
%{_includedir}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
