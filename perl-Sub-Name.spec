%{?scl:%scl_package perl-Sub-Name}
%{!?scl:%global pkg_name %{name}}

# Only need manual requires for "use base XXX;" prior to rpm 4.9
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e')

Name:		%{?scl_prefix}perl-Sub-Name
Version:	0.05
Release:	12%{?dist}
Summary:	Name - or rename - a sub
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Sub-Name/
Source0:	http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/Sub-Name-%{version}.tar.gz
Patch0:		Sub-Name-0.05-cpan50524.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(DynaLoader)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(Test::More)
BuildRequires:	%{?scl_prefix}perl(warnings)
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
%if ! %{rpm49}
Requires:	%{?scl_prefix}perl(DynaLoader)
Requires:	%{?scl_prefix}perl(Exporter)
%endif

# Don't "provide" private perl objects
%{?perl_default_filter}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /\.so()/d
%filter_setup
%endif

%description
This module allows one to "name" or rename subroutines, including anonymous
ones.

Note that this is mainly for aid in debugging; you still cannot call the sub
by the new name (without some deep magic).

%prep
%setup -q -n Sub-Name-%{version}

# Copy the contents of the %%DB::sub entry if it exists (CPAN RT#50524)
%patch0 -p1

%build
%{?scl:scl enable %{scl} '}
perl Makefile.PL INSTALLDIRS=vendor optimize="%{optflags}"
%{?scl:'}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/auto/Sub/
%{perl_vendorarch}/Sub/
%{_mandir}/man3/Sub::Name.3pm*

%changelog
* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.05-12
- Rebuilt for SCL

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.05-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.05-7
- Perl 5.16 rebuild

* Sat Feb 18 2012 Paul Howarth <paul@city-fan.org> - 0.05-6
- Add patch for CPAN RT#50524 (copy contents of %%DB::sub entry if it exists)
- Reinstate compatibility with old distributions like EL-5
  - Add BuildRoot definition
  - Clean buildroot in %%install
  - Restore %%clean section
  - Restore %%defattr
  - Don't use + to terminate find -exec commands
- Spec clean-up
  - Make %%files list more explicit
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Don't use macros for commands
  - Use tabs
  - Add buildreqs for Perl core modules that might be dual-lived
  - Explicit requires for "use base XXX;" only required prior to rpm 4.9

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-2
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat Dec 18 2010 Iain Arnell <iarnell@gmail.com> - 0.05-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild
- BR perl(Test::More)
- Requires perl(DynaLoader) and perl(Exporter)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-5
- Rebuild against perl 5.10.1

* Thu Aug 27 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-4
- Filtering errant private provides

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 03 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update to 0.04

* Sat Mar 15 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.03-1
- Update to 0.03

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-5
- Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.02-4.1
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.02-3.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-3
- Bump

* Wed Sep 06 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-2
- Bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Specfile autogenerated by cpanspec 1.69.1
