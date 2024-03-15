%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318
%global pypi_name tacker
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate python-blazarclient os-api-ref
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global common_desc \
OpenStack Tacker Service is an NFV Orchestrator for OpenStack

%global with_doc 1

Name:           openstack-%{pypi_name}
Version:        11.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        OpenStack Tacker Service

License:        Apache-2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#
# patches_base=11.0.0.0rc1
#

Source1:        openstack-tacker-server.service
Source2:        tacker.logrotate
Source3:        openstack-tacker-conductor.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  systemd
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  openstack-macros
Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_ordering}

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        OpenStack Tacker Service

%description -n python3-%{pypi_name}
%{common_desc}

This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python3-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Tacker common files.

%package -n python3-%{pypi_name}-tests
Summary:    Tacker unit and functional tests
Requires:   python3-%{pypi_name} = %{version}-%{release}

Requires:  python3-cliff
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-os-testr
Requires:  python3-subunit
Requires:  python3-tackerclient
Requires:  python3-tempest
Requires:  python3-testrepository
Requires:  python3-testtools

Requires:  python3-webtest

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains the Tacker unit and functional test files.

%if 0%{?with_doc}
%package -n python3-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service

%description -n python3-%{pypi_name}-doc
Documentation for OpenStack Tacker service
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/{.doctrees,.buildinfo,.htaccess,_downloads}
%endif

%install
%pyproject_install

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip tacker entry points.
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=./etc/config-generator.conf --output-file=./etc/%{pypi_name}.conf


# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pypi_name}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}/usr/etc/%{pypi_name}/* %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}/usr/etc/rootwrap.d %{buildroot}%{_sysconfdir}
install -p -D -m 640 etc/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# remove /usr/etc, it's not needed
# and the init.d script is in it, which is not needed
# because a systemd script is being included
rm -rf %{buildroot}/usr/etc/

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-conductor.service

%check
%tox -e %{default_toxenv} -- -- --exclude-regex 'ipv6|vnfm|vnflcm|sol_refactored'

%pre common
getent group %{pypi_name} >/dev/null || groupadd -r %{pypi_name}
getent passwd %{pypi_name} >/dev/null || \
    useradd -r -g %{pypi_name} -d %{_sharedstatedir}/%{pypi_name} -s /sbin/nologin \
    -c "OpenStack Tacker Daemons" %{pypi_name}
exit 0

%post
%systemd_post openstack-%{pypi_name}-server.service
%systemd_post openstack-%{pypi_name}-conductor.service

%preun
%systemd_preun openstack-%{pypi_name}-server.service
%systemd_preun openstack-%{pypi_name}-conductor.service

%postun
%systemd_postun_with_restart openstack-%{pypi_name}-server.service
%systemd_postun_with_restart openstack-%{pypi_name}-conductor.service

%files
%license LICENSE
%{_bindir}/%{pypi_name}*
%{_unitdir}/openstack-%{pypi_name}-server.service
%{_unitdir}/openstack-%{pypi_name}-conductor.service
%attr(-, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/api-paste.ini

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/rootwrap.conf
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/prometheus-plugin.yaml
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/rootwrap.d/%{pypi_name}.filters
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%if 0%{?with_doc}
%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Mar 15 2024 RDO <dev@lists.rdoproject.org> 11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

