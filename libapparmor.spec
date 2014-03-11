%define major 1
%define libname %mklibname apparmor %{major}
%define libimmunix %mklibname immunix %{major}
%define devname %mklibname apparmor -d
%define svnrev 1310

Summary:	Main libraries for AppArmor
Name:		libapparmor
Version:	2.3
Release:	1.%{svnrev}.6
License:	LGPLv2.1+
Group:		System/Libraries
Url:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	libapparmor-%{version}-%{svnrev}.tar.gz
Buildrequires:	bison
Buildrequires:	flex
Buildrequires:	libtool
Buildrequires:	swig
Buildrequires:	perl-devel

%description
AppArmor is a security framework that proactively protects the operating system
and applications. This package contains the main library for AppArmor.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the AppArmor library.

%files -n %{libname}
%doc COPYING.LGPL AUTHORS
%{_libdir}/libapparmor.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libimmunix}
Summary:	Shared library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}apparmor1 < 2.3-1.1310.6

%description -n %{libimmunix}
This package contains the AppArmor library.

%files -n %{libimmunix}
%doc COPYING.LGPL AUTHORS
%{_libdir}/libimmunix.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libimmunix} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	apparmor-devel = %{EVRD}

%description -n %{devname}
This package contains development files for %{name}.

%files -n %{devname}
%doc README
%{_includedir}/aalogparse/
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/sys/*.h
%{_mandir}/man2/aa_change_hat.2*

#----------------------------------------------------------------------------

%package -n perl-libapparmor
Summary:	AppArmor module for perl
Group:		Development/Perl
Requires:	%{libname} = %{EVRD}
Requires:	%{libimmunix} = %{EVRD}

%description -n perl-libapparmor
This package contains the AppArmor module for perl.

%files -n perl-libapparmor
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-%{svnrev}
find . -name "Makefile*" -o -name "*.m4" -o -name "configure*" |xargs sed -i -e 's,configure.in,configure.ac,g'

%build
./autogen.sh
%serverbuild
%configure2_5x \
	--with-perl \
	--enable-static
%make CFLAGS="%{optflags}" TESTBUILDDIR=$(pwd)

%install
# lib
%makeinstall_std LIB=%{_lib} LIBDIR=%{_libdir}
# XXX - for some reason, on i586 builds this file is not copied
install -m 0644 swig/perl/LibAppArmor.pm %{buildroot}%{perl_vendorarch}

