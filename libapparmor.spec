%define major 1
%define libname %mklibname apparmor %{major}
%define develname %mklibname apparmor -d
%define svnrev 1310

Summary:	Main libraries for AppArmor
Name:		libapparmor
Version:	2.3
Release:	1.%{svnrev}.3
License:	LGPL
Group:		System/Libraries
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	libapparmor-%{version}-%{svnrev}.tar.gz
Buildrequires:  libtool
Buildrequires:  perl-devel
Buildrequires:  flex
Buildrequires:  bison
Buildrequires:  swig

%description
AppArmor is a security framework that proactively protects the operating system
and applications. This package contains the main library for AppArmor.

%package -n	%{libname}
Summary:	Main libraries for %{name}
Group:		System/Libraries
License:        LGPL

%description -n	%{libname}
This package contains the AppArmor library.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libapparmor-devel = %{version}-%{release}
Provides:	apparmor-devel = %{version}-%{release}
Obsoletes:	%{mklibname apparmor 1 -d}

%description -n %{develname}
This package contains development files for %{name}.

%package -n     perl-libapparmor
Summary:        AppArmor module for perl
Group:          Development/Perl
Requires:       %{libname} = %{version}

%description -n perl-libapparmor
This package contains the AppArmor module for perl.


%prep
%setup -q -n %{name}-%{version}-%{svnrev}
./autogen.sh

%build
%serverbuild

%configure --with-perl
%make CFLAGS="$RPM_OPT_FLAGS" TESTBUILDDIR=$(pwd)

%install
# lib
%makeinstall_std LIB=%{_lib} LIBDIR=%{_libdir}
# XXX - for some reason, on i586 builds this file is not copied
install -m 0644 swig/perl/LibAppArmor.pm %{buildroot}%{perl_vendorarch}

%files -n %{libname}
%doc COPYING.LGPL AUTHORS
%attr(0755,root,root) /%{_libdir}/*.so.*

%files -n %{develname}
%doc README
%{_includedir}/aalogparse/
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_includedir}/sys/*.h
%attr(0644,root,root) %{_mandir}/man2/aa_change_hat.2*

%files -n perl-libapparmor
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm
