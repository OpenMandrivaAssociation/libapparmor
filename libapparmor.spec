%define major 1
%define libname %mklibname apparmor %{major}
%define develname %mklibname apparmor -d
%define svnrev 1310

Summary:	Main libraries for AppArmor
Name:		libapparmor
Version:	2.3
Release:	1.%{svnrev}.5
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
%attr(0644,root,root) %{_libdir}/*.a
%attr(0644,root,root) %{_includedir}/sys/*.h
%attr(0644,root,root) %{_mandir}/man2/aa_change_hat.2*

%files -n perl-libapparmor
%{perl_vendorarch}/auto/LibAppArmor
%{perl_vendorarch}/LibAppArmor.pm


%changelog
* Wed Jan 25 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2.3-1.1310.4
+ Revision: 768358
- svn commit -m mass rebuild of perl extension against perl 5.14.2
- cleanups

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3-1.1310.3mdv2011.0
+ Revision: 520749
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.3-1.1310.2mdv2010.0
+ Revision: 425514
- rebuild

* Sat Jan 03 2009 Eugeni Dodonov <eugeni@mandriva.com> 2.3-1.1310.1mdv2009.1
+ Revision: 323494
- Updated to current libapparmor version (as of SuSE 11.1 release).

* Wed Aug 06 2008 Luiz Fernando Capitulino <lcapitulino@mandriva.com> 2.3-1.1249.1mdv2009.0
+ Revision: 264632
- updated to version 2.3 svnrev 1249

* Mon Jun 09 2008 Pixel <pixel@mandriva.com> 2.2-1.1001.1mdv2009.0
+ Revision: 217188
- do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Feb 27 2008 Andreas Hasenack <andreas@mandriva.com> 2.2-1.1001.1mdv2008.1
+ Revision: 175915
- updated to version 2.2 svnrev 1001
- split out libapparmor

* Thu Jan 17 2008 Thierry Vignaud <tv@mandriva.org> 2.1-1.1076.2mdv2008.1
+ Revision: 154124
- rebuild for new perl

* Tue Jan 08 2008 Andreas Hasenack <andreas@mandriva.com> 2.1-1.1076.1mdv2008.1
+ Revision: 146893
- updated to svn revision 1076

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.5mdv2008.0
+ Revision: 91191
- remove more profiles from standard package: they are shipped in their own packages now

* Wed Sep 19 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.4mdv2008.0
+ Revision: 91061
- drop rpcbind profile, it's shipped in the rpcbind package now

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.3mdv2008.0
+ Revision: 85766
- bonobo file is under a noarch libdir
- build dbus and gnome applet packages

* Fri Sep 14 2007 Andreas Hasenack <andreas@mandriva.com> 2.1-1.961.1mdv2008.0
+ Revision: 85546
- install perl module in arch dir as the makefile does for x86_64 (doesn't seem right, though)
- make it not require an installed libapparmor-devel to build
- added swig to buildrequires
- added profile for rpcbind
- fix default syslog profile
- obsolete apparmor-docs (manpages are in each package now)
- better place for the LibAppArmor module
- build apache-mod_apparmor package
- install LibAppArmor.pm
- added utils subpackage
- Import apparmor

