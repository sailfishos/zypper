Name:       zypper
Summary:    Command line software manager using libzypp
Version:        1.14.6
Release:    1
Group:      System/Packages
License:    GPLv2+
URL:        http://en.opensuse.org/Zypper
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}-rpmlintrc
Patch0:     0001-Disable-doc-building-because-it-now-needs-text-tools.patch
Requires:   procps
BuildRequires:  pkgconfig(libzypp) >= 17.2.2
BuildRequires:  pkgconfig(augeas) >= 0.5.0
BuildRequires:  boost-devel  >= 1.33.1
BuildRequires:  gettext-devel >= 0.15
BuildRequires:  readline-devel >= 5.1
BuildRequires:  cmake >= 2.4.6
BuildRequires:  gcc-c++ >= 4.7
BuildRequires:  cmake >= 2.4.6
BuildRequires:  libxml2-devel

%description
Zypper is a command line tool for managing software. It can be used to add
package repositories, search for packages, install, remove, or update packages,
install patches, hardware drivers, verify dependencies, and more.

Zypper can be used interactively or non-interactively by user, from scripts,
or front-ends.


%package log
Summary:    CLI for accessing the zypper logfile
Requires:   %{name} = %{version}-%{release}
Requires:   python-argparse

%description log
CLI for accessing the zypper logfile.


%package aptitude
Summary:    aptitude compatibility with zypper
BuildArch:    noarch
Requires:   %{name} = %{version}-%{release}
Requires:   perl

%description aptitude
%{summary}.



%prep
%setup -q -n %{name}-%{version}/upstream

# zypper-libxml2.patch
%patch0 -p1

%build

%cmake .  \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DSYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_TRANSLATION_SET=${TRANSLATION_SET:-zypper}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
%{__install} -d -m755 %buildroot%_var/log
touch %buildroot%_var/log/zypper.log

%find_lang zypper

%files -f zypper.lang
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/zypp/zypper.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zypper.lr
%config(noreplace) %{_sysconfdir}/logrotate.d/zypp-refresh.lr
%{_sysconfdir}/bash_completion.d/zypper.sh
%{_bindir}/zypper
%{_bindir}/installation_sources
%{_sbindir}/zypp-refresh
%dir %{_datadir}/zypper
%{_datadir}/zypper/zypper.aug
%dir %{_datadir}/zypper/xml
%{_datadir}/zypper/xml/xmlout.rnc
%doc %dir %{_datadir}/doc/packages/zypper
%doc %{_datadir}/doc/packages/zypper/COPYING
%doc %{_datadir}/doc/packages/zypper/HACKING
# declare ownership of the log file but prevent
# it from being erased by rpm -e
%ghost %config(noreplace) %attr (640,root,root) %{_var}/log/zypper.log

%files log
%defattr(-,root,root,-)
%{_sbindir}/zypper-log

%files aptitude
%defattr(-,root,root,-)
%{_bindir}/aptitude
%{_bindir}/apt-get
%{_bindir}/apt
%config %{_sysconfdir}/zypp/apt-packagemap.d/10-packagemap.pm
%config %{_sysconfdir}/zypp/apt-packagemap.d/50-libperl.pm
%config %{_sysconfdir}/zypp/apt-packagemap.d/50-libruby.pm
%config %{_sysconfdir}/zypp/apt-packagemap.d/50-python.pm
%config %{_sysconfdir}/zypp/apt-packagemap.d/90-devel.pm

