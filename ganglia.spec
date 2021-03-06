#
# $Id: ganglia.spec.in 2636 2011-07-08 01:11:45Z rufustfirefly $
#
# @configure_input@
#
# IMPORTANT NOTE:
# This spec file has conditional constructs using the noarch target.
# To get all packages build you must include noarch and your real target
# (ex: i386, i686, x86_64) when calling rpmbuild as shown by the following
# command line aimed at 80386 or higher CPUs :
#
# % rpmbuild -ta --target noarch,i386 ganglia-3.2.0.tar.gz
#
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Ganglia Distributed Monitoring System
Name: ganglia
Version: 3.3.1
URL: http://ganglia.info/
# The Release macro value is set in configure.in, please update it there.
Release: 1
License: BSD
Vendor: Ganglia Development Team <ganglia-developers@lists.sourceforge.net>
Group: System Environment/Base
Source: %{name}-%{version}.tar.gz
Patch0:             diskusage-pcre.patch
Buildroot: %{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: libpng-devel, libart_lgpl-devel, gcc-c++, python-devel, libconfuse-devel, make, pcre-devel, autoconf, automake, subversion, libtool, libxslt
%if 0%{?suse_version}
BuildRequires:  freetype2-devel, libapr1-devel
%if 0%{?suse_version} > 1020
BuildRequires: rrdtool-devel, libexpat-devel
%else
BuildRequires: rrdtool, expat
%endif
%else
BuildRequires: expat-devel, rrdtool-devel, freetype-devel, apr-devel > 1
%endif
%define conf_dir /etc/ganglia
%define gmond_conf %{_builddir}/%{?buildsubdir}/gmond/gmond.conf
%define generate_gmond_conf %(test -e %gmond_conf && echo 0 || echo 1)

%description
Ganglia is a scalable, real-time monitoring and execution environment

######################################################################
################## noarch section ####################################
######################################################################
%ifarch noarch
%package web
Summary: Ganglia Web Frontend
Group: System Environment/Base
Obsoletes: ganglia-webfrontend < %{version}
Provides: ganglia-webfrontend = %{version}
# We should put rrdtool as a Requires too but rrdtool rpm support is very weak
# so most people install from source
#Requires: ganglia-gmetad >=  3.3.1
Requires: php >= 5, php-gd
%if 0%{?suse_version}
%define web_prefixdir /srv/www/htdocs/ganglia
%else
%define web_prefixdir /var/www/html/ganglia
%endif
Prefix: %{web_prefixdir}

%description web
This package provides a web frontend to display the XML tree published by
ganglia, and to provide historical graphs of collected metrics. This website is
written in the PHP5 language and uses the Dwoo templating engine.

#######################################################################
#######################################################################
%else

%package gmetad
Summary: Ganglia Meta daemon http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: ganglia-monitor-core-gmetad < %{version}
Obsoletes: ganglia-monitor-core < %{version}
Provides: ganglia-monitor-core-gmetad = %{version}
Provides: ganglia-monitor-core = %{version}

%description gmetad
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters
to form a monitoring grid. It also keeps metric history using rrdtool.

%package gmetad-python
Summary: Ganglia Meta daemon in Python http://ganglia.sourceforge.net/
Group: System Environment/Base
Requires: python-rrdtool
Obsoletes: ganglia-monitor-core-gmetad < %{version}
Obsoletes: ganglia-monitor-core < %{version}
Provides: ganglia-monitor-core-gmetad = %{version}
Provides: ganglia-monitor-core = %{version}
Conflicts: ganglia-gmetad

%description gmetad-python
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmetad daemon aggregates monitoring data from several clusters
to form a monitoring grid. It also keeps metric history using rrdtool.

gmetad-python is a re-write of the original gmetad code (written in C)
with pluggable interface.  The RRD files, both the metric RRDs and summary
RRDs are being written by RRD plugins rather than directly from gmetad.
This provides the ability to plug in new metric storage modules to support
other types of storage mechanisms other than RRD and also the ability to
plug in any type of gmetad-level analysis.

%package gmond
Summary: Ganglia Monitor daemon http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: ganglia-monitor-core-gmond < %{version}
Obsoletes: ganglia-monitor-core < %{version}
Provides: ganglia-monitor-core-gmond = %{version}
Provides: ganglia-monitor-core = %{version}

%description gmond
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond daemon provides the ganglia service within a single cluster or
Multicast domain.

%package gmond-modules-python
Summary: Ganglia Monitor daemon DSO/Python metric modules support http://ganglia.sourceforge.net/
Group: System Environment/Base
Requires: ganglia-gmond, python

%description gmond-modules-python
Ganglia is a scalable, real-time monitoring and execution environment
with all execution requests and statistics expressed in an open
well-defined XML format.

This gmond modules support package provides the capability of loading gmetric/python modules
via DSO at daemon start time instead of via gmetric

%package devel
Summary: Ganglia static libraries and header files http://ganglia.sourceforge.net/
Group: Development/Libraries
# revisit this list. it might be libtool bloat
Requires: expat-devel, apr-devel > 1
%if 0%{?suse_version}
Requires: libconfuse-devel, libexpat-devel, libapr1-devel, libganglia
%endif

%description devel
The Ganglia Monitoring Core library provides a set of functions that programmers
can use to build scalable cluster or grid applications

%package -n libganglia
Summary: Ganglia Shared Libraries http://ganglia.sourceforge.net/
Group: System Environment/Base
Obsoletes: libganglia-3_1_0

%description -n libganglia
The Ganglia Shared Libraries contains common libraries required by both gmond and
gmetad packages

%endif

%prep
%setup -n %{name}-%{version}
%patch0 -p1
## Hey, those shouldn't be executable...
chmod -x lib/*.{h,x}

%build
%configure --with-gmetad --enable-status --sysconfdir=%{conf_dir}
%ifnarch noarch
make
%endif
cd gmetad-python
%{__python} setup.py build

%pre

%ifnarch noarch

%post gmetad
/sbin/chkconfig --add gmetad

if [ -e /etc/gmetad.conf ]; then
  %__mv /etc/gmetad.conf %{conf_dir}
fi

%post gmetad-python
/sbin/chkconfig --add gmetad-python

%post gmond
/sbin/chkconfig --add gmond

LEGACY_GMOND_CONF=%{conf_dir}/gmond.conf
if [ -e /etc/gmond.conf ];
then
  LEGACY_GMOND_CONF=/etc/gmond.conf
fi

METRIC_LIST="`%{_sbindir}/gmond -c ${LEGACY_GMOND_CONF} -m`"
if [[ $? != 0 ]]; then
  # They may have an old configuration file format
  echo "-----------------------------------------------------------"
  echo "IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT"
  echo "-----------------------------------------------------------"
  echo "Parsing your gmond.conf file failed"
  echo "It appears that you are upgrading from ganglia gmond version"
  echo "2.5.x.  The configuration file has changed and you need to "
  echo "convert your old 2.5.x configuration file to the new format."
  echo ""   
  echo "To convert your old configuration file to the new format"
  echo "simply run the command:"
  echo ""
  echo "% gmond --convert old.conf > new.conf"
  echo ""
  echo "This conversion was not made automatic to prevent unknowningly"
  echo "altering your configuration without your notice."
else
  if [ `echo "$METRIC_LIST" | wc -l` -eq 0 ];
  then
    echo "-----------------------------------------------------------"
    echo "IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT"
    echo "-----------------------------------------------------------"
    echo "No metrics detected - perhaps you are using a gmond.conf"
    echo "file from Ganglia 3.0 or earlier."
    echo "Please see the README file for details about how to"
    echo "create a valid configuration."
  else
    if [ -e /etc/gmond.conf ]; then
      %__mv /etc/gmond.conf %{conf_dir}
    fi
  fi
fi
   
%preun gmetad
if [ "$1" = 0 ]
then
   /etc/init.d/gmetad stop
   /sbin/chkconfig --del gmetad
fi

%preun gmetad-python
if [ "$1" = 0 ]
then
   /etc/init.d/gmetad-python stop
   /sbin/chkconfig --del gmetad-python
fi

%preun gmond
if [ "$1" = 0 ]
then
   /etc/init.d/gmond stop
   /sbin/chkconfig --del gmond
fi

%post   -n libganglia -p /sbin/ldconfig

%postun -n libganglia -p /sbin/ldconfig

%endif #ifnarch noarch

%install
# Flush any old RPM build root
%__rm -rf $RPM_BUILD_ROOT

%ifarch noarch

%__make -C web install
%__install -d -m 0755 $RPM_BUILD_ROOT/%{web_prefixdir}
%__cp -rf web/* $RPM_BUILD_ROOT/%{web_prefixdir}
%__rm -f $RPM_BUILD_ROOT/%{web_prefixdir}/Makefile*
%__rm -f $RPM_BUILD_ROOT/%{web_prefixdir}/*.in
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/filters
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/dwoo

%else

# Create the directory structure
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/init.d
%__install -d -m 0755 $RPM_BUILD_ROOT/etc/sysconfig
%__install -d -m 0755 $RPM_BUILD_ROOT/var/lib/ganglia/rrds

# Move the files into the structure
%if 0%{?suse_version}
   %__cp -f gmond/gmond.init.SuSE $RPM_BUILD_ROOT/etc/init.d/gmond
   %__cp -f gmetad/gmetad.init.SuSE $RPM_BUILD_ROOT/etc/init.d/gmetad
   sed -e 's/sbin\/gmetad/sbin\/gmetad.py/' gmetad/gmetad.init.SuSE > $RPM_BUILD_ROOT/etc/init.d/gmetad-python
   chmod +x $RPM_BUILD_ROOT/etc/init.d/gmetad-python
%else
   %__cp -f gmond/gmond.init $RPM_BUILD_ROOT/etc/init.d/gmond
   %__cp -f gmetad/gmetad.init $RPM_BUILD_ROOT/etc/init.d/gmetad
   sed -e 's/sbin\/gmetad/sbin\/gmetad.py/' gmetad/gmetad.init > $RPM_BUILD_ROOT/etc/init.d/gmetad-python
   chmod +x $RPM_BUILD_ROOT/etc/init.d/gmetad-python
%endif
%__cp -f gmetad/gmetad-default $RPM_BUILD_ROOT/etc/sysconfig/gmetad

%__install -d -m 0755 $RPM_BUILD_ROOT%{conf_dir}
%__install -d -m 0755 $RPM_BUILD_ROOT%{conf_dir}/conf.d
%__install -d -m 0755 $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules

%if %generate_gmond_conf
# We just output the default gmond.conf from gmond using the '-t' flag
  gmond/gmond -t > $RPM_BUILD_ROOT%{conf_dir}/gmond.conf
%else
  %__cp -f %gmond_conf $RPM_BUILD_ROOT%{conf_dir}/gmond.conf
%endif
#%__cp -f gmetad/gmetad.conf $RPM_BUILD_ROOT%{conf_dir}/gmetad.conf
%__cp -f gmond/modules/conf.d/* $RPM_BUILD_ROOT%{conf_dir}/conf.d

# Copy the python metric modules and .conf files
%__cp -f gmond/python_modules/conf.d/*.pyconf $RPM_BUILD_ROOT%{conf_dir}/conf.d/
%{__python} -c 'import compileall; compileall.compile_dir("gmond/python_modules", 1, "/", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("gmond/python_modules", 1, "/", 1)' > /dev/null
%__cp -f gmond/python_modules/*/*.{py,pyc,pyo} $RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/

# Don't install the example modules
%__rm -f $RPM_BUILD_ROOT%{conf_dir}/conf.d/example.conf
%__rm -f $RPM_BUILD_ROOT%{conf_dir}/conf.d/example.pyconf
%__rm -f $RPM_BUILD_ROOT%{conf_dir}/conf.d/spfexample.pyconf

# Clean up the .conf.in files
%__rm -f $RPM_BUILD_ROOT%{conf_dir}/conf.d/*.conf.in

# Disable the diskusage module until it is configured properly
%__mv $RPM_BUILD_ROOT%{conf_dir}/conf.d/diskusage.pyconf $RPM_BUILD_ROOT%{conf_dir}/conf.d/diskusage.pyconf.off

%__make DESTDIR=$RPM_BUILD_ROOT install
%__make -C gmond gmond.conf.5

# gmetad-python
cd gmetad-python
%{__python} setup.py install --prefix=/usr --skip-build --install-scripts=%{_sbindir} --root=$RPM_BUILD_ROOT
%{__python} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/gmetad"'", 1, "/", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{_libdir}/ganglia/python_modules/gmetad"'", 1, "/", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{python_sitelib}/Gmetad"'", 1, "/", 1)' > /dev/null
%{__python} -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{_sbindir}"'", 1, "/", 1)' > /dev/null
%{__python} -O -c 'import compileall; compileall.compile_dir("'"$RPM_BUILD_ROOT%{_sbindir}"'", 1, "/", 1)' > /dev/null

%endif

%ifnarch noarch

%files gmetad
%defattr(-,root,root)
%attr(0755,nobody,nobody)/var/lib/ganglia/
%{_sbindir}/gmetad
/etc/init.d/gmetad
%config(noreplace) /etc/sysconfig/gmetad
%{_mandir}/man1/gmetad.1*
%config(noreplace) %{conf_dir}/gmetad.conf

%files gmetad-python
%defattr(-,root,root)
%{_sbindir}/gmetad.py*
/etc/init.d/gmetad-python
%config(noreplace) %{conf_dir}/gmetad-python.conf
%{python_sitelib}/*
%dir %{_libdir}/ganglia
%dir %{_libdir}/ganglia/python_modules
%{_libdir}/ganglia/python_modules/gmetad*
%{_mandir}/man1/gmetad.py.1*

%files gmond
%defattr(-,root,root)
%{_bindir}/gmetric
%{_bindir}/gstat
%{_sbindir}/gmond
/etc/init.d/gmond
%{_mandir}/man1/gmetric.1*
%{_mandir}/man1/gmond.1*
%{_mandir}/man1/gstat.1*
%{_mandir}/man5/gmond.conf.5*
%config(noreplace) %{conf_dir}/gmond.conf
%dir %{conf_dir}
%dir %{conf_dir}/conf.d/
%config(noreplace) %{conf_dir}/conf.d/modgstatus.conf
%dir %{_libdir}/ganglia/
%{_libdir}/ganglia/modmulticpu.so*
%{conf_dir}/conf.d/multicpu.conf
%{_libdir}/ganglia/modcpu.so*
%{_libdir}/ganglia/moddisk.so*
%{_libdir}/ganglia/modgstatus.so
%{_libdir}/ganglia/modload.so*
%{_libdir}/ganglia/modmem.so*
%{_libdir}/ganglia/modnet.so*
%{_libdir}/ganglia/modproc.so*
%{_libdir}/ganglia/modsys.so*

%files gmond-modules-python
%defattr(-,root,root,-)
%dir %{_libdir}/ganglia/python_modules/
%{_libdir}/ganglia/python_modules/*.py*
%{_libdir}/ganglia/modpython.so*
%config(noreplace) %{conf_dir}/conf.d/modpython.conf
%config(noreplace) %{conf_dir}/conf.d/*.pyconf*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ganglia.h
%{_includedir}/ganglia_gexec.h
%{_includedir}/gm_metric.h
%{_includedir}/gm_mmn.h
%{_includedir}/gm_msg.h
%{_includedir}/gm_protocol.h
%{_includedir}/gm_value.h
%{_libdir}/libganglia*.so
%{_libdir}/libganglia*.*a
%{_bindir}/ganglia-config

%files -n libganglia
%defattr(-,root,root,-)
%{_libdir}/libganglia*.so.*

%else

%files web
%defattr(-,root,root)
%attr(0755,nobody,nobody)/var/lib/ganglia/filters
%attr(0755,apache,apache)/var/lib/ganglia/dwoo
%dir %{web_prefixdir}/
%dir %{web_prefixdir}/dwoo
%config(noreplace) %{web_prefixdir}/conf.php
%{web_prefixdir}/AUTHORS
%{web_prefixdir}/auth.php
%{web_prefixdir}/calendar.php
%{web_prefixdir}/cluster_legend.html
%{web_prefixdir}/cluster_view.php
%{web_prefixdir}/COPYING
%{web_prefixdir}/eval_config.php
%{web_prefixdir}/footer.php
%{web_prefixdir}/functions.php
%{web_prefixdir}/ganglia.php
%{web_prefixdir}/get_context.php
%{web_prefixdir}/get_ganglia.php
%{web_prefixdir}/graph.d
%{web_prefixdir}/graph.php
%{web_prefixdir}/grid_tree.php
%{web_prefixdir}/header.php
%{web_prefixdir}/host_view.php
%{web_prefixdir}/index.php
%{web_prefixdir}/meta_view.php
%{web_prefixdir}/node_legend.html
%{web_prefixdir}/physical_view.php
%{web_prefixdir}/pie.php
%{web_prefixdir}/private_clusters
%{web_prefixdir}/show_node.php
%{web_prefixdir}/styles.css
%{web_prefixdir}/templates
%{web_prefixdir}/version.php
%{web_prefixdir}/dwoo/*

%endif

%clean
%__rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Mar 26 2012 Josh Toft <joshtoft@gmail.com>
- New upstream release 3.3.1
* Thu Mar 31 2011 Bernard Li <bernard@vanhpc.org>
- Allow file permissions for gmetric and gstat to be automatically set
* Wed Jan 26 2011 Bernard Li <bernard@vanhpc.org>
- Remove manual steps to install manpages as they are now installed via `make install`
- Include manpage for gmetad-python
- Remove hardcoded library version for libganglia
* Wed Jan 12 2011 Bernard Li <bernard@vanhpc.org>
- Fix gmetad-python subpackage not including files from Python site-packages dir
- Break gmetad-python installation into build and install stages
- Byte compile additional gmond-modules-python and gmetad-python scripts
- Do not include spfexample.pyconf
* Wed Sep  8 2010 Bernard Li <bernard@vanhpc.org>
- Replace TemplatePower with Dwoo for PHP templating engine
* Tue Aug 17 2010 Bernard Li <bernard@vanhpc.org>
- Use the 'install' target for web/ instead of calling make on
  conf.php and version.php individually
* Tue Jan 12 2010 Daniel Pocock <daniel@pocock.com.au>
- Add eval_config.php to files list
* Tue Jan  5 2010 Daniel Pocock <daniel@pocock.com.au>
- Add dependency on pcre-devel
* Thu Sep 17 2009 Jesse Becker <hawson@gmail.com>
- Use %{version} tags where possible instead of hard-coding
* Thu Jul 30 2009 Daniel Pocock <daniel@pocock.com.au>
- gstatus is now compiled and included in the RPM, but not loaded by default
* Sun Jun 14 2009 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- expat-devel is needed for building gstat
* Sat Nov 15 2008 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- Update manually selected list of files in %{web_prefixdir}
* Sat Oct 25 2008 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- Instruct RPM to byte compile python modules at install time
* Wed Oct 01 2008 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- Add missing defattr for gmond-modules-python
* Wed Jul 30 2008 Bernard Li <bernard@vanhpc.org>
- Add make to BuildRequires
* Sun Jul 20 2008 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- Remove ChangeLog from ganglia-web
* Tue Jun 10 2008 Bernard Li <bernard@vanhpc.org>
- New subpackage gmetad-python for the Python re-write of gmetad
* Wed Jun 04 2008 Bernard Li <bernard@vanhpc.org>
- Add ganglia_gexec.h to ganglia-devel package
* Tue May 06 2008 Bernard Li <bernard@vanhpc.org>
- Removed host_gmetrics.php from ganglia-web
* Tue Apr 15 2008 Bernard Li <bernard@vanhpc.org>
- Cleanup of *.{la,a} in %{_libdir}/ganglia is not needed anymore
* Mon Mar 31 2008 Carlo Marcelo Arenas Belon <carenas@sajinet.com.pe>
- Add gm_value.h and gm_msg.h
* Thu Mar 28 2008 Brad Nicholes <bnicholes@novell.com>
- Add the headers file in the include directory
* Thu Mar 27 2008 Bernard Li <bernard@vanhpc.org>
- Added man1 pages gmetad, gmetric, gmond, gstat
* Thu Mar 13 2008 Jesse Becker <hawson@gmail.com>
- Add web/graph.d directory and contents to %files.
* Fri Feb 15 2008 Bernard Li <bernard@vanhpc.org>
- Fix bug where .pyconf files are copied to %{_libdir}/ganglia/python_modules
- Enable tcpconn.py by default since code is now compatible with Python 2.3.x
- No longer need to run %configure when building ganglia-web (noarch)
* Tue Dec 18 2007 Brad Nicholes <bnicholes@novell.com>
- Remove all built in metrics and replace them with metric modules
* Thu Nov 29 2007 Brad Nicholes <bnicholes@novell.com>
- Do not install the modgstatus.conf file
- Add scoreboard.h to the -devel package
* Fri Nov 16 2007 Bernard Li <bernard@vanhpc.org>
- Set variable conf_dir to /etc/ganglia
- Migrate /etc/{gmond,gmetad}.conf files to /etc/ganglia for upgrades etc.
* Fri Nov 09 2007 Bernard Li <bernard@vanhpc.org>
- Include .pyc files from @moduledir@/python_modules
* Thu Nov 08 2007 Bernard Li <bernard@vanhpc.org>
- Clean up /etc/ganglia/conf.d/*.conf.in files
* Wed Oct 10 2007 Bernard Li <bernard@vanhpc.org>
- Clean up comments -- they were affecting output of rpm -q --scripts
- Spec by cleanup by darix, new package libganglia for common shared libraries
- New package ganglia-gmond-modules-python
* Tue Oct 9 2007 Brad Nicholes <bnicholes@novell.com>
- Add tcpconn python metric module
* Fri Jul 13 2007 Brad Nicholes <bnicholes@novell.com>
- Don't install the example modules
* Wed Jul 11 2007 Bernard Li <bernard@vanhpc.org>
- Delete .in files in %{web_prefixdir}
* Wed Jul 10 2007 Bernard Li <bernard@vanhpc.org>
- Added python-devel to BuildRequires
* Wed Jul 3 2007 Brad Nicholes <bnicholes@novell.com>
- Add the python modules and configuration
* Wed Jun 14 2007 Brad Nicholes <bnicholes@novell.com>
- Build the python support module by default
* Fri May 18 2007 Bernard Li <bernard@vanhpc.org>
- Add php-gd to web subpackage Requires
* Wed May 9 2007 Brad Nicholes <bnicholes@novell.com>
- Converted to dynamically link all external libraries
* Fri Apr 27 2007 Bernard Li <bernard@vanhpc.org>
- Add apr-devel to BuildRequires for distro other than SuSE
  (Red Hat/Fedora/Mandriva)
* Wed Apr 25 2007 Brad Nicholes <bnicholes@novell.com>
- Dynamically link APR rather than statically linking
  the Ganglia version of APR.
* Thu Apr 12 2007 Brad Nicholes <bnicholes@novell.com>
- Move the main .conf file out of /etc and into /etc/ganglia
* Fri Apr 06 2007 Brad Nicholes <bnicholes@novell.com>
- install the module .conf files under a /etc/ganglia/conf.d 
  directory and list the file owner of the .conf files and 
  the module DSOs
* Wed Apr 04 2007 Bernard Li <bernard@vanhpc.org>
- Added libmodexample* files to ganglia-gmond sub-package
* Tue Apr 03 2007 Bernard Li <bernard@vanhpc.org>
- Applied patch from Marcus Rueckert
- Use different web_prefixdir for SuSE
- More extensive use of RPM macroes (eg. %{_mandir}, %{_sbindir})
* Mon Jan 08 2007 Bernard Li <bernard@vanhpc.org>
- Do not automatically start/restart services as this may cause 
  ganglia to startup with bad config.
* Mon Aug 28 2006 Bernard Li <bli@bcgsc.ca>
- Added gcc-c++ to BuildRequires
* Sun Jul 23 2006 Bernard Li <bli@bcgsc.ca>
- Changed make install prefix=$RPM_BUILD_ROOT/usr to
  make DESTDIR=$RPM_BUILD_ROOT install (suggested by Jarod Wilson
  <jwilson@redhat.com>)
* Mon Jun 05 2006 Bernard Li <bli@bcgsc.ca>
- Changed /etc/rc.d/init.d -> /etc/init.d
* Mon May 22 2006 Bernard Li <bli@bcgsc.ca>
- Add rrdtool/rrdtool-devel, freetype2-devel/freetype-devel,
  libart_lgpl-devel to BuildRequires
- Use /usr/lib64 for x86_64
* Sun May 21 2006 Bernard Li <bli@bcgsc.ca>
- Correct init scripts dir for SuSE
- Add BuildRequires for libpng-devel
* Fri Feb 25 2006 Bernard Li <bli@bcgsc.ca>
- Use SuSE specific init scripts if /etc/SuSE-release file exists
* Fri Dec 10 2004 Matt Massie <massie@cs.berkeley.edu>
- Updated the spec file for 2.6.0 release
* Tue Apr 13 2004 Brooks Davis <brooks@one-eyed-alien.net>
- Use the autoconf variable varstatedir instead of /var/lib for consistency.
* Thu Feb 19 2004 Matt Massie <massie@cs.berkeley.edu>
- Removed the /usr/include/ganglia directory from the lib rpm and
  changed the deprecated Copyright to License
* Mon Oct 14 2002 Federico Sacerdoti <fds@sdsc.edu>
- Split package into -gmetad and -gmond subpackages for clarity,
  and separation of purpose/functionality.
* Thu Sep 19 2002 Federico Sacerdoti <fds@sdsc.edu>
- Added config files, made /var/lib/ganglia for RRD storage.
* Mon Mar 11 2002 Matt Massie <massie@cs.berkeley.edu>
- Added support for libganglia, added Prefix: for RPM relocation
* Wed Feb 27 2002 Matt Massie <massie@cs.berkeley.edu>
- Merge gmetric and gmond together into one RPM.  Fix some small bugs.
* Fri Nov  2 2001 Matt Massie <massie@cs.berkeley.edu>
- initial release
