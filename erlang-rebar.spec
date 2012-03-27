%global realname rebar
%global debug_package %{nil}
%global git_tag 90058c7


Name:		erlang-%{realname}
Version:	2
Release:	3.20101120git%{git_tag}%{?dist}
Summary:	Erlang Build Tools
Group:		Development/Tools
License:	MIT
URL:		https://github.com/basho/rebar
# wget --no-check-certificate https://github.com/basho/rebar/tarball/90058c7
Source0:	basho-%{realname}-RELEASE-1-327-g%{git_tag}.tar.gz
Source1:	rebar.escript
Patch1:		rebar-0001-No-need-to-create-bundle.patch
Patch2:		rebar-0002-Remove-bundled-mustache.patch
Patch3:		rebar-0003-Remove-bundled-getopt.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts >= R13B-03
BuildRequires:	erlang-getopt
BuildRequires:	erlang-reltool
Requires:	erlang-asn1
Requires:	erlang-compiler
Requires:	erlang-crypto
Requires:	erlang-dialyzer
Requires:	erlang-edoc
Requires:	erlang-erlydtl
Requires:	erlang-erts
Requires:	erlang-eunit
Requires:	erlang-getopt
Requires:	erlang-kernel
Requires:	erlang-lfe
Requires:	erlang-mustache
Requires:	erlang-neotoma
Requires:	erlang-protobuffs
Requires:	erlang-reltool
Requires:	erlang-snmp
Requires:	erlang-stdlib
Requires:	erlang-syntax_tools
Requires:	erlang-tools
Provides:	%{realname} = %{version}-%{release}


%description
Erlang Build Tools.


%prep
%setup -q -n basho-%{realname}-%{git_tag}
%patch1 -p1 -b .no_bundle
%patch2 -p1 -b .remove_bundled_mustache
%patch3 -p1 -b .remove_bundled_getopt


%build
./bootstrap


%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/rebar
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include
install -m 644 ebin/%{realname}.app $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 ebin/*.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -m 644 include/*.hrl $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/include
cp -a priv $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc THANKS rebar.config.sample
%{_bindir}/rebar
%{_libdir}/erlang/lib/%{realname}-%{version}


%changelog
* Mon Nov 22 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-3.20101120git90058c7
- Added missing buildrequires

* Sat Nov 20 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-2.20101120git90058c7
- Removed bundled mustache and getopt
- Fixed license tag
- Removed wrong license text from package
- Simplified %%files section
- Fixed links (project was moved to GitHub)
- Changed versioning scheme (post-release)

* Sun Sep  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 2-1
- Initial build

