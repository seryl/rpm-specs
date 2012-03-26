%define tmuxver		1.6

Name:		tmux
Version:	%{tmuxver}
Release:	1%{?dist}
License:	BSD
URL:		http://tmux.sourceforce.net/
Provides:       tmux(abi) = %{tmuxver}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	readline readline-devel ncurses ncurses-devel libevent libevent-devel gcc make
Source0:	http://downloads.sourceforce.net/tmux/tmux-%{tmuxver}.tar.gz
Summary:	tmux is a terminal multiplexer. It is a BSD-licensed alternative to screen.
Group:		Development/Languages
Provides: tmux(abi) = %{tmuxver}

%description
tmux is a terminal multiplexer: it enables a number of terminals (or windows), each running a separate program, to be created, accessed, and controlled from a single screen. tmux may be detached from a screen and continue running in the background, then later reattached.

tmux is intended to be a modern, BSD-licensed alternative to programs such as GNU screen.

%prep
%setup -n tmux-%{tmuxver}
%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

# we don't want to keep the src directory
rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%{_bindir}
%{_datadir}

%changelog
* Mon Mar 26 2012 Josh Toft <joshtoft@gmail.com> - 1.6-1
- Updated to 1.6

* Wed Aug 20 2011 Josh Toft <joshtoft@gmail.com> - 1.5-1
- Initial Spec File

