%global realname protobuffs
%global debug_package %{nil}
%global git_tag 58ff962


Name:		erlang-%{realname}
Version:	0
Release:	0.4.20100930git%{git_tag}%{?dist}
Summary:	A set of Protocol Buffers tools and modules for Erlang applications
Group:		Development/Libraries
License:	MIT
URL:		http://github.com/ngerakines/erlang_protobuffs
# wget http://github.com/ngerakines/erlang_protobuffs/tarball/58ff962
Source0:	ngerakines-erlang_%{realname}-%{git_tag}.tar.gz
# All patches below were taken from Basho's fork
Patch1:		erlang-protobuffs-0001-Test-changes-to-see-if-leaving-the-encoded-protocol-.patch
Patch2:		erlang-protobuffs-0002-Added-debug-info-to-generated-beams.patch
Patch3:		erlang-protobuffs-0003-Teach-protobuffs-how-to-skip-directives-it-doesn-t-u.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
BuildRequires:	erlang-etap
# For /usr/bin/prove
BuildRequires:	perl(Test::Harness)
Requires:	erlang-compiler
Requires:	erlang-erts >= R12B-5
Requires:	erlang-kernel
Requires:	erlang-stdlib >= R12B-5


%description
A set of Protocol Buffers tools and modules for Erlang applications.


%prep
%setup -q -n ngerakines-erlang_%{realname}-%{git_tag}
%patch1 -p1 -b .p1
%patch2 -p1 -b .p2
%patch3 -p1 -b .p3
mkdir ebin
sed -i -e "s,\.\.\/src,\.\.\/ebin,g" tests/*.t


%build
erlc +debug_info -o ebin src/*erl


%install
rm -rf $RPM_BUILD_ROOT
install -D -m 644 ebin/%{realname}.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
install -m 644 ebin/%{realname}.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_compile.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/%{realname}_parser.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/
install -m 644 ebin/pokemon_pb.beam $RPM_BUILD_ROOT%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/


%clean
rm -rf $RPM_BUILD_ROOT


%check
cd ./tests && ./runtests.sh


%files
%defattr(-,root,root,-)
%doc AUTHORS
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/pokemon_pb.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_compile.beam
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}_parser.beam


%changelog
* Fri Mar 11 2011 Peter Lemenkov <lemenkov@gmail.com> -  0-0.4.20100930git58ff962
- Added three patches from Basho's fork (required for riak_client)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20100930git58ff962
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct  5 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.2.20100930git58ff962
- Fixed License tag

* Thu Sep 30 2010 Peter Lemenkov <lemenkov@gmail.com> - 0-0.1.20100930git58ff962
- Initial package
