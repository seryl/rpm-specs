%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global pkgname boto

Summary:	A simple lightweight interface to Amazon Web Services
Name:		python-boto
Version:	1.9b
Release:	7%{?dist}
License:	MIT
Group:		Development/Languages
URL:		http://code.google.com/p/%{pkgname}/
Source:		http://boto.googlecode.com/files/%{pkgname}-%{version}.tar.gz
Patch0:		python-boto-1.9b-image.patch
Patch1:		python-boto-1.9b-prefix.patch
Patch2:		python-boto-1.9b-python27.patch
Patch3:		python-boto-1.9b-python24.patch
BuildRequires:	python-devel, python-setuptools-devel
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Boto is a Python package that provides interfaces to Amazon Web Services.
It supports S3 (Simple Storage Service), SQS (Simple Queue Service) via
the REST API's provided by those services and EC2 (Elastic Compute Cloud)
via the Query API. The goal of boto is to provide a very simple, easy to
use, lightweight wrapper around the Amazon services.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1 -b .image
%patch1 -p1 -b .prefix
%patch2 -p1 -b .python27
%patch3 -p1 -b .python24

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/elbadmin
%{_bindir}/fetch_file
%{_bindir}/launch_instance
%{_bindir}/list_instances
%{_bindir}/s3put
%{_bindir}/sdbadmin
%{_bindir}/taskadmin
%{python_sitelib}/*

%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9b-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 02 2011 Robert Scheck <robert@fedoraproject.org> 1.9b-6
- Added a patch for python 2.4 support (#656446, #661233)

* Thu Dec 02 2010 Lubomir Rintel <lubo.rintel@gooddata.com> 1.9b-5
- Apply a patch for python 2.7 support (#659248)

* Thu Nov 18 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-4
- Added patch to fix parameter of build_list_params() (#647005)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.9b-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Feb 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-2
- Backported upstream patch for image registration (#561216)

* Sat Jan 09 2010 Robert Scheck <robert@fedoraproject.org> 1.9b-1
- Upgrade to 1.9b

* Fri Jul 24 2009 Robert Scheck <robert@fedoraproject.org> 1.8d-1
- Upgrade to 1.8d (#513560)

* Wed Jun 03 2009 Luke Macken <lmacken@redhat.com> 1.7a-2
- Add python-setuptools-devel to our build requirements, for egg-info

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> 1.7a-1
- Upgrade to 1.7a

* Mon Feb 23 2009 Robert Scheck <robert@fedoraproject.org> 1.5c-2
- Rebuild against rpm 4.6

* Sun Dec 07 2008 Robert Scheck <robert@fedoraproject.org> 1.5c-1
- Upgrade to 1.5c

* Fri Dec 05 2008 Jeremy Katz <katzj@redhat.com> 1.2a-2
- Rebuild for python 2.6

* Wed May 07 2008 Robert Scheck <robert@fedoraproject.org> 1.2a-1
- Upgrade to 1.2a

* Sat Feb 09 2008 Robert Scheck <robert@fedoraproject.org> 1.0a-1
- Upgrade to 1.0a

* Sat Dec 08 2007 Robert Scheck <robert@fedoraproject.org> 0.9d-1
- Upgrade to 0.9d

* Thu Aug 30 2007 Robert Scheck <robert@fedoraproject.org> 0.9b-1
- Upgrade to 0.9b
- Initial spec file for Fedora and Red Hat Enterprise Linux
