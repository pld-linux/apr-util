%define snap	20030913101715
Summary:	A companion library to Apache Portable Runtime
Name:		apr-util
Version:	0.9.4
Release:	0.%{snap}.1
Epoch:		1
License:	Apache
Group:		Libraries
# http://www.apache.org/dist/apr/%{name}-%{version}.tar.gz
Source0:	http://cvs.apache.org/snapshots/apr-util/%{name}_%{snap}.tar.gz
# Source0-md5:	00e26d0d77e1265c3bd45d11e9d8457d
URL:		http://apr.apache.org/
BuildRequires:	apr-devel >= 1:0.9.4
BuildRequires:	openldap-devel
BuildRequires:	expat-devel
BuildRequires:	db3-devel
BuildRequires:	gdbm-devel
BuildRequires:	libtool
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_includedir	/usr/include/apr-util

%description
A companion library to Apache Portable Runtime.

%package devel
Summary:	Header files and develpment documentation for apr-util
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
Header files and develpment documentation for apr-util.

%package static
Summary:	Static apr-util library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}

%description static
Static apr-util library.

%prep
%setup  -q -n %{name}

%build
./buildconf
%configure \
	--with-apr=%{_bindir}/apr-config \
	--with-ldap-include=%{_includedir} \
	--with-ldap-lib=%{_libdir} \
	--with-iconv=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

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
