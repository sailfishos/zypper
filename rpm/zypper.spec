Name:       zypper
Summary:    Command line software manager using libzypp
Version:    1.14.38
Release:    1
License:    GPLv2+
URL:        https://github.com/sailfishos/zypper
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}-rpmlintrc
Patch0:     0001-Disable-doc-building-because-it-now-needs-text-tools.patch
Patch1:     0001-Fix-obsolete-diff-argument.patch
Patch2:     0001-Don-t-log-by-default.patch
Requires:   procps
BuildRequires:  pkgconfig(libzypp) >= 17.24.0
BuildRequires:  pkgconfig(augeas) >= 1.10.0
BuildRequires:  boost-devel  >= 1.33.1
BuildRequires:  gettext-devel >= 0.15
BuildRequires:  readline-devel >= 5.1
BuildRequires:  gcc-c++ >= 7
BuildRequires:  cmake >= 3.1
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
%autosetup -p1 -n %{name}-%{version}/upstream

%build

%cmake .  \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DSYSCONFDIR=%{_sysconfdir} \
    -DCMAKE_VERBOSE_MAKEFILE=TRUE \
    -DCMAKE_C_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_CXX_FLAGS_RELEASE:STRING="%{optflags}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DUSE_TRANSLATION_SET=${TRANSLATION_SET:-zypper}

%make_build

%install
%make_install
%{__install} -d -m755 %buildroot%_var/log
touch %buildroot%_var/log/zypper.log

rm -rf %{buildroot}%{_docdir}/packages

%find_lang zypper

%files -f zypper.lang
%license COPYING
%defattr(-,root,root,-)
%config %{_sysconfdir}/zypp/zypper.conf
%config %{_sysconfdir}/logrotate.d/zypper.lr
%config %{_sysconfdir}/logrotate.d/zypp-refresh.lr
%{_sysconfdir}/bash_completion.d/zypper.sh
%{_bindir}/zypper
%{_bindir}/installation_sources
%{_bindir}/needs-restarting
%{_sbindir}/zypp-refresh
%dir %{_datadir}/zypper
%{_datadir}/zypper/zypper.aug
%dir %{_datadir}/zypper/xml
%{_datadir}/zypper/xml/xmlout.rnc
# declare ownership of the log file but prevent
# it from being erased by rpm -e
%ghost %config %attr (640,root,root) %{_var}/log/zypper.log

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

