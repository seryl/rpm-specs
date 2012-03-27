%global realname mustache
%global debug_package %{nil}
%global git_tag 795a15f


Name:		erlang-%{realname}
Version:	0.1.0
Release:	2%{?dist}
Summary:	Mustache template engine for Erlang
Group:		Development/Languages
License:	MIT
URL:		http://github.com/mojombo/mustache.erl
# wget http://github.com/mojombo/mustache.erl/tarball/v0.1.0
Source0:	mojombo-%{realname}.erl-v%{version}-0-g%{git_tag}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	erlang-erts
Requires:	erlang-erts >= R12B-5
Requires:	erlang-kernel >= R12B-5
Requires:	erlang-stdlib >= R12B-5

%description
An Erlang port of Mustache for Ruby. Mustache is a framework-agnostic template
system that enforces separation of view logic from the template file. Indeed, it
is not even possible to embed logic in the template. This allows templates to be
reused across language boundaries and for other language independent uses.


%prep
%setup -q -n mojombo-%{realname}.erl-%{git_tag}


%build
erlc +debug_info %{realname}.erl


%install
rm -rf %{buildroot}
install -D -m 644 %{realname}.beam %{buildroot}%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc examples/ LICENSE README.md
%dir %{_libdir}/erlang/lib/%{realname}-%{version}
%dir %{_libdir}/erlang/lib/%{realname}-%{version}/ebin
%{_libdir}/erlang/lib/%{realname}-%{version}/ebin/%{realname}.beam


%changelog
* Thu Oct 28 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.1.0-2
- Ensure consistency in macro usage

* Fri Oct  1 2010 Peter Lemenkov <lemenkov@gmail.com> - 0.1.0-1
- Initial build

