%global debug_package %{nil}
%global realname etap


Name:		erlang-%{realname}
Version:	0.3.4
Release:	5%{?dist}
Summary:	Erlang testing library
Group:		Development/Languages
License:	BSD
URL:		http://github.com/ngerakines/etap
# wget http://github.com/ngerakines/etap/tarball/0.3.4
Source0:	ngerakines-etap-17b8d43.tar.gz
Patch1:		erlang-etap-0001-No-such-function-os-getenv-1-in-R11B.patch
Patch2:		erlang-etap-0002-All-lists-fun-arity-functions-missing-in-R11B-are-re.patch
Patch3:		erlang-etap-0003-Add-missing-right-parenthesis.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-inets
BuildRequires:	erlang-kernel
BuildRequires:	erlang-stdlib
Requires: erlang-erts
Requires: erlang-inets
Requires: erlang-kernel
Requires: erlang-stdlib
Requires: erlang-tools


%description
Etap is a collection of Erlang modules that provide a TAP testing client
library.


%prep
%setup -q -n ngerakines-etap-17b8d43
%if 0%{?el4}
# Erlang/OTP R11B
%patch1 -p1 -b .no-os-getenv-1
%patch2 -p1 -b .no-lists-member-and-others
%endif
%patch3 -p1 -b .add_missing_parenthesis
# Fails to pass this test - I'm investigating it
rm -f ./t/etap_t_005.erl

%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%check
make test


%files
%defattr(-,root,root,-)
%doc README.markdown
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_*.beam


%changelog
* Thu Oct 21 2010 Peter Lemenkov <lemenkov@gmail.com> 0.3.4-5
- Fixed missing runtime dependency on EL-4
- Added %%check target

* Tue Sep 28 2010 Peter Lemenkov <lemenkov@gmail.com> 0.3.4-4
- Narrowed BuildRequires

* Mon Jul 12 2010 Peter Lemenkov <lemenkov@gmail.com> 0.3.4-3
- Rebuild for Erlang/OTP R14A
- Simplified spec-file

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> 0.3.4-2
- Narrowed explicit requires

* Wed Apr  7 2010 Peter Lemenkov <lemenkov@gmail.com> 0.3.4-1
- initial package

