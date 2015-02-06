Name:       zypper
Summary:    Command line software manager using libzypp
Version:        1.11.22
Release:    1
Group:      System/Packages
License:    GPL v2 or later
URL:        http://en.opensuse.org/Zypper
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}-rpmlintrc
Patch0:     zypper-libxml2.patch
Requires:   procps
BuildRequires:  pkgconfig(libzypp) >= 12.2.0
BuildRequires:  pkgconfig(augeas)
BuildRequires:  boost-devel >= 1.33.1
BuildRequires:  gettext-devel >= 0.15
BuildRequires:  readline-devel >= 5.1
BuildRequires:  cmake >= 2.4.6
BuildRequires:  gcc-c++ >= 4.1
BuildRequires:  cmake

%description
Zypper is a command line tool for managing software. It can be used to add
package repositories, search for packages, install, remove, or update packages,
install patches, hardware drivers, verify dependencies, and more.

Zypper can be used interactively or non-interactively by user, from scripts,
or front-ends.


%package log
Summary:    CLI for accessing the zypper logfile
Group:      System/Packages
Requires:   %{name} = %{version}-%{release}
Requires:   python-argparse

%description log
CLI for accessing the zypper logfile.


%package aptitude
Summary:    aptitude compatibility with zypper
Group:      System/Packages
BuildArch:    noarch
Requires:   %{name} = %{version}-%{release}
Requires:   perl

%description aptitude
%{summary}.



%prep
%setup -q -n %{name}-%{version}

cd %{name}
# zypper-libxml2.patch
%patch0 -p1

%build

cd %{name}
%cmake .  \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DSYSCONFDIR=%{_sysconfdir} \
    -DMANDIR=%{_mandir} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_TRANSLATION_SET=${TRANSLATION_SET:-zypper}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
cd %{name}
%make_install
%{__install} -d -m755 %buildroot%_var/log
touch %buildroot%_var/log/zypper.log

%find_lang zypper

%files -f zypper/zypper.lang
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
%doc %{_mandir}/man8/zypper.8*
%doc %dir %{_datadir}/doc/packages/zypper
%doc %{_datadir}/doc/packages/zypper/COPYING
%doc %{_datadir}/doc/packages/zypper/HACKING
# declare ownership of the log file but prevent
# it from being erased by rpm -e
%ghost %config(noreplace) %{_var}/log/zypper.log

%files log
%defattr(-,root,root,-)
%{_sbindir}/zypper-log
%doc %{_mandir}/man8/zypper-log.8*

%files aptitude
%defattr(-,root,root,-)
%{_bindir}/aptitude
