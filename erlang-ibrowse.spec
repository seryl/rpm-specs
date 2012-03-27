%global realname ibrowse
%global debug_package %{nil}
%global git_tag 8c46b10


Name:		erlang-%{realname}
Version:	2.2.0
Release:	4%{?dist}
Summary:	Erlang HTTP client
Group:		Development/Languages
License:	BSD or LGPLv2+
URL:		http://github.com/cmullaparthi/ibrowse
# wget --no-check-certificate https://github.com/cmullaparthi/ibrowse/tarball/v2.1.3
Source0:	cmullaparthi-%{realname}-v%{version}-0-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-eunit
%if 0%{?el6}%{?fc14}%{?fc15}%{?fc16}
# FIXME
BuildRequires:	erlang-rebar
%endif
BuildRequires:	sed
Requires:	erlang-erts
Requires:	erlang-kernel
Requires:	erlang-sasl
Requires:	erlang-ssl
Requires:	erlang-stdlib


%description
Erlang HTTP client.


%prep
%setup -q -n cmullaparthi-%{realname}-%{git_tag}
iconv -f iso8859-1 -t utf-8 README > README.utf8 && \
	mv -f README.utf8 README || rm -f README.utf8
rm -f ebin/%{realname}.app

# FIX  version
sed -i -e "s,\"2.1.3\",\"2.2.0\",g" src/ibrowse.app.src

# Wait until we'll add rebar to EL-5
#sed -i -e "s,./rebar,rebar -v,g" Makefile


%build
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT%{_libdir}/erlang
rm -f $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_test.beam
sed -i -e "s,\,ibrowse_test,,g" $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 -D src/ibrowse.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include/ibrowse.hrl


%clean
rm -rf $RPM_BUILD_ROOT


%check
make test


%files
%defattr(-,root,root,-)
%doc BSD_LICENSE LICENSE README
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/include
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_app.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_http_client.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_lb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_lib.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_sup.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/include/%{realname}.hrl


%changelog
* Fri Sep 02 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-4
- Removed mentioning about test file from *.app

* Tue Jul 12 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-3
- Fix building on EL-5

* Sun May 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-2
- Added missing build requirements

* Sun May 15 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.2.0-1
- Ver. 2.2.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.1.3-1
- Ver. 2.1.3

* Wed Nov 10 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.1.0-1
- Ver. 2.1.0

* Tue Sep 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 2.0.1-1
- Ver. 2.0.1
- Narrowed BuildRequires

* Sun Jul 11 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.4.20100601git07153bc
- Add missing runtime requirement - erlang-sasl
- Rebuild with Erlang/OTP R14A

* Tue Jun  8 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.3.20100601git07153bc
- Also install header file

* Tue Jun  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.2.20100601git07153bc
- New git snapshot (with clarified licensing terms)

* Thu May 27 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.6.0-0.1.gita114ed3b
- Ver 1.6.0 from git with one patch ahead.

* Thu May 13 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.5.6-2
- Narrowed explicit requires

* Wed Apr  7 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.5.6-1
- initial package

