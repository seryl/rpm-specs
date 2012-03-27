%global realname getopt
%global debug_package %{nil}
%global git_tag 8f54692


Name:		erlang-%{realname}
Version:	0.3
Release:	3%{?dist}
Summary:	Erlang module to parse command line arguments using the GNU getopt syntax

Group:		Development/Libraries
License:	BSD
URL:		http://github.com/jcomellas/getopt
# wget http://github.com/jcomellas/getopt/tarball/v0.3
Source0:	jcomellas-%{realname}-v%{version}-0-g%{git_tag}.tar.gz
Patch1:		erlang-getopt-0001-No-such-type-boolean-in-R12B.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	erlang-erts
#BuildRequires:	erlang-rebar
Requires:	erlang-erts >= R12B-5
Requires:	erlang-kernel >= R12B-5
Requires:	erlang-stdlib >= R12B-5


%description
Command-line parsing module that uses a syntax similar to that of GNU getopt.

%prep
%setup -q -n jcomellas-%{realname}-8f54692
%if 0%{?el5}
%patch1 -p1 -b .unknown_type_boolean
%endif
chmod 0644 examples/*.escript


%build
#make %{?_smp_mflags}
erlc -o ebin src/%{realname}.erl


%check
#make test


%install
rm -rf $RPM_BUILD_ROOT
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -D -m 644 ebin/%{realname}.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.markdown examples/
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Wed Oct  6 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-3
- Fix building on EPEL-5

* Tue Oct  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-2
- Fixed License tag
- Doc-files now have 644 mode

* Thu Sep 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.3-1
- Initial package
- Disabled %%check section until rebar will be available

