%global realname oauth
%global debug_package %{nil}
%global git_tag 2c9269b


Name:		erlang-%{realname}
Version:	1.0.1
Release:	1%{?dist}
Summary:	An Erlang OAuth implementation
Group:		Development/Languages
License:	MIT
URL:		http://github.com/tim/erlang-oauth
# wget --no-check-certificate https://github.com/tim/erlang-oauth/tarball/v1.0.1
Source0:	tim-%{name}-v%{version}-0-g%{git_tag}.tar.gz
Patch1:		erlang-oauth-0001-Use-http-instead-of-httpc-in-old-Erlang.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-public_key >= R12B
BuildRequires:	erlang-tools
Requires:	erlang-crypto
Requires:	erlang-erts
Requires:	erlang-inets
Requires:	erlang-kernel
Requires:	erlang-public_key >= R12B
Requires:	erlang-stdlib >= R12B
Requires:	erlang-xmerl


%description
An Erlang OAuth implementation.


%prep
%setup -q -n tim-%{name}-%{git_tag}
%if 0%{?el5}
# Erlang/OTP R12B5
%patch1 -p1 -b .no_httpc_request_4
%endif


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
install -D -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc License.txt README.txt
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_client.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_hmac_sha1.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_http.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_plaintext.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_rsa_sha1.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_unix.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_uri.beam


%changelog
* Fri Nov 26 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.0.1-1
- First stable release (this is the same as git7d85d3e with the patch no. 1)

* Wed Sep 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.6.git7d85d3e
- Narrowed BuildRequires
- New git snapshot

* Mon Jul 12 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.5.gite8aecf0
- Rebuild with new Erlang R14A
- Simplified spec-file
- Added missing requirement - erlang-kernel

* Fri May 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.4.gite8aecf0
- Fixed CouchDB failure (see rhbz #597093)
- Fixed reqirements for F-11

* Thu May 27 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.3.gite8aecf0
- Fixed explicit requires on EL-[45]

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.2.gite8aecf0
- Narrowed explicit requires

* Wed Apr  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.gite8aecf0
- initial package

