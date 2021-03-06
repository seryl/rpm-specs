# $Id$
# Authority: cmr
# Upstream: The icinga devel team <icinga-devel at lists.sourceforge.net>
#
# Needs libdbi
#
# ExclusiveDist: el5 el6

%define logdir %{_localstatedir}/log/icinga

%define apacheconfdir  %{_sysconfdir}/httpd/conf.d
%define apacheuser apache

Summary: Open Source host, service and network monitoring program
Name: icinga
Version: 1.5.1
Release: 1%{?dist}
License: GPLv2
Group: Applications/System
URL: http://www.icinga.org/

Source0: http://dl.sf.net/icinga/icinga-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc
BuildRequires: gd-devel > 1.8
BuildRequires: httpd
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: libdbi-devel
BuildRequires: perl(ExtUtils::Embed)
### Requires: nagios-plugins
Provides: nagios

%description
Icinga is an application, system and network monitoring application.
It can escalate problems by email, pager or any other medium. It is
also useful for incident or SLA reporting.

Icinga is written in C and is designed as a background process,
intermittently running checks on various services that you specify.

The actual service checks are performed by separate "plugin" programs
which return the status of the checks to Icinga.

Icinga is a fork of the nagios project.

%package gui
Summary: Web content for %{name}
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: httpd
Requires: %{name}-doc

%description gui
This package contains the webgui (html,css,cgi etc.) for %{name}

%package idoutils
Summary: database broker module for %{name}
Group: Applications/System
Requires: %{name} = %{version}-%{release}

%description idoutils
This package contains the idoutils broker module for %{name} which provides
database storage via libdbi.

%package api
Summary: PHP api for %{name}
Group: Applications/System
Requires: php

%description api
PHP api for %{name}

%package doc
Summary: documentation %{name}
Group: Documentation

%description doc
Documentation for %{name}


%prep
%setup -qn %{name}-%{version}

%build
%configure \
    --datadir="%{_sysconfdir}/icinga/share" \
    --datarootdir="%{_sysconfdir}/icinga/share" \
    --libexecdir="%{_sysconfdir}/icinga/libexec" \
    --localstatedir="%{_sysconfdir}/icinga/var" \
    --with-checkresult-dir="%{_sysconfdir}/icinga/var/checkresults" \
    --sbindir="%{_sysconfdir}/icinga/sbin" \
    --sysconfdir="%{_sysconfdir}/icinga/etc" \
    --with-cgiurl="/icinga/cgi-bin" \
    --with-command-user="icinga" \
    --with-command-group="icingacmd" \
    --with-gd-lib="%{_libdir}" \
    --with-gd-inc="%{_includedir}" \
    --with-htmurl="/icinga" \
    --with-init-dir="%{_initrddir}" \
    --with-lockfile="%{_sysconfdir}/icinga/var/icinga.pid" \
    --with-mail="/bin/mail" \
    --with-icinga-user="icinga" \
    --with-icinga-group="icinga" \
    --with-template-objects \
    --with-template-extinfo \
    --enable-event-broker \
    --enable-embedded-perl \
    --with-httpd-conf=%{apacheconfdir} \
    --with-init-dir=%{_initrddir} \
    --with-log-dir=%{logdir} \
    --with-cgi-log-dir=%{logdir}/gui \
    --with-phpapi-log-dir=%{logdir}/api \
    --with-p1-file-dir="%{_libdir}/icinga"
%{__make} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}
%{__mkdir} -p %{buildroot}/%{apacheconfdir}
%{__make} install-unstripped \
    install-init \
    install-commandmode \
    install-config \
    install-webconf \
    install-idoutils \
    install-api \
    DESTDIR="%{buildroot}" \
    INSTALL_OPTS="" \
    INSTALL_OPTS_WEB="" \
    COMMAND_OPTS="" \
    INIT_OPTS=""

### strip binary
%{__strip} %{buildroot}%{_bindir}/{icinga,icingastats}
%{__strip} %{buildroot}%{_sysconfdir}/icinga/sbin/*.cgi

### copy idoutils db-script
cp -r module/idoutils/db %{buildroot}%{_sysconfdir}/icinga/etc/idoutils



%pre
# Add icinga user
/usr/sbin/groupadd icinga 2> /dev/null || :
/usr/sbin/groupadd icingacmd 2> /dev/null || :
/usr/sbin/useradd -c "icinga" -s /sbin/nologin -r -d /var/icinga -G icingacmd -g icinga icinga 2> /dev/null || :


%post
/sbin/chkconfig --add icinga

%preun
if [ $1 -eq 0 ]; then
    /sbin/service icinga stop &>/dev/null || :
    /sbin/chkconfig --del icinga
fi

%pre gui
# Add apacheuser in the icingacmd group
  /usr/sbin/usermod -a -G icingacmd %{apacheuser}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,icinga,icinga,-)
%attr(755,root,root) %{_initrddir}/icinga
%dir %{_sysconfdir}/icinga/etc
%dir %{_sysconfdir}/icinga/etc/modules
%config(noreplace) %{_sysconfdir}/icinga/etc/icinga.cfg
%dir %{_sysconfdir}/icinga/etc/objects
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/commands.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/contacts.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/notifications.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/localhost.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/printer.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/switch.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/templates.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/timeperiods.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/objects/windows.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/resource.cfg
%{_bindir}/icinga
%{_bindir}/icingastats
%{_libdir}/icinga/p1.pl
%dir %{_sysconfdir}/icinga/var
%dir %{_sysconfdir}/icinga/var/checkresults
%attr(2755,icinga,icingacmd) %{_sysconfdir}/icinga/var/rw/
%{logdir}
%{logdir}/archives

%files doc
%defattr(-,icinga,icinga,-)
%{_sysconfdir}/icinga/share/docs

%files gui
%defattr(-,icinga,icinga,-)
%config(noreplace) %attr(-,root,root) %{apacheconfdir}/icinga.conf
%config(noreplace) %{_sysconfdir}/icinga/etc/cgi.cfg
%config(noreplace) %{_sysconfdir}/icinga/etc/cgiauth.cfg
%{_sysconfdir}/icinga
%{_sysconfdir}/icinga/sbin
%dir %{_sysconfdir}/icinga/share
%{_sysconfdir}/icinga/share/contexthelp
%{_sysconfdir}/icinga/share/images
%{_sysconfdir}/icinga/share/index.html
%{_sysconfdir}/icinga/share/js
%{_sysconfdir}/icinga/share/main.html
%{_sysconfdir}/icinga/share/media
%{_sysconfdir}/icinga/share/menu.html
%{_sysconfdir}/icinga/share/robots.txt
%{_sysconfdir}/icinga/share/sidebar.html
%{_sysconfdir}/icinga/share/ssi
%{_sysconfdir}/icinga/share/stylesheets
%attr(2775,icinga,icingacmd) %dir %{logdir}/gui
%attr(664,icinga,icingacmd) %{logdir}/gui/index.htm
%attr(664,icinga,icingacmd) %{logdir}/gui/.htaccess

%files api
%defattr(-,icinga,icinga,-)
%dir %{_sysconfdir}/icinga/share/icinga-api
%{_sysconfdir}/icinga/share/icinga-api/IcingaApi.php
%{_sysconfdir}/icinga/share/icinga-api/contrib
%{_sysconfdir}/icinga/share/icinga-api/objects
%{_sysconfdir}/icinga/share/icinga-api/tests
%attr(2775,icinga,icingacmd) %dir %{logdir}/api


%changelog
* Wed Jun 29 2011 Michael Friedrich <michael.friedrich@univie.ac.at> - 1.5.0-1
- set to 1.5.0 target, remove provides nagios version, set idoutils.cfg-sample
- move all logging to one location https://bugzilla.redhat.com/show_bug.cgi?id=693608
- add log-dir, cgi-log-dir, phpapi-log-dir to configure, remove the manual creation
- remove manual logdir creation and movings, as no longer needed
- add objects/notifications.cfg for further examples
- fix file perms and locations of cfgs
- fix group for doc

* Wed May 11 2011 Michael Friedrich <michael.friedrich@univie.ac.at> - 1.4.0-2
- undo changes on icinga-cmd group, use icingacmd like before

* Thu Apr 28 2011 Michael Friedrich <michael.friedrich@univie.ac.at> - 1.4.0-1
- update for release 1.4.0
- remove perl subst for eventhandler submit_check_result, this is now done by configure
- remove top.html, doxygen
- set cgi log permissions to apache user
- honour modules/ in icinga cfg and modules/idoutils.cfg for neb definitions
- add /icinga/log for cmd.cgi logging, includes .htaccess

* Tue Mar 31 2011 Christoph Maser <cmaser@gmx.de> - 1.3.1-1
- update for release 1.3.1

* Tue Feb 15 2011 Christoph Maser <cmaser@gmx.de> - 1.3.0-2
- move cgis to libdir
- remove suse suppot (packages available at opensuse build system)
- add doxygen docs

* Wed Nov 03 2010 Michael Friedrich <michael.friedrich@univie.ac.at> - 1.3.0-1
- prepared 1.3.0, added log2ido for idoutils install

* Mon Oct 25 2010 Christoph Maser <cmaser@gmx.de> - 1.2.1-1
- update for release 1.2.1
- add build dep for httpd
- set INSTALL_OPTS_WEB=""

* Thu Sep 30 2010 Christoph Maser <cmaser@gmx.de> - 1.2.0-1
- update for release 1.2.0

* Mon Sep 20 2010 Michael Friedrich <michael.friedrich@univie.ac.at> - 1.0.3-4
- remove php depency for classic gui

* Wed Sep 01 2010 Christoph Maser <cmaser@gmx.de> - 1.0.3-3
- Put documentation in a separate package

* Tue Aug 31 2010 Christoph Maser <cmaser@gmx.de> - 1.0.3-2
- Set icinga-api logdir ownership to apache user 
- add php dependency for icinga-gui subpackage

* Wed Aug 18 2010 Christoph Maser <cmaser@gmx.de> - 1.0.3-1
- Update to 1.0.3-1

* Thu Jul 05 2010 Christoph Maser <cmaser@gmx.de> - 1.0.2-2
- Enable debuginfo

* Thu Jun 24 2010 Christoph Maser <cmaser@gmx.de> - 1.0.2-1
- Update to 1.0.2-1

* Wed Mar 03 2010 Christoph Maser <cmr@financial.com> - 1.0.1-1
- Update to 1.0.1-1

* Tue Dec 15 2009 Christoph Maser <cmr@financial.com> - 1.0-1
- Update to 1.0-1

* Mon Oct 26 2009 Christoph Maser <cmr@financial.com> - 1.0-0.RC1.2
- Split out icinga-api in sub package

* Mon Oct 26 2009 Christoph Maser <cmr@financial.com> - 1.0-0.RC1.1
- Update to 1.0-RC1
- Correct checkconfig --del in idoutils #preun

* Mon Oct 26 2009 Christoph Maser <cmr@financial.com> - 0.8.4-3
- Use icinga-cmd group and add apache user to that group instead
  of using apachegroup as icinga command group.

* Wed Oct 07 2009 Christoph Maser <cmr@financial.com> - 0.8.4-2
- make packages openSUSE compatible
- add #apachecondir, #apacheuser, #apachegroup depending on vendor
- configure add --with-httpd-conf=#{apacheconfdir} 
- configure add --with-init-dir=#{_initrddir}

* Wed Sep 16 2009 Christoph Maser <cmr@financial.com> - 0.8.4-1
- Update to version 0.8.4.

* Tue Sep 15 2009 Christoph Maser <cmr@financial.com> - 0.8.3-3
- Apply patch from 
  https://git.icinga.org/index?p=icinga-core.git;a=commit;h=8b3505883856310472979b152b9960f81cdbaad7

* Tue Sep 15 2009 Christoph Maser <cmr@financial.com> - 0.8.3-2
- Apply patch from 
  https://git.icinga.org/index?p=icinga-core.git;a=commit;h=068baf7bfc99a2a5a88b64d06df49d7395008b40

* Wed Sep 09 2009 Christoph Maser <cmr@financial.com> - 0.8.3-1
- Update to version 0.8.3.

* Thu Aug 27 2009 Christoph Maser <cmr@financial.com> - 0.8.2-3
- fix dir name ndoutils -> idoutils

* Thu Aug 27 2009 Christoph Maser <cmr@financial.com> - 0.8.2-2
- fix idututils post script
- copy database scripts from source to sysconfigdir

* Sat Aug 22 2009 Christoph Maser <cmr@financial.com> - 0.8.2-1
- Update to release 0.8.2.
- remove idoutils-init, init-script for ido2db is shipped now 

* Sun Jul 19 2009 Christoph Maser <cmr@financial.com> - 0.8.1-1
- initial package

