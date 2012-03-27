%global realname neotoma
%global debug_package %{nil}
%global git_tag adb132b


Name:		erlang-%{realname}
Version:	1.5
Release:	1%{?dist}
Summary:	Erlang library and packrat parser-generator for parsing expression grammars
Group:		Development/Languages
License:	MIT
URL:		http://github.com/seancribbs/neotoma
# wget --no-check-certificate https://github.com/seancribbs/neotoma/tarball/1.5
Source0:	seancribbs-%{realname}-%{version}-0-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-eunit
BuildRequires:	erlang-rebar
# ets:insert/2 ( >= R12B-5 )
# ets:insert_new/2 ( >= R12B-5 )
# ets:lookup/2 ( >= R12B-5 )
# ets:new/2 ( >= R12B-5 )
# re:compile/1 ( >= R12B-5 )
# re:run/2 ( >= R12B-5 )
Requires:	erlang-erts >= R12B-5
Requires:	erlang-kernel
# re:replace/4 ( >= R12B-5 )
# string:join/2 ( >= R12B-5 )
# unicode:characters_to_list/1 ( >= R13B )
Requires:	erlang-stdlib >= R13B


%description
Erlang library and packrat parser-generator for parsing expression grammars.


%prep
%setup -q -n seancribbs-%{realname}-%{git_tag}


%build
rebar -v compile


%install
rm -rf %{buildroot}
install -p -m 0644 -D ebin/%{realname}.app %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
install -p -m 0644 ebin/%{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_parse.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 ebin/%{realname}_peg.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin
install -p -m 0644 -D priv/peg_includes.hrl %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv/peg_includes.hrl
install -p -m 0644 priv/neotoma_parse.peg %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/priv


%clean
rm -rf %{buildroot}


%check
rebar eunit


%files
%defattr(-,root,root,-)
%doc extra/ LICENSE README.textile
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/priv
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.app
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_parse.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_peg.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/peg_includes.hrl
%{_libdir}/erlang/lib/%{realname}-%{version}/priv/neotoma_parse.peg


%changelog
* Sat Mar 26 2011 Peter Lemenkov <lemenkov@gmail.com> - 1.5-1
- Ver. 1.5
- Requires R13B or higher
- BuildRequires rebar

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4-2
- Ensure consistency in macro usage

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.4-1
- Initial build
